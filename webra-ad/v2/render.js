// v2 renderer: 3-sample motion blur (180° shutter) -> 30 fps H.264 + AAC.
// node render.js | node render.js --stills 1.5,6,...
const path=require('path'),fs=require('fs'),{spawn,execSync}=require('child_process');
let chromium;try{({chromium}=require('playwright'))}catch{({chromium}=require(path.join(execSync('npm root -g').toString().trim(),'playwright')))}
const FFMPEG=process.env.FFMPEG||'ffmpeg',FPS=30,DUR=30,SUB=3,OUT=path.join(__dirname,'out');
(async()=>{
  fs.mkdirSync(OUT,{recursive:true});
  const browser=await chromium.launch({args:['--allow-file-access-from-files']});
  const page=await browser.newPage({viewport:{width:1080,height:1920}});
  page.on('pageerror',e=>console.error('PAGE ERROR',e.message));
  await page.goto('file://'+path.join(__dirname,'index.html')+'?render=1');
  await page.waitForFunction('window.READY===true');
  if(await page.evaluate('!!window.LOGO_MISSING'))console.warn('WARNING: brand/logo.svg|png not found — placeholder used');
  const si=process.argv.indexOf('--stills');
  if(si>0){fs.mkdirSync(path.join(OUT,'stills'),{recursive:true});
    for(const t of process.argv[si+1].split(',').map(Number)){await page.evaluate(t=>seek(t),t);await page.screenshot({path:path.join(OUT,'stills',`t${t.toFixed(2).padStart(5,'0')}.png`)})}
    await browser.close();return}
  const ff=spawn(FFMPEG,['-y','-f','image2pipe','-framerate',String(FPS*SUB),'-c:v','mjpeg','-i','-','-i',path.join(__dirname,'audio.wav'),
    '-vf',`tmix=frames=${SUB},framestep=${SUB}`,'-r',String(FPS),'-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-profile:v','high',
    '-c:a','aac','-b:a','256k','-shortest','-movflags','+faststart',path.join(OUT,'webra_v2_ka_1080x1920.mp4')],{stdio:['pipe','inherit','inherit']});
  for(let f=0;f<FPS*DUR;f++){
    for(let s=0;s<SUB;s++){ // samples spread over half a frame, centred on the frame time
      const t=(f+(s-(SUB-1)/2)*0.5/SUB)/FPS;
      await page.evaluate(t=>seek(t),Math.max(0,t));
      const buf=await page.screenshot({type:'jpeg',quality:95});
      if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
    }
    if(f%90===0)console.log(`frame ${f}/${FPS*DUR}`);
  }
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await browser.close();
})();
