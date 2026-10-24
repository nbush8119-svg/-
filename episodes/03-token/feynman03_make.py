"""费曼卡片03 · Token 词元（B7.1） —— 本地配音（Qwen3-TTS 复用系列旁白音色）+ ASR 回检 + 按配音算 BPM + ACE-Step 配乐 3 首。
输出：OUT_DIR  vo.wav  timings.json  voice_report.txt  lines/  music/cand_*.wav
只想重做配乐：加环境变量 MUSIC_ONLY=1
"""
import os, re, sys, gc, json, time, difflib, subprocess, wave
from pathlib import Path
import numpy as np

STACK = Path(os.environ.get('AUDIO_STACK', Path.home() / 'Documents/ChatGPT/kindle/audio-stack'))
NARR = Path(os.environ.get('NARRATOR_DIR', Path.home() / '高性价比人生指南-视频工程/voices'))
OUT = Path(os.environ.get('OUT_DIR', STACK / 'out' / 'feynman03')); (OUT / 'lines').mkdir(parents=True, exist_ok=True); (OUT / 'music').mkdir(exist_ok=True)
SR_OUT = 24000

# (id, 文本, 句后停顿秒)
LINES = [
 ('L01', '你跟AI聊天，它是按字收费的吗？不是。', 0.45),
 ('L02', '它按一个你可能天天见、却说不清的单位收费：Token，中文叫词元。', 0.45),
 ('L03', '用了一年AI，大多数人还是说不上来，Token到底是什么。', 0.40),
 ('L04', '今天用费曼学习法，四步把Token讲透。', 0.70),
 ('L05', '第一步，选一个概念，写在纸的最上方：Token，词元。', 0.70),
 ('L06', '第二步，讲给一个十二岁的孩子听，不许用术语。', 0.45),
 ('L07', 'AI读一句话，既不是一个字一个字地读，也不是一整句一口吞。', 0.35),
 ('L08', '它先把句子切成一小块一小块。每一块，就是一个Token。', 0.45),
 ('L09', '比如，我爱吃火锅，可能被切成三块：我，爱吃，火锅。', 0.45),
 ('L10', '每一块再换成一个编号。AI从头到尾看到的，其实是一串数字。', 0.45),
 ('L11', '它回答你，也是一块一块往外蹦：猜下一块，再猜下一块。', 0.45),
 ('L12', '所以AI收多少钱，按Token算；它能记住多长的对话，也按Token算。', 0.70),
 ('L13', '第三步，找卡住的地方。最常见的误会：AI读字，跟我们一样。', 0.50),
 ('L14', '其实不一样。你让它数一个长长的英文单词里有几个某个字母，它经常数错。', 0.40),
 ('L15', '不是它笨，是它根本没看见字母。它看见的，是切好的一整块。', 0.40),
 ('L16', '就像你拿到的是一袋一袋的米，却有人问你，一共有几粒。', 0.85),
 ('L17', '第四步，简化成一句话：Token，就是AI眼里的一个字。', 0.55),
 ('L18', '这张卡挂在世界怎么运转这根主干上。往下还能长出一张：AI到底是怎么猜下一个字的。', 0.55),
 ('L19', '今晚就打开你常用的AI，让它数一数一个长单词里的字母，看它会不会数错。', 0.30),
 ('L20', '评论区告诉我。', 0.60),
 ('L21', '费曼学习法卡片，第三张。我们下一张见。', 0.0),
]
LEAD_IN = 0.25

def strip(s): return re.sub(r'[^一-鿿0-9A-Za-z]', '', s)
def nchars(s): return len(re.findall(r'[一-鿿]', s))
def write_wav(p, x, sr):
    x = np.clip(np.asarray(x, np.float32), -1, 1)
    with wave.open(str(p), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype('<i2').tobytes())
def read_wav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768, w.getframerate()
def trim(x, sr, th=0.01):
    idx = np.nonzero(np.abs(x) > th)[0]
    if not len(idx): return x
    a = max(0, idx[0] - int(0.03 * sr)); b = min(len(x), idx[-1] + int(0.08 * sr))
    return x[a:b]

def exec_imports(pyfile, patt):
    for line in Path(pyfile).read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if re.match(patt, s):
            exec(s, globals())

