"""混音（mix_ace）：48k；人声 50ms RMS 包络（> −38 dBFS 判为说话）；每条字幕内人声比音乐高约 10 dB（只压不抬），
闪避起 40ms / 释放 350ms，再做 300ms 平滑；句间音乐约 −2 dB；片尾卡音乐不低于 −1 dB；按 EV 合成轻音效。
输出未做响度标准化的 mix_raw.wav（之后两遍 loudnorm 到 −14 LUFS / −1 dBTP）。
用法：python mix.py vo.wav music_edit.wav page.json timings.json out.wav
"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt

vo_p, mu_p, page_p, tj, dst = sys.argv[1:6]
SR = 48000
def load(p):
    x, sr = sf.read(p, always_2d=True); x = x.astype(np.float32)
    if sr != SR: x = resample_poly(x, SR, sr, axis=0).astype(np.float32)
    return x
page = json.load(open(page_p, encoding='utf-8')); TM = json.load(open(tj, encoding='utf-8'))
N = int(page['dur'] * SR)
vo = load(vo_p).mean(1); vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
mu = load(mu_p)
if mu.shape[1] == 1: mu = np.repeat(mu, 2, 1)
mu = np.pad(mu, ((0, max(0, N - len(mu))), (0, 0)))[:N]
db = lambda v: 20 * np.log10(max(v, 1e-9))

# 人声：高通 + 轻压缩，语音段 RMS 定到 −18 dBFS
vo = sosfilt(butter(2, 70, 'high', fs=SR, output='sos'), vo)
H = int(0.05 * SR); nf = N // H
fr = lambda s: np.sqrt(np.mean(s[:nf * H].reshape(nf, H) ** 2, 1) + 1e-12)
venv = fr(vo); speak = 20 * np.log10(venv) > -38 + db(np.abs(vo).max())
vo *= 10 ** (-18 / 20) / np.sqrt(np.mean(venv[speak] ** 2))
venv = fr(vo); speak = 20 * np.log10(venv) > -38
# 音乐整体先放到 −20 dBFS RMS
menv = fr(mu.mean(1)); mu *= 10 ** (-20 / 20) / np.sqrt(np.mean(menv ** 2)); menv = fr(mu.mean(1))

t = (np.arange(nf) + 0.5) * H / SR
g = np.full(nf, 10 ** (-2 / 20))                      # 句间约 −2 dB
for a, b, _ in page['cues']:
    m = (t >= a) & (t < b)
    sp = m & speak
    if not sp.any(): continue
    vd = db(np.sqrt(np.mean(venv[sp] ** 2))); md = db(np.sqrt(np.mean(menv[m] ** 2)))
    g[m] = min(10 ** (-2 / 20), 10 ** ((vd - 10 - md) / 20))
end_t = TM[-1]['end'] + 0.1
g[t >= end_t] = np.maximum(g[t >= end_t], 10 ** (-1 / 20))
# 起 40ms / 释放 350ms 的单极点跟随，然后 300ms 平滑
fps = SR / H; aa = np.exp(-1 / (0.04 * fps)); ar = np.exp(-1 / (0.35 * fps))
gs = np.empty_like(g); cur = g[0]
for i, v in enumerate(g):
    c = aa if v < cur else ar; cur = c * cur + (1 - c) * v; gs[i] = cur
k = max(1, int(0.3 * fps)); gs = np.convolve(np.pad(gs, (k, k), 'edge'), np.ones(k) / k, 'same')[k:-k]
gain = np.interp(np.arange(N) / SR, t, gs).astype(np.float32)
mu *= gain[:, None]

# 音效（轻量合成，峰值对齐事件时刻）
rng = np.random.default_rng(7)
def tone(f0, f1, d, dec):
    n = int(d * SR); tt = np.arange(n) / SR; f = np.linspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec)
def noise(d, lo, hi, att, dec):
    n = int(d * SR); tt = np.arange(n) / SR
    s = sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), rng.standard_normal(n))
    return s * np.minimum(1, tt / att) * np.exp(-tt / dec)
def add(*a):
    n = max(len(v) for v in a); return sum(np.pad(v, (0, n - len(v))) for v in a)
SFX = {'tick': lambda: tone(2200, 1800, 0.05, 0.008) * 0.5,
       'pop': lambda: tone(900, 420, 0.12, 0.03) * 0.6,
       'whoosh': lambda: noise(0.6, 300, 3000, 0.35, 0.12) * 0.8,
       'stamp': lambda: add(tone(110, 55, 0.35, 0.08), noise(0.12, 200, 2000, 0.002, 0.03) * 0.5),
       'strike': lambda: noise(0.16, 1500, 6000, 0.01, 0.04) * 0.7,
       'pen': lambda: noise(0.7, 2500, 7000, 0.05, 0.4) * 0.25 * (1 + 0.6 * np.sin(np.arange(int(0.7 * SR)) / SR * 2 * np.pi * 9)),
       'drop': lambda: tone(320, 90, 0.25, 0.07) * 0.7,
       'chime': lambda: add(*[tone(f, f, 1.6, 0.5) * a for f, a in ((880, 0.5), (1320, 0.25), (1760, 0.12))])}
fx = np.zeros(N, np.float32)
for e in page['ev']:
    s = SFX.get(e['type']);
    if s is None: continue
    s = s().astype(np.float32); pk = int(np.argmax(np.abs(s))); i0 = int(e['t'] * SR) - pk
    if i0 < 0: s = s[-i0:]; i0 = 0
    s = s[:max(0, N - i0)]; fx[i0:i0 + len(s)] += s
fx *= 10 ** (-24 / 20) / max(1e-9, np.abs(fx).max()) * 4   # 音效峰值约 −12 dBFS，低于人声

mix = mu + (vo + fx)[:, None]
pk = np.abs(mix).max()
if pk > 0.98: mix *= 0.98 / pk
sf.write(dst, mix, SR, subtype='PCM_24')
spk = speak & (t < end_t)
print(f'混音完成 {N/SR:.1f}s；说话时音乐平均增益 {db(np.mean(gs[spk])):.1f} dB')
