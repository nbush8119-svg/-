# 02 · 哲学（树码 A）

完整工程，目录结构和 Mac 上的 `~/Movies/feynman02/` 一致。口播稿和分镜见 `cards/02-哲学.md`，流程见 `docs/production-pipeline.md`。

| 路径 | 内容 |
|---|---|
| `feynman02_make.py` | 口播稿 LINES；本地 Qwen3-TTS 配音 + Qwen3-ASR 回检 + 算 BPM + ACE-Step 3 首配乐候选 |
| `kit/index.html` | 画面（Canvas 逐帧，读 `timings.js`）；字体放 `kit/fonts/`（`scripts/fetch_fonts.sh kit/fonts`） |
| `kit/*.py` | `make_timings_js` → `dump` → `music_edit` → `mix` → `loudnorm` → `render` |
| `out/vo.wav` | 定稿配音（24kHz）。重做画面或混音时可以直接用，不必重新配音 |
| `out/timings.json`, `out/voice_report.txt` | 每句起止时间、回检报告（22 句全过） |
| `out/music/_gen.py`, `bpm.json` | 配乐生成脚本与参数（候选 wav 太大没入库，种子 2201 可复现） |
| `out/feynman02.srt`, `out/CREDITS.txt` | 字幕、素材与许可 |
| `work/page.json`, `work/music_edit.json` | 画面导出的 DUR/CUES/音效事件；配乐剪接参数 |
| `work/contact.jpg`, `work/qc_contact.jpg` | 自检联系表 |
| `cover/` | 封面 HTML + 截图脚本 + 渲染结果 |
| `release/` | 发布用成片 mp4（100.3 秒，9.06MB）、封面（截帧版和卡片版，发布用卡片版）、发布文案 |
| `HANDOFF_2026-10-23.md` | 当时给 Mac 本机会话的交接说明（部分路径已过时，以 docs/ 为准） |

没入库、需要时在 Mac 上找或重新生成：`out/lines/*.wav`、`out/music/cand_*.wav`、`work/mix*.wav`、`work/frames/`、字体。
