"""Procedural cinematic score + SFX synced to timeline.json.  Usage: python3 score.py out.wav"""
import json, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
here = Path(__file__).parent
TL = json.loads((here / "timeline.json").read_text())
t = 0.0
for b in TL:
    b["start"] = t
    t += b["d"]
TOTAL = t
N = int((TOTAL + 1.5) * SR)
rng = np.random.default_rng(3)

music = np.zeros((N, 2))
sfx = np.zeros((N, 2))


def note(n):  # midi -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def lp(x, cutoff, q=1.0):
    """Smooth FFT low-pass (mono or stereo)."""
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(x.shape[0], 1 / SR)
    m = 1 / (1 + (f / cutoff) ** (4 * q))
    return np.fft.irfft(X * (m[:, None] if x.ndim == 2 else m), n=x.shape[0], axis=0)


def hp(x, cutoff):
    return x - lp(x, cutoff)


def add(buf, at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N:
        return
    if i < 0:
        sig = sig[-i:]
        i = 0
    sig = sig[: N - i]
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], 1)
    buf[i : i + len(sig)] += sig * gain


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 2 if na else 1
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e


# ---------------- music ----------------
def pad(notes, dur, bright=1.0, a=0.8, r=1.0):
    n = int((dur + r) * SR)
    tt = np.arange(n) / SR
    out = np.zeros((n, 2))
    for m in notes:
        f0 = note(m)
        for ch, det in ((0, -0.0035), (1, 0.0035), (0, 0.0012), (1, -0.0012)):
            f = f0 * (1 + det)
            s = np.zeros(n)
            for h in range(1, 9):
                if f * h > 9000:
                    break
                s += np.sin(2 * np.pi * f * h * tt + h * 0.7) / h ** (1.9 - 0.5 * bright)
            out[:, ch] += s
    out *= env(n, a, r)[:, None] / (len(notes) * 4)
    # slow breathing
    out *= (0.85 + 0.15 * np.sin(2 * np.pi * 0.18 * tt))[:, None]
    return out


def sub(m, dur, r=0.8):
    n = int((dur + r) * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * note(m) * tt) * env(n, 0.3, r)


def pluck(m, dur=0.6, bright=3000):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = note(m)
    s = sum(np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (5 + h * 3)) / h for h in range(1, 7))
    return s * np.minimum(1, tt * 400)


def bell(m, dur=3.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = note(m)
    s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 1.2)
         + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 2.5)
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 5))
    return s * np.minimum(1, tt * 300)


def kick(f0=55, dur=0.5, click=True):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    fr = f0 + 90 * np.exp(-tt * 35)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 7)
    if click:
        s[:300] += rng.standard_normal(300) * np.linspace(0.4, 0, 300)
    return s


def acts():
    """contiguous act runs -> (act, start, end)"""
    runs = []
    for b in TL:
        if runs and runs[-1][0] == b["act"]:
            runs[-1][2] = b["start"] + b["d"]
        else:
            runs.append([b["act"], b["start"], b["start"] + b["d"]])
    return runs


# chord vocab (midi) — bright, major-centred
Am = [45, 52, 57, 60, 64]
F = [41, 48, 53, 57, 60]
C = [48, 55, 60, 64, 67]
G = [43, 50, 55, 59, 62]
Fmaj7 = [41, 48, 52, 57, 64]
Am7 = [45, 52, 55, 60, 64]
Cmaj7 = [48, 55, 59, 64, 67]
BEAT = 0.6  # 100 bpm; every poster cut lands on this grid


def clap():
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    x = noise(n)
    x = hp(lp(x, 2600), 900)
    e = np.exp(-tt * 28) + 0.6 * np.exp(-np.maximum(tt - 0.012, 0) * 40) * (tt > 0.012)
    return x * e


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    return hp(noise(n), 7500) * np.exp(-np.arange(n) / SR * (18 if open_ else 90))


def noise(n):
    return rng.standard_normal(n)


def drums(s, e, mode):
    """mode: full | half | light"""
    tt, i = s, 0
    while tt < e - 0.05:
        if mode == "full" or (mode == "half" and i % 2 == 0) or (mode == "light" and i % 4 == 0):
            add(music, tt, kick(50, .45), 0.55)
        if i % 2 == 1 and mode != "light":
            add(music, tt, clap(), 0.32, pan=.05)
        if mode != "light":
            add(music, tt + BEAT / 2, hat(i % 4 == 3), 0.09, pan=.35)
            add(music, tt, hat(), 0.05, pan=-.3)
        tt += BEAT
        i += 1


