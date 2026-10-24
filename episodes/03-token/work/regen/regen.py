"""重做 L08/L15：多试几个 seed，按同音字归一后的相似度选最佳，然后重拼 vo.wav / timings.json / voice_report.txt。"""
import sys, os, re, json, difflib, gc
from pathlib import Path
sys.path.insert(0, str(Path.home() / 'Movies/feynman03'))
import feynman03_make as M
import numpy as np
REDO = ['L08', 'L15']
SEEDS = [11, 23, 37, 51, 67, 79, 97, 113, 131, 149]
HOMO = str.maketrans({'他': '它', '她': '它', '锯': '句'})
norm = lambda s: M.strip(s).lower().translate(HOMO)
M.exec_imports(M.STACK / 'verify_speech.py', r'^(import\s+mlx|from\s+mlx|import\s+mlx_audio|from\s+mlx_audio)')
import mlx.core as mx
from mlx_audio.stt import load as stt_load
_load = M.__dict__.get('load_model') or globals().get('load_model')
if _load is None:
    from mlx_audio.tts.utils import load_model as _load
ref_wav = M.NARR / 'narrator.wav'
meta = json.loads((M.NARR / 'narrator.json').read_text(encoding='utf-8')) if (M.NARR / 'narrator.json').exists() else {}
ref_text = next((meta[k] for k in ('ref_text', 'text', 'transcript', 'reference_text') if isinstance(meta.get(k), str)), None)
asr = stt_load(str(M.STACK / 'models/Qwen3-ASR-1.7B-8bit'))
if not ref_text: ref_text = asr.generate(str(ref_wav), language='Chinese').text
tts = _load(str(M.STACK / 'models/Qwen3-TTS-1.7B-Base-bf16'))
rep = {}
for line in M.Path(M.OUT / 'voice_report.txt').read_text(encoding='utf-8').split('\n'):
    pass
results = {}
for lid, txt, pause in M.LINES:
    if lid not in REDO: continue
    best = None
    for seed in SEEDS:
        mx.random.seed(seed)
        parts = [r.audio.astype(mx.float32) for r in tts.generate(text=txt, language='Chinese', ref_audio=str(ref_wav), ref_text=ref_text, max_tokens=800)]
        x = M.trim(np.concatenate([np.array(p) for p in parts]).astype(np.float32), M.SR_OUT)
        tmp = M.OUT / 'lines' / f'{lid}_try.wav'; M.write_wav(tmp, x, M.SR_OUT)
        heard = asr.generate(str(tmp), language='Chinese').text
        sim = difflib.SequenceMatcher(None, M.strip(txt), M.strip(heard)).ratio()
        nsim = difflib.SequenceMatcher(None, norm(txt), norm(heard)).ratio()
        rate = M.nchars(txt) / max(0.1, len(x) / M.SR_OUT)
        ok = sim >= 0.92 and 2.8 <= rate <= 7.5
        nok = nsim >= 0.92 and 2.8 <= rate <= 7.5
        print(f'{lid} seed={seed} 相似度={sim:.3f} 同音归一={nsim:.3f} 语速={rate:.1f} 听：{heard}', flush=True)
        cand = (ok, nok, nsim, -abs(rate - 4.6), x, heard, seed, rate, sim)
        if best is None or cand[:4] > best[:4]: best = cand
        if ok: break
    (M.OUT / 'lines' / f'{lid}_try.wav').unlink(missing_ok=True)
    ok, nok, nsim, _, x, heard, seed, rate, sim = best
    M.write_wav(M.OUT / 'lines' / f'{lid}.wav', x, M.SR_OUT)
    mark = '✓' if ok else ('✓(同音)' if nok else '⚠️')
    results[lid] = f'{mark} {lid} 相似度{sim:.3f} 同音归一{nsim:.3f} 语速{rate:.1f} seed{seed}（重做）\n   稿：{txt}\n   听：{heard}'
del tts, asr; gc.collect()
# 重拼
rpt = M.Path(M.OUT / 'voice_report.txt').read_text(encoding='utf-8')
blocks = re.split(r'\n(?=[✓⚠])', rpt)
blocks = [results.get(re.search(r'L\d\d', b).group(0), b) for b in blocks]
t = M.LEAD_IN; segs = [np.zeros(int(M.LEAD_IN * M.SR_OUT), np.float32)]; timings = []
for lid, txt, pause in M.LINES:
    x, sr = M.read_wav(M.OUT / 'lines' / f'{lid}.wav')
    timings.append({'id': lid, 'text': txt, 'start': round(t, 3), 'end': round(t + len(x) / sr, 3)})
    segs += [x, np.zeros(int(pause * sr), np.float32)]; t += len(x) / sr + pause
vo = np.concatenate(segs); vo = vo / max(1e-6, np.abs(vo).max()) * 0.5
M.write_wav(M.OUT / 'vo.wav', vo, M.SR_OUT)
(M.OUT / 'timings.json').write_text(json.dumps(timings, ensure_ascii=False, indent=1), encoding='utf-8')
(M.OUT / 'voice_report.txt').write_text('\n'.join(blocks), encoding='utf-8')
print(f'重拼完成：{len(vo)/M.SR_OUT:.1f}s')
