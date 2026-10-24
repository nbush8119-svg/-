"""从画面页面导出 DUR / CUES / EV（音效事件），写 work/page.json 和成片字幕 out/feynman02.srt。"""
import os, json, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + os.path.join(HERE, 'index.html')); pg.wait_for_function('window.READY===true', timeout=60000)
    d = pg.evaluate('({dur:window.DUR,cues:window.CUES,ev:window.EV})'); b.close()
if errs: sys.exit('页面报错：' + '; '.join(errs))
json.dump(d, open(os.path.join(ROOT, 'work', 'page.json'), 'w'), ensure_ascii=False, indent=1)
f = lambda t: f'{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(round(t%1*1000))%1000:03d}'
srt = [f'{i+1}\n{f(max(0,a))} --> {f(b)}\n{s}\n' for i, (a, b, s) in enumerate(d['cues'])]
open(os.path.join(ROOT, 'out', 'feynman02.srt'), 'w', encoding='utf-8').write('\n'.join(srt))
print(f"DUR {d['dur']:.2f}s  字幕 {len(d['cues'])} 条  音效 {len(d['ev'])} 个")
