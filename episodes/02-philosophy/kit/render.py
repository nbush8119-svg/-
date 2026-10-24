import sys, base64, os, math
from multiprocessing import Process
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'file://' + os.path.join(HERE, os.environ.get('PAGE', 'index.html'))
FPS = 30

def page_ctx(p):
    b = p.chromium.launch(args=['--font-render-hinting=none'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(URL)
    pg.wait_for_function('window.READY===true', timeout=60000)
    return b, pg

def grab(pg, t, path, q=0.9):
    data = pg.evaluate(f"(()=>{{render({t});return document.getElementById('c').toDataURL('image/jpeg',{q});}})()")
    with open(path, 'wb') as f:
        f.write(base64.b64decode(data.split(',', 1)[1]))

def worker(start, end, outdir):
    with sync_playwright() as p:
        b, pg = page_ctx(p)
        for i in range(start, end):
            grab(pg, i / FPS, os.path.join(outdir, f'f{i:05d}.jpg'))
        b.close()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        times = [float(x) for x in sys.argv[3:]]
        with sync_playwright() as p:
            b, pg = page_ctx(p)
            for t in times:
                grab(pg, t, os.path.join(outdir, f's_{t:06.2f}.jpg'), 0.92)
            b.close()
    elif mode == 'frames':
        outdir = sys.argv[2]; nw = int(sys.argv[3]); os.makedirs(outdir, exist_ok=True)
        with sync_playwright() as p:
            b, pg = page_ctx(p); dur = pg.evaluate('window.DUR'); b.close()
        n = int(math.ceil(dur * FPS))
        chunk = math.ceil(n / nw)
        ps = [Process(target=worker, args=(k * chunk, min(n, (k + 1) * chunk), outdir)) for k in range(nw)]
        [x.start() for x in ps]; [x.join() for x in ps]
        print('frames', n)
    elif mode == 'range':
        outdir, a, b, nw = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        chunk = math.ceil((b - a) / nw)
        ps = [Process(target=worker, args=(a + k * chunk, min(b, a + (k + 1) * chunk), outdir)) for k in range(nw)]
        [x.start() for x in ps]; [x.join() for x in ps]
        print('frames', a, b)
