# 费曼学习法卡片

把对人生和世界的理解，用费曼学习法做成一张张卡片，再做成抖音竖屏短视频，长成一棵永远在长的知识树。

- 抖音合集：「费曼学习法卡片」
- 作者：Shaomanman · 内容许可 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 合集规划原文：https://claude.ai/artifact/VQGAokE3Bz8KggeR4pUU2j（仓库内副本：[docs/series-plan.md](docs/series-plan.md)）

## 已发布

| 发布号 | 树码 | 卡片 | 一句话 | 成片 |
|---|---|---|---|---|
| 01 | 根 | 三观 | 三观，就是你每天都在用的导航 | 只有封面在库（源工程未保存） |
| 02 | A | 哲学 | 哲学，就是把理所当然，重新问一遍 | [episodes/02-philosophy/release](episodes/02-philosophy/release) |

## 知识树与树码

01 三观是根，往上长出六根主干：A 怎么想、B 世界怎么运转、C 认识自己、D 和人相处、E 生存技能、F 怎么活（以后还能长第七根）。每张卡有两个编号：

- **发布号**：按发布顺序 01、02、03…，没有上限；
- **树码**：卡片在树上的位置，主干 A–F，一级知识点 A3，下级 A3.1，再下级 A3.1.1。

每张卡只有一个上级，可以「连向」别的枝条。下级卡片从三处长出来：讲不透的概念、评论区追问、生活里的新领悟。索引在 [cards/tree.yaml](cards/tree.yaml)。

## 生产流水线（全部在用户 Mac 上本地完成）

```
口播稿 LINES ──► Qwen3-TTS 逐句配音（复用系列旁白音色）──► Qwen3-ASR 回听比对（≥0.92）
      │                                                        │
      │                                     vo.wav + timings.json（每句起止时间）
      ▼                                                        ▼
 按关键句算 BPM ──► ACE-Step 1.5 生成 3 首配乐候选 ──► 用户选 ──► 按小节剪接，高潮对准关键台词
                                                                       │
 index.html（Canvas，render(t) 纯函数）◄── timings.js                   ▼
      │                                                     逐句闪避混音 → 两遍 loudnorm −14 LUFS
      ▼                                                                │
 Playwright 逐帧截图 1080×1920@30 ─────────────► ffmpeg 合成压制（≤10MB）◄┘
                                                          │
                     自检（联系表、安全区、ebur128、blackdetect）→ 封面 → 用户确认 → 抖音发布
```

详细命令见 [docs/production-pipeline.md](docs/production-pipeline.md)；画面规范见 [docs/style-guide.md](docs/style-guide.md)；发布规则见 [docs/publishing-douyin.md](docs/publishing-douyin.md)。

## 封面

`templates/cover/cover.html` 是卡片风格封面模板（深色 #0E1014 + 香槟金 #CDAA6B、大号衬线标题、左上角「No.XX 费曼学习法卡片」徽章），`node templates/cover/shot.js` 用 Playwright 截出 1080×1920 PNG。

## 给 agent

请读 [AGENTS.md](AGENTS.md)。
