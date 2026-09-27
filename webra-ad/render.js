// Renders index.html frame-by-frame and muxes with audio.wav -> out/webra_30s_1080x1920.mp4
// Usage: node render.js            (full video)
//        node render.js --stills 1.8,5.5,...   (PNG stills into out/stills)
const path = require('path'), fs = require('fs'), { spawn, execSync } = require('child_process');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'))); }
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const FPS = 30, DUR = 30, OUT = path.join(__dirname, 'out');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--disable-web-security', '--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, 'index.html') + '?render=1');
  await page.waitForFunction('window.READY===true');

  const si = process.argv.indexOf('--stills');
  if (si > 0) {
    fs.mkdirSync(path.join(OUT, 'stills'), { recursive: true });
    for (const t of process.argv[si + 1].split(',').map(Number)) {
      await page.evaluate(t => seek(t), t);
      await page.screenshot({ path: path.join(OUT, 'stills', `t${t.toFixed(2).padStart(5,"0")}.png`) });
    }
    await browser.close(); return;
  }

  const ff = spawn(FFMPEG, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(__dirname, 'audio.wav'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', path.join(OUT, 'webra_30s_1080x1920.mp4')],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < FPS * DUR; f++) {
    await page.evaluate(t => seek(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 90 === 0) console.log(`frame ${f}/${FPS * DUR}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
