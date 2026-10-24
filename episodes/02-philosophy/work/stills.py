import sys, os, base64
from playwright.sync_api import sync_playwright
url='file://'+os.path.expanduser('~/Movies/feynman02/kit/index.html'); out=sys.argv[1]; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--font-render-hinting=none']); pg=b.new_page(viewport={'width':1080,'height':1920})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: m.type=='error' and errs.append(m.text))
    pg.goto(url); pg.wait_for_function('window.READY===true',timeout=60000)
    ts=pg.evaluate("""(()=>{const r={};for(const x of TIMINGS)r[x.id]=[x.start,x.end];return r})()""")
    pick=[]
    for k,(s,e) in ts.items(): pick.append(round((s+e)/2+0.3,2))
    pick+= [round(ts['L04'][1]+0.9,2), round(ts['L17'][1]+0.8,2), round(ts['L22'][0]+2.5,2)]
    for t in sorted(pick):
        d=pg.evaluate(f"(()=>{{render({t});return document.getElementById('c').toDataURL('image/jpeg',0.85)}})()")
        open(f'{out}/s_{t:06.2f}.jpg','wb').write(base64.b64decode(d.split(',',1)[1]))
    print('errors:',errs[:5]); print('dur',pg.evaluate('DUR'))
    b.close()