def chords(s, e, seq, step, gain=0.42, bright=1.0, subg=0.24):
    k = 0
    while s + k * step < e - 0.05:
        ch = seq[k % len(seq)]
        dur = min(step, e - s - k * step)
        add(music, s + k * step, pad(ch, dur + .1, bright, a=0.08, r=0.5), gain)
        add(music, s + k * step, sub(ch[0] - 12, dur, r=.3), subg)
        k += 1


def arps(s, e, seq, step, rate, gain=0.12, pattern=(2, 3, 4, 3), octave=12):
    tt, i = s, 0
    while tt < e - 0.1:
        ch = seq[int((tt - s) // step) % len(seq)]
        add(music, tt, pluck(ch[pattern[i % len(pattern)]] + octave, .45), gain, pan=[-.4, .4][i % 2])
        tt += rate
        i += 1


for act, s, e in acts():
    dur = e - s
    if act == 0:  # hook: warm open F major, light pulse
        chords(s, e, [F, C], 2.4, gain=0.38, bright=0.7)
        drums(s + 1.8, e, "light")
    elif act == 1:  # body: driving four-on-the-floor
        chords(s, e, [C, G, Am, F], 2.4, gain=0.4)
        drums(s, e, "full")
        arps(s, e, [C, G, Am, F], 2.4, 0.3, 0.09)
    elif act == 2:  # mind: same groove, faster 16th arps
        chords(s, e, [Am, F, C, G], 2.4, gain=0.38, bright=1.2)
        drums(s, e, "full")
        arps(s, e, [Am, F, C, G], 2.4, 0.15, 0.08, pattern=(2, 3, 4, 3, 4, 2, 3, 4))
    elif act == 3:  # soul: dreamy maj7, half-time + bells
        chords(s, e, [Fmaj7, Am7, Cmaj7, G], 2.4, gain=0.42, bright=1.3)
        drums(s, e, "half")
        r2 = np.random.default_rng(8)
        tt = s + 0.3
        while tt < e - 0.4:
            ch = [Fmaj7, Am7, Cmaj7, G][int((tt - s) // 2.4) % 4]
            add(music, tt, bell(int(r2.choice(ch)) + 24, 2.2), 0.05, pan=float(r2.uniform(-.7, .7)))
            tt += float(r2.choice([0.3, 0.6, 0.6, 0.9]))
    elif act == 5:  # conflict: the beat drops out, clock + low drone
        add(music, s, pad([45, 46, 52], dur + .2, 0.3, a=0.05, r=0.4), 0.45)
        add(music, s, sub(33, dur, r=0.3), 0.3)
        tt = s
        while tt < e:
            n = int(0.03 * SR)
            add(music, tt, hp(noise(n) * np.exp(-np.arange(n) / SR * 200), 2500), 0.2, pan=.2)
            tt += BEAT
    elif act == 4:  # revelation: everything returns, biggest section, then ring out
        end_beat = e - 4.2
        chords(s, end_beat, [F, G, Am, C], 2.4, gain=0.45, bright=1.4, subg=0.3)
        drums(s, end_beat, "full")
        arps(s, end_beat, [F, G, Am, C], 2.4, 0.15, 0.08, pattern=(2, 3, 4, 3, 4, 2, 3, 4))
        add(music, end_beat, pad(F + [69], 4.2, 1.2, a=0.05, r=3.0), 0.45)
        add(music, end_beat, sub(29, 4.0, r=2.5), 0.3)
        add(music, end_beat, bell(77, 4), 0.1)

# ---------------- sfx ----------------
def impact(big=False, low=False):
    dur = 2.4 if big else 1.2
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = (38 if low else 48) + 80 * np.exp(-tt * 12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (1.8 if big else 3.5))
    nz = lp(noise(n), 2500 if not low else 700) * np.exp(-tt * 14) * 0.9
    s = boom + nz
    if big:
        s += hp(noise(n), 5000) * np.exp(-tt * 1.6) * 0.22
    return np.tanh(s * 1.4)


def riser(dur=1.2):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    k = tt / dur
    x = noise(n)
    s = lp(x, 900) * (1 - k) + hp(x, 3000) * k
    tone = np.sin(2 * np.pi * np.cumsum(300 + 1200 * k ** 2) / SR) * 0.2
    return (s * 0.5 + tone) * k ** 2.2


def paper(dur=0.22):
    """paper flip / swipe on each poster cut"""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    e = np.exp(-tt * 22) * np.minimum(1, tt * 600)
    return hp(lp(noise(n), 6000), 1500) * e


def swell(dur=1.0):
    n = int(dur * SR)
    k = np.arange(n) / n
    return lp(noise(n), 1500) * k ** 3


def tick_hit():
    n = int(.3 * SR)
    return np.tanh(kick(75, .3) * 1.4 + hp(noise(n), 4000) * np.exp(-np.arange(n) / SR * 35) * 0.5)


def pop():
    n = int(.12 * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (900 - 2500 * tt) * tt) * np.exp(-tt * 40)


for b in TL:
    s, d, look, fx = b["start"], b["d"], b.get("look", ""), b.get("sfx", "")
    add(sfx, s, paper(), 0.22, pan=float(rng.uniform(-.5, .5)))
    if fx == "slam":
        add(sfx, s, impact(), 0.5)
    elif fx == "slam_low":
        add(sfx, s, impact(low=True), 0.6)
    elif fx == "big":
        add(sfx, s, impact(big=True), 0.55)
    elif fx == "riser_slam":
        add(sfx, s - 1.2, riser(1.2), 0.3)
        add(sfx, s, impact(), 0.5)
    elif fx == "slam_late":
        add(sfx, s + 2.4, impact(), 0.5)
    elif fx == "swell":
        add(sfx, s - 0.9, swell(0.9), 0.22)
    if b.get("tag"):
        add(sfx, s, pop(), 0.25)
    if look == "list":
        slot = d / len(b["words"])
        for i in range(len(b["words"])):
            add(sfx, s + i * slot, tick_hit(), 0.32, pan=[-.2, .2][i % 2])
            if i:
                add(sfx, s + i * slot, paper(), 0.18)
    if look == "stack":
        for i in range(len(b["lines"])):
            add(sfx, s + i * .55, tick_hit(), 0.28)
    if look in ("cream", "red") and fx == "":
        stg = min(.22, d * .4 / len(b["lines"]))
        for i in range(len(b["lines"])):
            add(sfx, s + i * stg, tick_hit(), 0.12)
    if look == "progress":
        n = int(1.7 * SR)
        k = np.arange(n) / n
        add(sfx, s + .7, np.sin(2 * np.pi * np.cumsum(220 + 800 * k ** 2) / SR) * k * 0.5, 0.1)
    if look == "triad":
        for i, m in enumerate([72, 76, 79]):
            add(sfx, s + 1.6 + i * .8, bell(m, 3), 0.16, pan=[-.5, .5, 0][i])
        add(sfx, s + 4.1, impact(big=True), 0.45)
        for m in (65, 69, 72, 77):
            add(sfx, s + 4.1, bell(m, 4), 0.06)
    if look == "echo":
        for i in range(11):
            add(sfx, s + .25 + i * .13, tick_hit(), 0.1, pan=[-.5, .5][i % 2])
        add(sfx, s + 2.2, impact(low=True), 0.35)

# ---------------- reverb + mix ----------------
def reverb(x, secs=2.6, decay=2.2):
    n = int(secs * SR)
    tt = np.arange(n) / SR
    ir = np.stack([lp(noise(n), 6000), lp(noise(n), 6000)], 1) * np.exp(-tt * decay)[:, None]
    ir[: int(.02 * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum(0))
    L = x.shape[0] + n
    sz = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, sz, axis=0) * np.fft.rfft(ir, sz, axis=0), sz, axis=0)[: x.shape[0]]
    return y


music = lp(music, 15000)
mix = 0.7 * (music + 0.18 * reverb(music, 1.8, 3.0)) + sfx + 0.3 * reverb(sfx, 1.8, 3.0)
# fades
fi, fo = int(.4 * SR), int(2.0 * SR)
end = int((TOTAL + 0.6) * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix[end - fo : end] *= np.linspace(1, 0, fo)[:, None]
mix[end:] = 0
mix = np.tanh(mix / np.abs(mix).max() * 1.15) * 0.97
pcm = (mix * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", TOTAL)
