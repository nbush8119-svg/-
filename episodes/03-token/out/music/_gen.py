
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
