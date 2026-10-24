"""把 timings.json 写成 index.html 读取的 timings.js。
没有 timings.json 时按 4.6 字/秒 + 稿中停顿估一个时间轴（只用于搭画面框架）。
用法：python make_timings_js.py [timings.json] [music_seed]
"""
import sys, json, re, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mk', HERE.parent / 'feynman02_make.py')
src = (HERE.parent / 'feynman02_make.py').read_text(encoding='utf-8')
LINES = eval(re.search(r'LINES = (\[.*?\n\])', src, re.S).group(1))

src_json = Path(sys.argv[1]) if len(sys.argv) > 1 else None
seed = sys.argv[2] if len(sys.argv) > 2 else ''
if src_json and src_json.exists():
    tim = json.loads(src_json.read_text(encoding='utf-8')); est = False
else:
    t, tim = 0.25, []
    for lid, txt, pause in LINES:
        d = len(re.findall(r'[一-鿿]', txt)) / 4.6 + 0.12 * len(re.findall(r'[，、：；]', txt)) + 0.2 * len(re.findall(r'[？。！]', txt[:-1]))
        tim.append({'id': lid, 'text': txt, 'start': round(t, 3), 'end': round(t + d, 3)}); t += d + pause
    est = True
meta = {'estimated': est, 'music_seed': seed}
(HERE / 'timings.js').write_text('window.TIMINGS=' + json.dumps(tim, ensure_ascii=False) + ';\nwindow.META=' + json.dumps(meta, ensure_ascii=False) + ';\n', encoding='utf-8')
print(('估算' if est else '实测') + f'时间轴：{len(tim)} 句，口播到 {tim[-1]["end"]:.1f}s')
