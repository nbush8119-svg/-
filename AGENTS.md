# AGENTS.md · 费曼学习法卡片

给接手本仓库的 agent（Codex、Claude Code 等）。先读完本页，再按需读 `docs/`。

## 这是什么

用户 Shaomanman 把自己对人生和世界的理解做成一张张「费曼学习法卡片」，每张卡做成一条抖音竖屏短视频，发进抖音合集「费曼学习法卡片」，最终长成一套个人知识体系（知识殿堂）。

- 已发布：01 三观（根），02 哲学（主干 A「怎么想」的主干卡）。
- 合集是一棵**开放的知识树**：没有总集数、没有季、没有大结局。详见 `docs/series-plan.md`。

## 用户的长期规则（必须遵守）

1. **用简体中文**和用户沟通，回复简短、先说结论。
2. **不要让用户处理文件**（下载、移动、转发、拖进对话），也**不要让用户跑脚本**。文件传输和命令都由 agent 自己在用户的 Mac 上完成。
3. 在 Mac 上产出的视频和封面，**成片要直接发给用户看**（上传到对话里能直接播放），不要只给一个 Mac 路径。
4. **配音和配乐只用 Mac 上的本地模型**：Qwen3-TTS（配音）、Qwen3-ASR（读音回检）、ACE-Step 1.5（配乐）。不用 ElevenLabs，不花额度。旁白音色全系列统一（见 `docs/mac-environment.md`）。
5. 每集都要**定制卡片风格封面**，不能用自动截取的帧（01 曾因黑帧封面返工）。模板在 `templates/cover/`。
6. **发布到抖音、修改已发布作品之前，必须得到用户本人的确认**。标题 ≤ 30 字，上传 ≤ 10MB，公开，进合集。见 `docs/publishing-douyin.md`。
7. 片尾和简介都要写出处与许可：内容「作者自我认知（Shaomanman）」，CC BY 4.0；配音、配乐写实际来源。
8. 每张新卡都要标**树码和上级**（如「A3.1 期望值，上级 A3 概率思维」），永远不要规划「最后一集」。
9. **绝不提交**密钥、Cookie、浏览器登录态、账号截图里的隐私信息。

## 仓库结构

```
AGENTS.md                 本文件（Codex 读这个）
CLAUDE.md                 指向本文件
README.md                 人看的总览
cards/                    卡片内容：tree.yaml（知识树索引）+ 每张卡的口播稿
docs/
  series-plan.md          合集规划：知识树、树码、六根主干、发布顺序、每集格式
  production-pipeline.md  从稿子到成片的完整流水线和命令
  style-guide.md          画面与封面的配色、字体、安全区、导演规则
  publishing-douyin.md    抖音发布规则和清单
  mac-environment.md      用户 Mac 上的环境、模型、路径
  status.md               每集进度与发布记录
  user-rules.md           用户偏好与历史决定（更完整的版本）
  skills/                 两个相关技能的原文（本地配音配乐、代码拍视频）
templates/cover/          封面 HTML 模板 + Playwright 截图脚本
episodes/
  01-sanguan/             01 三观：封面方案、旧版画面模板和脚本
  02-philosophy/          02 哲学：完整工程（口播稿、画面、混音、渲染脚本、成片、封面、发布文案）
scripts/fetch_fonts.sh    下载 Noto CJK 字体（字体不入库）
```

## 做一张新卡的最短路径

1. 在 `cards/tree.yaml` 里确定发布号、树码、上级；在 `cards/` 写口播稿（2026-10-26 起用七步结构：定主题 → 各种说法 → 我的理解 → 讲给没读过多少书的人听 → 对方哪里没懂 → 换更准的比喻重新理解 → 讨论话题 + 预告下一集，见 `docs/series-plan.md`「每集统一格式」）。
2. 复制 `episodes/02-philosophy/` 为 `episodes/NN-<slug>/`，改 `feynmanNN_make.py` 里的 `LINES` 和配乐 caption，改 `kit/index.html` 的画面。
3. 在用户 Mac 上按 `docs/production-pipeline.md` 跑：配音 + 回检 → 配乐 3 首候选 → 用户选 → 剪接对齐 → 混音 → 渲染 → 压制 → 自检。
4. 用 `templates/cover/` 做卡片风格封面。
5. 把成片和封面发给用户看；用户确认后再发布到抖音。
6. 更新 `docs/status.md` 和 `cards/tree.yaml`。

## 运行环境须知

- 模型推理只能在用户的 Mac（Apple Silicon，MLX）上跑。云端容器、Linux 虚拟机跑不了 MLX。
- 画面渲染需要 Playwright + Chromium、ffmpeg、Python（numpy、scipy、soundfile）。
- 字体：`scripts/fetch_fonts.sh episodes/<集>/kit/fonts`。
- 仓库里的脚本默认以 `~/Movies/feynmanNN/` 为工程目录（`kit/`、`out/`、`work/` 三个子目录），本仓库的 `episodes/NN-*/` 保持同样的结构，可以直接复制过去用。
