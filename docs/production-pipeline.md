# 生产流水线：从口播稿到成片

以 02 哲学为范例（`episodes/02-philosophy/`）。所有模型推理在用户的 Mac 上本地跑（Apple Silicon，MLX）。

## 0. 工程目录约定

每集一个目录，Mac 上放在 `~/Movies/feynmanNN/`，仓库里是 `episodes/NN-<slug>/`，结构一致：

```
feynmanNN_make.py   口播稿 LINES + 配音 + 回检 + 算 BPM + 配乐候选
kit/                画面与后期脚本
  index.html        画面：Canvas 2D，window.render(t) 纯函数，读 timings.js
  timings.js        由 make_timings_js.py 生成
  fonts/            Noto CJK（不入库，scripts/fetch_fonts.sh 下载）
  make_timings_js.py, music_edit.py, dump.py, mix.py, loudnorm.py, render.py
out/                交付物：vo.wav, timings.json, voice_report.txt, music/cand_*.wav, *.srt, CREDITS.txt, 成片 mp4
work/               中间产物：page.json, music_edit.wav, mix_raw.wav, mix.wav, frames/, stills/, 联系表
```

## 1. 写稿

- 七步结构（2026-10-26 起）：定主题 → 各种说法 → 我的理解 → 讲给没读过多少书的人听 → 对方哪里没懂 → 换更准的比喻重新理解 → 讨论话题 + 预告下一集，见 `docs/series-plan.md`。01–03 用的是旧的费曼四步。
- 稿子写进 `feynmanNN_make.py` 的 `LINES = [(id, 文本, 句后停顿秒), ...]`，同时存一份到 `cards/NN-<标题>.md`。
- 口播稿防读错：数字写汉字、去掉引号括号、多音字换词。每句单独生成。

## 2. 配音 + 回检 + 配乐候选（一条命令）

```sh
cd ~/Documents/ChatGPT/kindle/audio-stack && \
OUT_DIR=~/Movies/feynmanNN/out .venv/bin/python ~/Movies/feynmanNN/feynmanNN_make.py
```

做的事：

1. Qwen3-TTS 1.7B Base 逐句配音，参考音频 `~/高性价比人生指南-视频工程/voices/narrator.wav`（+ `narrator.json` 里的参考文本）。
2. 每句用 Qwen3-ASR 1.7B 回听，相似度 ≥ 0.92 且语速 2.8–7.5 字/秒才通过，否则换种子（11/23/37/51）重试。
3. 拼接出 `out/vo.wav`（24kHz，峰值约 −6 dBFS）、`out/timings.json`（每句起止）、`out/voice_report.txt`（⚠️ 的句子要单独重做）。
4. 按关键句的开口时间算一个最贴合的 BPM（`out/music/bpm.json`）。
5. 用 ACE-Step 1.5 XL-SFT（48 步，D minor）生成 3 首配乐候选 `out/music/cand_<seed>.wav`。02 的种子是 2201 / 4403 / 6605，用户选了 2201。

只重做配乐：加 `MUSIC_ONLY=1`。耗时：02 全流程约 4 分钟。

## 3. 用户试听并选配乐

把 `vo.wav` 和 3 首候选发给用户（直接上传到对话里），让用户挑一首。agent 听不到声音，不要声称「听起来不错」。

## 4. 画面与后期（在 `~/Movies/feynmanNN/` 下运行）

需要一个装了 playwright、numpy、scipy、soundfile 的 Python，以及 ffmpeg。

```sh
cd ~/Movies/feynmanNN
scripts/fetch_fonts.sh kit/fonts                                     # 首次：下载字体（仓库根目录的脚本）
python kit/make_timings_js.py out/timings.json 2201                  # timings.json → kit/timings.js（第二个参数是配乐种子，片尾显示）
python kit/dump.py                                                   # 导出 DUR / CUES / 音效事件 → work/page.json，字幕 → out/feynmanNN.srt
python kit/music_edit.py out/music/cand_2201.wav out/timings.json auto <DUR秒> work/music_edit.wav
                                                                     # 测拍、按小节剪接，把高潮对到 L16/L18（auto 取误差小的），结尾 1.8 秒淡出
python kit/mix.py out/vo.wav work/music_edit.wav work/page.json out/timings.json work/mix_raw.wav
                                                                     # 逐句闪避：人声比音乐高约 10 dB，句间音乐 −2 dB，片尾卡 ≥ −1 dB，合成轻音效
python kit/loudnorm.py work/mix_raw.wav work/mix.wav                 # 两遍 loudnorm → −14 LUFS，真峰值 ≤ −1 dBTP
python kit/render.py stills work/stills 2.3 6.0 9.9                  # 先渲几张静帧自查
python kit/render.py frames work/frames 8                            # 8 个进程逐帧截图 1080×1920@30fps
```

`<DUR秒>` 取 `work/page.json` 里的 `dur`（02 为 100.3）。

## 5. 压制（≤ 10MB）

抖音上传上限按 10MB 控制。02 用 x264 两遍编码，100 秒得到 9.06MB（总码率约 720 kbps）。参考命令（按时长调 `-b:v`，目标总大小 ≈ 9.5MB）：

```sh
ffmpeg -y -framerate 30 -i work/frames/f%05d.jpg -c:v libx264 -preset slow -b:v 580k -pass 1 -passlogfile work/x264 -an -f mp4 /dev/null
ffmpeg -y -framerate 30 -i work/frames/f%05d.jpg -i work/mix.wav -c:v libx264 -preset slow -b:v 580k -pass 2 -passlogfile work/x264 \
       -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart -shortest "out/费曼学习法卡片NN_<标题>.mp4"
```

## 6. 自检（全部通过才交给用户）

- 联系表：`work/stills.py` 在每句中点附近取帧，拼成 `work/contact.jpg`，看两遍（字是否出安全区、是否挡主体、有无空白帧）。
- `ffmpeg -i out.mp4 -af ebur128 -f null -` 确认约 −14 LUFS。
- `ffmpeg -i out.mp4 -vf blackdetect=d=0.1 -an -f null -` 确认没有黑帧。
- 文件大小 ≤ 10MB，1080×1920，30fps。
- 出处、许可、配音配乐来源都在片尾卡和 `out/CREDITS.txt` 里。

## 7. 封面

见 `docs/style-guide.md`「封面」。每集都要定制，不能截帧。

## 8. 交付与发布

1. 成片和封面上传到对话里，让用户直接播放查看。
2. 用户确认后，按 `docs/publishing-douyin.md` 发布。
3. 更新 `docs/status.md`、`cards/tree.yaml`。

## 怎么在 Mac 上执行

- 云端 agent 通过 Claude 的 Remote Control 会话在 Mac 上执行命令；Remote Control 的指令里不能出现 HTML 标签（`<tag`），需要传 HTML 时用 JS 写出或用文字描述。
- Claude 桌面版的文件夹工具跑在 Mac 上的 Linux 虚拟机里（约 4 核 3GB，无 Metal/MLX），只能读写文件和做数值分析，跑不了模型。
- Codex 等本机 agent 直接在终端运行上面的命令即可。
