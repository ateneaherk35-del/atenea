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


# chord vocab (midi)
Am = [45, 52, 57, 60, 64]
F = [41, 48, 53, 57, 60]
C = [48, 55, 60, 64, 67]
G = [43, 50, 55, 59, 62]
Fmaj7 = [41, 48, 52, 57, 64]
Cmaj7 = [48, 55, 59, 64, 67]
Dm9 = [50, 57, 60, 64, 65]

for act, s, e in acts():
    dur = e - s
    if act == 0:  # hook: dark sustained Am
        add(music, s, pad([45, 52, 60], dur + 0.5, 0.4, a=1.2, r=1.2), 0.55)
        add(music, s, sub(33, dur), 0.25)
    elif act == 1:  # body: Am/F with heartbeat
        seq = [Am, F]
        step = 2.4
        k = 0
        while s + k * step < e:
            ch = seq[k % 2]
            add(music, s + k * step, pad(ch, min(step, e - s - k * step) + .2, 0.8, a=0.4, r=0.9), 0.5)
            add(music, s + k * step, sub(ch[0] - 12, step), 0.28)
            k += 1
        bt = s + 0.6
        rate = 1.0
        while bt < e - 0.3:
            add(music, bt, kick(48, .45), 0.45)
            add(music, bt + 0.22, kick(44, .4), 0.28)
            rate = max(0.62, rate - 0.012)
            bt += rate
    elif act == 2:  # mind: C G Am F + pluck arpeggio
        seq = [C, G, Am, F]
        step = 2.6
        k = 0
        while s + k * step < e:
            ch = seq[k % 4]
            add(music, s + k * step, pad(ch, min(step, e - s - k * step) + .2, 1.0, a=0.3, r=0.9), 0.42)
            add(music, s + k * step, sub(ch[0] - 12, step), 0.25)
            k += 1
        tt = s + 0.4
        i = 0
        while tt < e - 0.2:
            ch = seq[int((tt - s) // step) % 4]
            m = ch[[2, 3, 4, 3][i % 4]] + 12
            add(music, tt, pluck(m, .5), 0.13, pan=[-.4, .4][i % 2])
            if i % 4 == 0:
                add(music, tt, kick(50, .35, False), 0.25)
            n = int(0.06 * SR)
            add(music, tt + 0.125, hp(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 80), 7000), 0.05, pan=.3)
            tt += 0.25
            i += 1
    elif act == 3:  # soul: lush maj7 + bells
        seq = [Fmaj7, Cmaj7, Dm9, Cmaj7]
        step = 3.0
        k = 0
        while s + k * step < e:
            ch = seq[k % 4]
            add(music, s + k * step, pad(ch, min(step, e - s - k * step) + .4, 1.2, a=0.7, r=1.4), 0.5)
            add(music, s + k * step, sub(ch[0] - 12, step), 0.22)
            k += 1
        r2 = np.random.default_rng(8)
        tt = s + 0.3
        while tt < e - 0.5:
            ch = seq[int((tt - s) // step) % 4]
            add(music, tt, bell(int(r2.choice(ch)) + 24, 2.5), 0.06, pan=float(r2.uniform(-.7, .7)))
            tt += float(r2.choice([0.375, 0.75, 0.75, 1.125]))
    elif act == 5:  # tension: cluster drone + clock
        add(music, s, pad([45, 46, 52], dur + .3, 0.3, a=0.2, r=0.6), 0.5)
        add(music, s, sub(33, dur, r=0.4), 0.3)
        tt = s
        while tt < e:
            n = int(0.03 * SR)
            click = hp(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 200), 2500)
            add(music, tt, click, 0.18, pan=-.2 if int((tt - s) * 2) % 2 else .2)
            tt += 0.5
    elif act == 4:  # resolution: F G Am C, building
        seq = [F, G, Am, C]
        step = 2.2
        k = 0
        while s + k * step < e:
            ch = seq[k % 4]
            last = s + (k + 1) * step >= e
            add(music, s + k * step, pad(ch + [ch[2] + 12], min(step, e - s - k * step) + .3, 1.3, a=0.25, r=2.5 if last else 0.9), 0.55)
            add(music, s + k * step, sub(ch[0] - 12, step, r=2.5 if last else .8), 0.3)
            k += 1
        tt = s + 0.1
        i = 0
        while tt < e - 4.0:
            if i % 2 == 0:
                add(music, tt, kick(52, .5), 0.4)
            ch = seq[int((tt - s) // step) % 4]
            add(music, tt, pluck(ch[[2, 3, 4, 3][i % 4]] + 12, .6), 0.1, pan=[-.5, .5][i % 2])
            tt += 0.3
            i += 1

# ---------------- sfx ----------------
def noise(n):
    return rng.standard_normal(n)


def impact(big=False, low=False):
    dur = 2.8 if big else 1.6
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = (38 if low else 45) + 70 * np.exp(-tt * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (1.4 if big else 2.4))
    nz = lp(noise(n), 1800 if not low else 600) * np.exp(-tt * 9) * 0.9
    s = boom + nz
    if big:
        s += hp(noise(n), 5000) * np.exp(-tt * 1.5) * 0.25  # cymbal wash
    return np.tanh(s * 1.4)


def riser(dur=1.6):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    k = tt / dur
    x = noise(n)
    lo = lp(x, 900)
    hi = hp(x, 3000)
    s = lo * (1 - k) + hi * k
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * k ** 2) / SR) * 0.25
    return (s * 0.6 + tone) * k ** 2.2


def whoosh(dur=0.45):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    e = np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 2
    return lp(noise(n), 2500) * e


def swell(dur=1.3):
    n = int(dur * SR)
    k = np.arange(n) / n
    return lp(noise(n), 1200) * k ** 3 + np.sin(2 * np.pi * 110 * np.arange(n) / SR) * k ** 3 * 0.3


def tick_hit():
    return np.tanh(kick(70, .35) * 1.5 + hp(noise(int(.35 * SR)), 4000) * np.exp(-np.arange(int(.35 * SR)) / SR * 30) * 0.4)


for b in TL:
    s, d, kind, fx = b["start"], b["d"], b.get("kind", "text"), b.get("sfx", "")
    add(sfx, s - 0.05, whoosh(), 0.10, pan=float(rng.uniform(-.5, .5)))
    if fx == "impact":
        add(sfx, s, impact(), 0.55)
    elif fx == "impact_low":
        add(sfx, s, impact(low=True), 0.6)
    elif fx == "big":
        add(sfx, s, impact(big=True), 0.6)
    elif fx == "riser_impact":
        add(sfx, s - 1.6, riser(1.6), 0.35)
        add(sfx, s, impact(), 0.55)
    elif fx == "impact_late":
        add(sfx, s + 2.4, impact(), 0.55)
    elif fx == "swell":
        add(sfx, s - 0.9, swell(1.0), 0.25)
    if kind == "list":
        slot = d / len(b["words"])
        for i in range(len(b["words"])):
            add(sfx, s + i * slot, tick_hit(), 0.35, pan=[-.2, .2][i % 2])
    if kind == "stack":
        for i in range(len(b["items"])):
            add(sfx, s + .1 + i * .55, tick_hit(), 0.3)
    if kind == "progress":
        n = int(1.9 * SR)
        k = np.arange(n) / n
        add(sfx, s + .6, np.sin(2 * np.pi * np.cumsum(180 + 700 * k ** 2) / SR) * k * 0.5, 0.12)
    if kind == "chapter":
        add(sfx, s + .05, bell(57 + {1: 0, 2: 3, 3: 7}.get(b["act"], 0), 3), 0.12)
    if kind == "triad":
        for i, m in enumerate([69, 72, 76]):
            add(sfx, s + .2 + i * 1.25, bell(m, 4), 0.2, pan=[-.5, .5, 0][i])
            add(sfx, s + .2 + i * 1.25, kick(48, .5), 0.3)
        add(sfx, s + 4.3, impact(big=True), 0.5)
        for m in (57, 64, 69, 72, 76):
            add(sfx, s + 4.3, bell(m, 5), 0.07)
    if kind == "echo":
        r2 = np.random.default_rng(99)
        for i in range(11):
            r2.random(); r2.random(); r2.random()
            t0 = .3 + r2.random() * 1.8
            add(sfx, s + t0, whoosh(.3), 0.05, pan=float(r2.uniform(-.8, .8)))

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


music = lp(music, 7000)
mix = 0.62 * (music + 0.35 * reverb(music)) + sfx + 0.3 * reverb(sfx, 1.8, 3.0)
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