def make_voice():
    exec_imports(STACK / 'verify_speech.py', r'^(import\s+mlx|from\s+mlx|import\s+mlx_audio|from\s+mlx_audio)')
    import mlx.core as mx
    from mlx_audio.stt import load as stt_load
    _load = globals().get('load_model')
    if _load is None:
        from mlx_audio.tts.utils import load_model as _load
    # 旁白参考
    ref_wav = NARR / 'narrator.wav'
    meta = json.loads((NARR / 'narrator.json').read_text(encoding='utf-8')) if (NARR / 'narrator.json').exists() else {}
    ref_text = next((meta[k] for k in ('ref_text', 'text', 'transcript', 'reference_text') if isinstance(meta.get(k), str)), None)
    asr = stt_load(str(STACK / 'models/Qwen3-ASR-1.7B-8bit'))
    if not ref_text:
        ref_text = asr.generate(str(ref_wav), language='Chinese').text
    print('旁白参考：', ref_wav, '|', ref_text[:30], flush=True)
    tts = _load(str(STACK / 'models/Qwen3-TTS-1.7B-Base-bf16'))

    report, clips = [], []
    for lid, txt, pause in LINES:
        best = None
        for attempt, seed in enumerate([11, 23, 37, 51]):
            mx.random.seed(seed)
            parts = [r.audio.astype(mx.float32) for r in tts.generate(text=txt, language='Chinese', ref_audio=str(ref_wav), ref_text=ref_text, max_tokens=800)]
            sr = SR_OUT
            x = np.concatenate([np.array(p) for p in parts]).astype(np.float32)
            x = trim(x, sr)
            tmp = OUT / 'lines' / f'{lid}_try.wav'; write_wav(tmp, x, sr)
            heard = asr.generate(str(tmp), language='Chinese').text
            sim = difflib.SequenceMatcher(None, strip(txt), strip(heard)).ratio()
            rate = nchars(txt) / max(0.1, len(x) / sr)
            ok = sim >= 0.92 and 2.8 <= rate <= 7.5
            cand = (ok, sim, -abs(rate - 4.6), x, heard, seed, rate)
            if best is None or cand[:3] > best[:3]: best = cand
            print(f'{lid} 第{attempt+1}次 seed={seed} 相似度={sim:.3f} 语速={rate:.1f}字/秒 {"✓" if ok else "×"}', flush=True)
            if ok: break
        ok, sim, _, x, heard, seed, rate = best
        write_wav(OUT / 'lines' / f'{lid}.wav', x, SR_OUT); (OUT / 'lines' / f'{lid}_try.wav').unlink(missing_ok=True)
        clips.append((lid, txt, pause, x))
        report.append(f'{"✓" if ok else "⚠️"} {lid} 相似度{sim:.3f} 语速{rate:.1f} seed{seed}\n   稿：{txt}\n   听：{heard}')
    del tts, asr; gc.collect(); mx.clear_cache()

    # 拼接 + 时间轴
    t = LEAD_IN; segs = [np.zeros(int(LEAD_IN * SR_OUT), np.float32)]; timings = []
    for lid, txt, pause, x in clips:
        timings.append({'id': lid, 'text': txt, 'start': round(t, 3), 'end': round(t + len(x) / SR_OUT, 3)})
        segs += [x, np.zeros(int(pause * SR_OUT), np.float32)]; t += len(x) / SR_OUT + pause
    vo = np.concatenate(segs); vo = vo / max(1e-6, np.abs(vo).max()) * 0.5   # 峰值约 −6 dBFS
    write_wav(OUT / 'vo.wav', vo, SR_OUT)
    (OUT / 'timings.json').write_text(json.dumps(timings, ensure_ascii=False, indent=1), encoding='utf-8')
    (OUT / 'voice_report.txt').write_text('\n'.join(report), encoding='utf-8')
    print(f'\n配音完成：{len(vo)/SR_OUT:.1f} 秒；⚠️ 句数 {sum(r.startswith("⚠️") for r in report)}（见 voice_report.txt）', flush=True)
    return timings

