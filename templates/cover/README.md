# 封面模板

- `cover.html` + `shot.js`：卡片版封面（02 用的版本）。改徽章编号、标题、关键词后运行 `node shot.js` 得到 `cover.png`（1080×1920）。
- `cover_01_variants.html` + `shot_variants.js`：01 的三个方案，用 `#1/#2/#3` 切换，`node shot_variants.js 1 2 3` 输出 `v1.png` 等。
- 需要 `npm i playwright` 和已安装的 Noto CJK 字体。规范见 `docs/style-guide.md`「封面」。
