"""费曼卡片05 · 机器学习（B7.2） —— 本地配音（Qwen3-TTS 复用系列旁白音色）+ ASR 回检 + 按配音算 BPM + ACE-Step 配乐 3 首。
输出：OUT_DIR  vo.wav  timings.json  voice_report.txt  lines/  music/cand_*.wav
只想重做配乐：加环境变量 MUSIC_ONLY=1
"""
import os, re, sys, gc, json, time, difflib, subprocess, wave
from pathlib import Path
import numpy as np

STACK = Path(os.environ.get('AUDIO_STACK', Path.home() / 'Documents/ChatGPT/kindle/audio-stack'))
NARR = Path(os.environ.get('NARRATOR_DIR', Path.home() / '高性价比人生指南-视频工程/voices'))
OUT = Path(os.environ.get('OUT_DIR', STACK / 'out' / 'feynman05')); (OUT / 'lines').mkdir(parents=True, exist_ok=True); (OUT / 'music').mkdir(exist_ok=True)
SR_OUT = 24000

# (id, 文本, 句后停顿秒)
LINES = [
 ('L01', '机器学习，这四个字你天天听。可它到底是什么？', 0.50),
 ('L02', '先看看别人怎么说。有人说，它是让电脑像人一样思考。', 0.35),
 ('L03', '有人说，它就是一堆数学公式。还有人说，它是用数据练出来的程序。', 0.40),
 ('L04', '都沾点边，又都没说到点子上。我自己琢磨下来，是这样的：', 0.40),
 ('L05', '机器学习，其实是在找一个函数：一头放进问题，另一头出来答案。', 0.40),
 ('L06', '以前，这个函数是人一条一条写出来的规则。机器学习反过来：人只给例子和答案，让电脑在成千上万种可能里一遍遍试，挑出最对得上的那一个。', 0.70),
 ('L07', '我觉得讲透了，就去讲给楼下卖菜的王大姐听。', 0.40),
 ('L08', '王大姐没读过多少书。她听完，问了我两句。', 0.35),
 ('L09', '第一句：函数是个啥？', 0.35),
 ('L10', '第二句：电脑把答案都记住，不就行了吗？', 0.60),
 ('L11', '这两问，我一句都没答好。我才发现，我没讲透。', 0.50),
 ('L12', '我回去又想了想，换了一件她天天在做的事来讲。', 0.40),
 ('L13', '大姐，你挑西瓜，拍一拍，看一看，就知道好不好。你心里那套判断，就是一个函数：瓜放进去，好坏出来。', 0.40),
 ('L14', '这套判断不是谁教你的规则。是你拍过成千上万个瓜，切开对答案，错了就改一点，慢慢练出来的。', 0.50),
 ('L15', '再说记答案。假如你只见过三个好瓜，一个青，一个黑，一个白，根蒂都是卷的。', 0.35),
 ('L16', '死记的人会说：青的黑的白的才是好瓜。来个金黄的，他就不认了。', 0.35),
 ('L17', '会找规律的人会说：根蒂卷的是好瓜。金黄的，也挑得准。', 0.40),
 ('L18', '机器学习要的是后一种：没见过的瓜也挑得准，才算学会。', 0.70),
 ('L19', '王大姐又问：那它要是只拍过地里的瓜，到了超市，不就看走眼了？', 0.40),
 ('L20', '对。它学到的，只是它见过的那些瓜里的规律。例子偏了，它就学偏了。', 0.70),
 ('L21', '所以我重新写下这张卡：机器学习，就是让电脑从一堆对过答案的例子里，练出一套对新情况也管用的判断。', 0.70),
 ('L22', '留个话题：你身上哪个本事，也是这样一边试、一边对答案练出来的？评论区聊聊。', 0.60),
 ('L23', '下一张卡，讲我用的这套方法本身：费曼学习法。', 0.40),
 ('L24', '费曼学习法卡片，第五张。我们下一张见。', 0.00),
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
    K = [key[i] for i in ('L04', 'L07', 'L09', 'L12', 'L18', 'L21')]; W = [1.5, 2, 2, 2, 2.5, 3]
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
CAPTION = ("Warm, curious cinematic electronic instrumental for a machine learning explainer short video. "
  "Opens with a gentle felt piano motif and soft music-box plucks, like a child learning, light ticking data pulse, deep sub bass, "
  "evolving arpeggiated synth that slowly gets more confident, soft heartbeat kick, warm pads and rising strings. "
  "Thoughtful and curious at first, gradually building momentum, a tense suspended moment, "
  "then an emotional, uplifting climax with wide strings and driving drums, ending on a calm, open piano chord. "
  "Premium, polished, spacious mix that leaves room for a male voiceover.")
dit = AceStepHandler(); dit.initialize_service(project_root=str(REPO), config_path=os.environ.get('MODEL', 'acestep-v15-xl-sft'), device='mps',
      use_flash_attention=False, compile_model=False, offload_to_cpu=False, use_mlx_dit=True)
llm = LLMHandler(); llm.initialize(checkpoint_dir=str(REPO / 'checkpoints'), lm_model_path='acestep-5Hz-lm-1.7B', backend='mlx', device='mps')
for seed in (5501, 5512, 5523):
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
