# 逐梦前行，心绘中大 · 中山大学招生概念站

> 2026 年中山大学招生设计大赛 · 网页类参赛作品

一个单页招宣互动概念站，围绕"三校区五校园"与中大校训展开。主站以滚动驱动的书法书写动画为核心视觉记忆点；五校园板块正在迭代隶书字形 + 信纸照片堆的交互方案。

## 本地预览

主站直接双击 `index.html` 即可在浏览器中打开（推荐 Chrome / Edge）。

五校园交互原型在 `demos/campus-ink-ligen-demo.html`，同样双击打开。

如需本地服务器预览（可选）：

```bash
python -m http.server 8000
# 浏览器访问 http://localhost:8000
```

## 主站页面结构

| 区块 | 锚点 | 内容 |
| --- | --- | --- |
| Hero | — | 「逐梦前行，心绘中大」+ 校徽 |
| 五校园长廊 | `#campus` | 南校园怀士堂 / 北校园中山医红楼 / 东校园图书馆 / 深圳校区图书馆 / 珠海校区天琴中心 |
| 校训书写 | `#motto` | 滚动驱动，一笔一划写出"博学审问慎思明辨笃行"，写完淡化成背景 |
| 数字里的中大 | `#why` | 五项办学数据 |
| 招生服务入口 | `#service` | 学校概况 / 院系专业 / 招生章程 / 招生计划 / 历年分数 / 联系院系 |
| 结尾 | `#ending` | 公众号与小程序二维码 |
| Footer | — | 招生办联系方式 |

## 五校园交互方案（迭代中）

当前方案：`demos/campus-ink-ligen-demo.html`

- 五个校名词以隶书字形竖排呈现（南校园 / 东校园 / 北校园 / 深圳校区 / 珠海校区）
- 字形来自用户提供的 10 张隶书字图，经去背、二值化、裁剪后为透明底 PNG，base64 内嵌
- `#sealInk` 滤镜（`feTurbulence` + `feDisplacementMap`）给字形边缘加手写墨痕
- 米色宣纸底 + 顶部光晕 / 底部暗角渐变
- 交互动画：点击校园字 → 墨色涟漪 → 信纸浮现 + 照片堆 → 点击照片查看详情（调整中）

### 原型归档

`demos/` 目录下保留了历次迭代原型，供参考：

| 文件 | 方案 | 状态 |
| --- | --- | --- |
| `campus-ink-ligen-demo.html` | 隶书字形 + 信纸照片堆动画 | **当前方案** |
| `campus-ink-demo.html` | 篆书字形 + 信纸动画 | 已被隶书版取代 |
| `campus-click-demo.html` | 点击交互原型 | 已归档 |
| `campus-3d-demo.html` / `campus-3d-demo-v2.html` | 3D 卡片原型 | 已归档 |

## 修改与重建

`demos/campus-ink-ligen-demo.html` 是**生成物**，不要直接编辑它。正确流程：

1. 改版式 / 文案 / 样式 → 编辑 `_src/ligen-lite.src.html`（源模板）
2. 改字形 → 把新字图放进 `_src/ligen/`，跑 `_src/ligen/process_ligen.py` 重新出 PNG
3. 重建生成物 → 仓库根目录执行：

```bash
python build_lite.py
```

脚本会从 `_src/campus-ink-ligen-demo.v3-anim.bak.html` 提取 GLYPH_IMAGES base64 数据行，注入模板，输出到 `demos/campus-ink-ligen-demo.html`。

## 技术说明

- 纯静态单页，原生 HTML / CSS / JavaScript，无构建工具、无框架依赖
- 校训书写：基于书法楷体笔画轮廓数据，沿运笔中线逐笔揭示，滚动进度直接映射书写行程，支持正向书写与回滚擦除
- 主站配色：米白纸 `#F5F1E8`、墨绿 `#1F4D38`、砖红 `#8B3A2E`、金 `#C9A24B`
- 页面字体经 CDN 加载（Noto Serif SC / Noto Sans SC），离线时回退到系统字体
- 响应式适配桌面与移动端

## 文件结构

```
sysu-admission-site/
├── index.html                  # 主站（单文件自包含，内联校训笔画数据）
├── assets/                     # 主站素材
│   ├── campus-nan.png              # 南校园·怀士堂
│   ├── campus-bei.png              # 北校园·中山医红楼
│   ├── campus-dong.png             # 东校园·图书馆
│   ├── campus-shenzhen.png         # 深圳校区·图书馆
│   ├── campus-zhuhai.png           # 珠海校区·天琴中心
│   ├── logo.gif                    # 校徽与中英文校名
│   ├── qr-gzh.jpg                  # 本科招生公众号二维码
│   └── qr-mini.jpg                 # 本科招生小程序二维码
├── demos/                      # 交互原型
│   ├── campus-ink-ligen-demo.html  # 当前方案：隶书字形 + 信纸照片堆
│   └── archive/                    # 历次迭代归档
│       ├── campus-ink-demo.html       # 旧方案：篆书字形
│       ├── campus-click-demo.html     # 点击交互原型
│       ├── campus-3d-demo.html        # 3D 卡片原型
│       └── campus-3d-demo-v2.html     # 3D 卡片原型 v2
├── docs/                       # 项目文档
│   └── 项目现状.md                 # 项目进度与待办
├── _src/                       # 源模板与构建脚本（勿直接编辑生成物）
│   ├── ligen-lite.src.html         # 当前方案源模板
│   ├── campus-ink-ligen-demo.v3-anim.bak.html  # 字形 base64 数据来源
│   ├── ligen/                      # 隶书字形素材与处理脚本
│   │   ├── *.jpg                   # 原始字图（用户提供）
│   │   ├── processed/*.png         # 去背、二值化、裁剪后的字形 PNG
│   │   └── process_ligen.py        # 图片处理脚本（需 Pillow）
│   ├── archive/                    # 旧方案归档（篆书字形生成器等）
│   └── *.py                        # 历史迭代脚本
├── build_lite.py               # 构建脚本：模板 + 字形注入 → demos/ 生成物
├── preview.png                 # 主站预览图
├── README.md
└── .gitignore
```

## 比赛信息

- 赛事：2026 年中山大学招生设计大赛
- 主题：逐梦前行，心绘中大
- 类别：网页类（需提供设计稿 + 演示方案）
- 截止：2026 年 10 月 20 日 24:00

## 许可

本作品为参赛用途，素材版权归中山大学及原作者所有。