def pick_bpm(timings):
    key = {r['id']: r['start'] for r in timings}
    K = [key[i] for i in ('L04', 'L05', 'L06', 'L13', 'L15', 'L17')]; W = [1.5, 2, 2, 2, 2.5, 3]
    best = None
    for bpm in np.arange(84, 100.01, 0.05):
        beat = 60 / bpm
        for off in np.arange(0, beat, 0.01):
            d = [min(abs(((k - off) / beat) - round((k - off) / beat)), 0.5) * beat for k in K]
            s = sum(w * x * x for w, x in zip(W, d))
            if best is None or s < best[0]: best = (s, round(float(bpm), 2), round(float(off), 3))
    return best[1], best[2]

MUSIC_SRC = r'''
import os, sys, re, glob, shutil, time
from pathlib import Path
STACK = Path(sys.argv[1]); BPM = float(sys.argv[2]); DUR = int(float(sys.argv[3])); OUT = Path(sys.argv[4])
REPO = STACK / 'ACE-Step-1.5'; os.chdir(REPO); sys.path.insert(0, str(REPO))
for line in (STACK / 'verify_music.py').read_text(encoding='utf-8').splitlines():
    s = line.strip()
    if re.match(r'^(from\s+acestep[\w\.]*\s+import|import\s+acestep)', s): exec(s)
CAPTION = ("Curious futuristic cinematic electronic instrumental for an AI explainer short video. "
  "Opens with crisp glitchy digital plucks and a felt piano motif, clicking data-stream pulse, deep sub bass, "
  "pulsing arpeggiated analog synth, soft heartbeat kick, warm pads and rising strings. "
  "Thoughtful and curious at first, gradually building momentum, a tense suspended moment, "
  "then an emotional, uplifting climax with wide strings and driving drums, ending on a calm, open piano chord. "
  "Premium, polished, spacious mix that leaves room for a male voiceover.")
dit = AceStepHandler(); dit.initialize_service(project_root=str(REPO), config_path=os.environ.get('MODEL', 'acestep-v15-xl-sft'), device='mps',
      use_flash_attention=False, compile_model=False, offload_to_cpu=False, use_mlx_dit=True)
llm = LLMHandler(); llm.initialize(checkpoint_dir=str(REPO / 'checkpoints'), lm_model_path='acestep-5Hz-lm-1.7B', backend='mlx', device='mps')
for seed in (3301, 5503, 7705):
    tmp = OUT / f'_tmp_{seed}'; tmp.mkdir(exist_ok=True); t1 = time.time()
    generate_music(dit, llm, GenerationParams(caption=CAPTION, lyrics='[Instrumental]', instrumental=True, bpm=int(round(BPM)),
                   keyscale='D minor', duration=DUR, inference_steps=int(os.environ.get('STEPS', '48')), seed=seed, thinking=False),
                   GenerationConfig(batch_size=1, use_random_seed=False, seeds=[seed], audio_format='wav'), save_dir=str(tmp))
    w = sorted(glob.glob(str(tmp / '**' / '*.wav'), recursive=True), key=os.path.getmtime)
    if w: shutil.move(w[-1], OUT / f'cand_{seed}.wav'); shutil.rmtree(tmp, ignore_errors=True); print(f'配乐 cand_{seed}.wav 完成 {time.time()-t1:.0f}s', flush=True)
    else: print(f'seed {seed} 没有输出', flush=True)
'''

if __name__ == '__main__':
    t0 = time.time()
    if os.environ.get('MUSIC_ONLY'):
        timings = json.loads((OUT / 'timings.json').read_text(encoding='utf-8'))
    else:
        timings = make_voice()
    bpm, off = pick_bpm(timings)
    total = timings[-1]['end'] + 4.5
    (OUT / 'music' / 'bpm.json').write_text(json.dumps({'bpm': bpm, 'offset': off, 'duration': total}), encoding='utf-8')
    print(f'配乐速度 {bpm} BPM（拍点偏移 {off}s），时长 {total:.0f}s', flush=True)
    ms = OUT / 'music' / '_gen.py'; ms.write_text(MUSIC_SRC, encoding='utf-8')
    subprocess.run([str(STACK / 'ACE-Step-1.5/.venv/bin/python'), str(ms), str(STACK), str(round(bpm)), str(total + 6), str(OUT / 'music')], check=False)
    print(f'\n全部完成，用时 {time.time()-t0:.0f}s。文件夹：{OUT}')
    (OUT / 'DONE').write_text('ok')
