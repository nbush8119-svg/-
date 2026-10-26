"""测拍（ana）+ 按小节剪接（edit_music）：把配乐高潮对到关键台词，结尾 1.8 秒淡出。
用法：python music_edit.py cand.wav timings.json 目标句ID(L15/L17/auto) 总时长 输出.wav
"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

src, tj, target, dur, dst = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
x, sr = sf.read(src, always_2d=True); x = x.astype(np.float32)
mono = x.mean(1)
TM = {r['id']: r for r in json.load(open(tj, encoding='utf-8'))}

def frames(sig, hop):
    n = len(sig) // hop; return sig[:n * hop].reshape(n, hop)

# ---- ana：频谱通量 → 拍速/相位；120Hz 以下能量 → 强拍 ----
hop = 512; win = 2048
spec = np.abs(np.fft.rfft(np.lib.stride_tricks.sliding_window_view(np.pad(mono, (0, win)), win)[::hop] * np.hanning(win), axis=1))
flux = np.maximum(0, np.diff(np.log1p(spec), axis=0)).sum(1); flux = np.r_[0, flux]; flux -= flux.mean()
fr = sr / hop
best = None
for bpm in np.arange(80, 100, 0.02):
    per = 60 / bpm * fr
    for ph in np.linspace(0, per, 48, endpoint=False):
        idx = np.round(np.arange(ph, len(flux) - 1, per)).astype(int)
        s = flux[idx].mean()
        if best is None or s > best[0]: best = (s, bpm, ph / fr)
_, BPM, PH = best
beat = 60 / BPM
low = sosfilt(butter(4, 120, 'low', fs=sr, output='sos'), mono)
beats = np.arange(PH, len(mono) / sr - beat, beat)
le = np.array([np.sqrt(np.mean(low[int(b * sr):int((b + beat * 0.25) * sr)] ** 2)) for b in beats])
down = max(range(4), key=lambda k: le[k::4].mean())
bars = beats[down::4]; bar = 4 * beat
rms = np.array([np.sqrt(np.mean(mono[int(b * sr):int((b + bar) * sr)] ** 2)) for b in bars])
sm = np.convolve(rms, np.ones(3) / 3, 'same')
# 高潮：平滑后首次达到 90% 最大值、且比前两小节明显抬升的小节
cands = [i for i in range(2, len(bars)) if sm[i] >= 0.9 * sm.max()]
jump = max(cands[:4] or [int(np.argmax(sm))], key=lambda i: rms[i] - rms[max(0, i - 2)])
climax = bars[jump]
print(f'拍速 {BPM:.2f} BPM，首个强拍 {bars[0]:.2f}s，小节 {bar:.2f}s，高潮在第 {jump} 小节 {climax:.2f}s')

# ---- edit_music：在前奏后整小节删/补，使高潮落到目标台词 ----
tgts = ['L15', 'L17'] if target == 'auto' else [target]
def plan(tid):
    want = TM[tid]['start'] - 0.15   # 高潮落拍略早于开口
    n = int(round((climax - want) / bar)); return abs(climax - n * bar - want), n, tid, want
err, n, tid, want = min(plan(t) for t in tgts)
sl = lambda a, b: x[int(a * sr):int(b * sr)]
xf = int(0.03 * sr)
def join(a, b):
    if len(a) < xf or len(b) < xf: return np.concatenate([a, b])
    k = np.linspace(0, np.pi / 2, xf)[:, None]
    return np.concatenate([a[:-xf], a[-xf:] * np.cos(k) + b[:xf] * np.sin(k), b[xf:]])
cut0 = bars[2] if len(bars) > 2 else bars[0]
if n > 0:   # 删掉前奏后的 n 个小节
    y = join(sl(0, cut0), sl(cut0 + n * bar, len(mono) / sr))
elif n < 0: # 重复前奏小节
    y = sl(0, cut0)
    for k in range(-n): y = join(y, sl(bars[0] + (k % 2) * bar, bars[0] + (k % 2 + 1) * bar))
    y = join(y, sl(cut0, len(mono) / sr))
else: y = x
new_climax = climax - n * bar
need = int(dur * sr)
if len(y) < need: y = np.concatenate([y, np.zeros((need - len(y), y.shape[1]), np.float32)])
y = y[:need].copy()
fo = int(1.8 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
sf.write(dst, y, sr)
json.dump({'bpm': round(BPM, 2), 'bar': round(bar, 3), 'climax_src': round(climax, 2), 'bars_shift': n, 'target': tid,
           'climax_new': round(new_climax, 2), 'target_time': round(want + 0.15, 2), 'err': round(err, 2)},
          open(dst.replace('.wav', '.json'), 'w'), ensure_ascii=False)
print(f'高潮对到 {tid}（{want + 0.15:.2f}s），整小节移动 {n}，新高潮 {new_climax:.2f}s，误差 {err:.2f}s，音乐时长 {len(y)/sr:.1f}s')
