# 画面与封面规范

## 视频画面

- 1080×1920，30fps，竖屏。画面由代码逐帧绘制（`kit/index.html` 的 Canvas 2D，`render(t)` 只由 t 决定，不用 CSS 动画、计时器、无种子随机数）。
- 页面约定：`window.DUR`、`window.render(t)`、`window.READY`、`window.CUES=[[起,止,字幕]]`、`window.EV=[{t,type}]`（音效事件）。
- 配色（深色高级）：

| 用途 | 色值 |
|---|---|
| 底色 PAPER（加径向渐变） | `#0E1014` |
| 卡片 CARD | `#161A20` |
| 文字 象牙白 INK | `#ECE5D8` |
| 唯一强调色 香槟金 | `#CDAA6B` |
| 辅色 MUTE / SOFT | `#857F74` / `#2B3039` |

- 字体：Noto Sans CJK SC（Medium/Bold/Black）、Noto Serif CJK SC（Black），SIL OFL 1.1，本地加载，不链外网。
- 安全区：顶部 200px、底部 420px、右侧 160px 不放关键内容；主画面 300–1250px；字幕在 1300–1480px，必须烧录。
- 字幕：每句一条，≤ 2 行，在中间附近的标点处折行；关键词（如「费曼学习法」「哲学」「三观」）用金色高亮。
- 片尾卡停留 ≥ 3 秒：「费曼学习法卡片，第 N 张」、出处、CC BY 4.0、配音配乐来源、下一张预告。
- 音效：numpy 合成的轻音效（tick、pop、whoosh、stamp、strike、pen、drop、chime），峰值对齐事件时刻，低于人声。

## 导演规则（摘自 `docs/skills/opus-video-studio.md`）

- 前 3 秒是钩子；结尾呼应开头。
- 拒绝 PPT 感：镜头时长差 ≥ 4 倍，每个段落边界都要有东西活过切换。
- 阅读时间：字幕 ≥ max(1.8 秒, 口播 + 0.6 秒)。
- 声音：人声高于音乐约 10 dB；−14 LUFS，≤ −1 dBTP；不用泛泛的「钢琴 + 弦乐」。
- 禁用：粒子爆炸、冲击波、RGB 分离、霓虹辉光、闪烁背景、弹跳缓动、默认淡入淡出。

## 封面

模板：`templates/cover/cover.html`（02 的卡片版）；01 的三个方案在 `templates/cover/cover_01_variants.html`（`#1` 罗盘版、`#2` 三观不合冲突版、`#3` 卡片版，用户选了 #3）。

- 风格：「卡片版」。底色 `#0E1014` + 径向渐变 + 细颗粒噪点，大号衬线标题（Noto Serif），香槟金 `#CDAA6B` 强调。
- 左上角徽章「**No.XX** 费曼学习法卡片」，位置 left 80px / top 250px。
- 关键内容放在 y 240–1500px 之间（抖音会在底部和右侧盖 UI）。
- 渲染：`cd templates/cover && node shot.js` → `cover.png`（1080×1920）；变体版 `node shot_variants.js 1 2 3` → `v1.png` 等。需要 `npm i playwright`。
- 字体：`cover.html` 用系统里安装的 `Noto Sans CJK SC` / `Noto Serif CJK SC`；`cover_01_variants.html` 用的是 `Noto Sans SC` / `Noto Serif SC`（Google Fonts 名）。渲染前确认字体已安装，否则会退回系统字体。
- 导出 JPG 后放到 `episodes/NN-*/release/封面_卡片版.jpg`。
- 每集都要重新做，不能用视频截帧（01 第一次发布时用了黑帧封面，后来返工）。
