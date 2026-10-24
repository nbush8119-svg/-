const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--font-render-hinting=none']});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/cover.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({path:__dirname+'/cover.png'});await b.close();})();
