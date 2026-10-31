// Usage:
//   node render.mjs frames <out.mp4>            -> full video (no audio)
//   node render.mjs stills <outdir> t1 t2 ...   -> PNG previews at given times
import { createRequire } from 'module';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const TL = JSON.parse(fs.readFileSync(path.join(here, 'timeline.json'), 'utf8'));
const FPS = 30;

const [, , mode, out, ...rest] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.addInitScript(tl => { window.TL = tl; }, TL);
await page.goto('file://' + path.join(here, 'index.html'));
await page.evaluate(async () => {
  const fams = ['200 20px Inter', '400 20px Inter', '800 20px Inter', '400 20px Bebas', 'italic 400 20px Playfair', 'italic 700 20px Playfair'];
  await Promise.all(fams.map(f => document.fonts.load(f, 'ÁÉÍÓÚÑáéíóúñ¿¡«»…')));
});
const total = await page.evaluate(() => window.TOTAL);
console.log('total seconds', total.toFixed(2));

if (mode === 'stills') {
  fs.mkdirSync(out, { recursive: true });
  for (const t of rest.map(Number)) {
    const d = await page.evaluate(t => window.frameJPEG(t, .9), t);
    fs.writeFileSync(path.join(out, `t${t.toFixed(2).padStart(6, '0')}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
  }
} else {
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.ceil(total * FPS);
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    const d = await page.evaluate(t => window.frameJPEG(t, .95), f / FPS);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
}
await browser.close();
