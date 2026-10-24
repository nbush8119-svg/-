const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--font-render-hinting=none']});const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const v of process.argv.slice(2)){await p.goto('file://'+__dirname+'/cover.html#'+v);await p.reload();await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.screenshot({path:__dirname+'/v'+v+'.png'});}
await b.close();})();
