# 用户 Mac 上的环境

- 机器：laoyudeMacBook-Pro（Apple Silicon，M5 Max，128GB），用户名 `laoyu`。
- 所有模型本地运行，不花积分、不联网。

## 音频模型：`~/Documents/ChatGPT/kindle/audio-stack/`

| 用途 | 位置 |
|---|---|
| 配音（复用参考音色） | `models/Qwen3-TTS-1.7B-Base-bf16` |
| 音色设计 | `models/Qwen3-TTS-1.7B-VoiceDesign-bf16` |
| 读音回检 | `models/Qwen3-ASR-1.7B-8bit` |
| 逐字时间戳 | `models/Qwen3-ForcedAligner-0.6B-8bit` |
| 配乐 | `ACE-Step-1.5/`（DiT `acestep-v15-xl-sft`，LM `acestep-5Hz-lm-1.7B`，MLX 后端） |

- 语音环境 `audio-stack/.venv`（Python 3.12，mlx-audio）；配乐环境 `audio-stack/ACE-Step-1.5/.venv`（Python 3.11）。两者隔离，不要混装。
- `verify_speech.py`、`verify_music.py` 是验证过的调用范例，`feynmanNN_make.py` 直接从它们抄 import。
- 详细 API 和排错见 `docs/skills/local-zh-voice-music.md`。

## 旁白音色

- 全系列（也包括另一个系列《高性价比人生指南》）用同一个男声旁白。
- 参考音频：`~/高性价比人生指南-视频工程/voices/narrator.wav` + `narrator.json`（参考文本）。取自 `~/Downloads/ep01_vo_brian.mp3` 的 14.4–26.0 秒（《高性价比人生指南》EP01 的纯人声轨，ElevenLabs Brian 音色，经 vidIQ 生成）。
- 2026-10-23 用户决定继续用这个 Brian 音色，作为本地 Qwen3-TTS 的参考，不再花 ElevenLabs 额度。
- 这段音频**不在仓库里**（来自 ElevenLabs）。在别的机器上要复现，需要从上面的 mp3 重新截取同一段。

## 工程与产物位置

| 内容 | Mac 路径 |
|---|---|
| 02 哲学工程 | `~/Movies/feynman02/`（`kit/` `out/` `work/`） |
| 01 封面 | `~/Movies/feynman01_cover/`、`~/Claude/feynman01_cover/` |
| 发布截图、成片副本 | `~/Claude/feynman02/` |
| 字体副本 | `~/Movies/feynman02/kit/fonts/`（OTF）、`~/Claude/feynman02/_fonts/`（TTC） |
| 《高性价比人生指南》工程 | `~/高性价比人生指南-视频工程/` |
| 代码拍视频资料库 | `~/opus-video-kit/`（见 `docs/skills/opus-video-studio.md`） |

01 三观的完整源工程没有保存在 `~/Movies` 或 `~/Claude` 下。

## 发布用浏览器

已登录抖音创作者中心的 Chrome。登录态只在用户机器上，绝不导出或入库。
