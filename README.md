# AI 服装参考库 · 中文汉化版

将 [AI Costume Gallery](https://ai-costume-gallery.pages.dev/) 整理为本地中文静态图库，界面样式参考 [Anhao 的 AI 姿势参考库](https://github.com/anhao/ai-pose-gallery-zh)。

**原始网址：[https://ai-costume-gallery.pages.dev/](https://ai-costume-gallery.pages.dev/)**  
原作者：[ギア（@giaaibusi）](https://x.com/giaaibusi)。本项目是对上述原站的**中文汉化与本地化整理**，并非原站原创作品，也不代表原作者。

**非商业项目声明：** 本项目为个人学习、交流及非商业汉化整理而制作，不销售原站素材，不对原站图片及数据主张著作权。源码采用 **MIT License**；MIT 本身允许代码商业使用，此声明不对 MIT 源码许可增加额外限制。图片与原始数据不适用本项目 MIT 许可，须遵循原作者条款。

图库对应 **1,407 套服装 / 8 个分类 / 4,221 个图片文件（约 1.42 GiB）**。GitHub 源码仓库提供完整页面代码、中文与原始元数据、词典、下载/校验脚本和启动文件；**不包含图片及含原图的截图**，以遵守原站禁止图片再分发的条款。克隆代码后，需先运行下载脚本，才是素材齐全的可运行图库。

现有本地工作目录保留了全部已下载图片。页面零运行时依赖，素材齐全后可断网浏览；上传源码不会删除本地素材，也不等于公开部署网站。

## 启动

需要 Python 3.10 或更新版本。如果从 GitHub 获取源码，先在项目目录执行：

```powershell
python scripts/download.py
python scripts/verify.py
```

下载完成后，Windows 双击根目录的 **启动图库.cmd**，会启动本地服务并打开浏览器。原本已包含全部素材的本地目录无需重复下载。

也可在 PowerShell 执行：

```powershell
# 先进入你保存源码的目录
python scripts/serve.py --open
```

访问 [http://127.0.0.1:8949/](http://127.0.0.1:8949/)。服务仅监听本机，终端中按 `Ctrl+C` 停止。端口被占用时可指定其他端口：

```powershell
python scripts/serve.py --port 9321 --open
```

不要直接双击 `index.html`；浏览器需要通过 HTTP 读取 JSON 数据。

## 功能

- 八类服装页签及分类数量，分类与搜索可组合使用。
- 中文服装、颜色、材质关键词和原英文关键词检索；也支持完整或部分 ID。
- 多个词用空格分隔，结果同时满足各词，例如 `白色 蕾丝`。`/` 聚焦搜索。
- 详细 / 简洁卡片切换，卡片每批加载 60 套，图片懒加载。
- 点击查看大图；先显示缩略图与 WebP，再加载原尺寸 PNG，全程保持图片比例。
- 灯箱显示中文描述、英文关键词、ID、分类与实际原图尺寸。
- 下载 PNG、在新窗口打开、复制 ID、复制中文描述。
- `← / →` 或 `↑ / ↓` 浏览当前筛选结果，`Esc` 关闭大图；图片支持左右滑动切换。
- 手机双列网格、可收起筛选区、全屏灯箱；对话框提供焦点限制与关闭后焦点恢复。
- 中文使用指南、原站完整使用说明译文、原作者与样式参考来源。

服装站每套只有一张图片，因此没有虚构多角度切换或姿势分组；参考库的双浏览模式在这里适配为详细 / 简洁卡片。

## 收录规模

数据快照日期：2026-10-29。计数以保存的源数据为准，不使用原网页代码中遗留的旧数量注释。

| 中文分类 | 原分类 | 套数 |
| --- | --- | ---: |
| 春季 | 春 | 215 |
| 夏季 | 夏 | 254 |
| 秋季 | 秋 | 244 |
| 冬季 | 冬 | 253 |
| 内衣 | ランジェリー | 199 |
| 派对礼服 | パーティ | 48 |
| 泳装 | 水着 | 54 |
| 性感服饰 | セクシー | 140 |
| **合计** | | **1,407** |

每套保留 `thumbs/*.webp`、`img/*.webp`、`png/*.png` 三个源文件。原图保持站点原尺寸；灯箱动态读取尺寸，不将所有文件假定为同一分辨率。

## 目录

```text
pose-gallery/
├── index.html                 # 静态页面
├── styles.css                 # 参考库样式及服装版适配
├── app.js                     # 筛选、搜索、卡片与灯箱交互
├── 启动图库.cmd                # Windows 一键启动
├── data/
│   ├── costume.json           # 原始记录，保留日文字段与英文关键词
│   ├── costume-zh.json        # 页面使用的中文记录
│   ├── meta.json              # 原始分类与计数
│   ├── meta-zh.json           # 中文分类与计数
│   ├── translations.csv       # 分类、词汇、词组、逐条描述对照，UTF-8 BOM
│   ├── source-manifest.json   # 来源 URL、快照文件与 SHA-256
│   ├── download-report.json   # 图片下载结果
│   └── verification-report.json # 完整性检查结果
├── thumbs/                    # 1,407 张 WebP 缩略图
├── img/                       # 1,407 张 WebP 预览图
├── png/                       # 1,407 张 PNG 原图
├── scripts/
│   ├── download.py            # 并发下载，断点续传、有限重试、临时文件落盘
│   ├── i18n.py                # 中文分类与服装词典
│   ├── apply_translation.py   # 生成中文数据和对照表
│   ├── verify.py              # 记录、翻译与全量图片校验
│   └── serve.py               # Python 标准库本地 HTTP 服务
├── docs/
│   ├── design.md
│   ├── implementation-plan.md
│   ├── verification.md
│   ├── reference-LICENSE.txt  # 参考库原始许可证，原样保留
│   ├── source-terms.md        # 服装站使用说明，含原文与译文
│   └── screenshots/           # 仅本地保存，不随源码上传
├── .source/                   # 原始页面快照，仅供本地溯源，不参与页面运行
├── LICENSE
└── README.md
```

## 中文数据

| 字段 | 说明 |
| --- | --- |
| `id` | 保持原 ID，不重编号 |
| `分类` / `分类原文` | 中文分类 / 日文原分类 |
| `服装名称` | 主要服装词组构成的中文标题 |
| `中文描述` / `关键词` | 完整中文标签描述 / 分项列表 |
| `英文关键词` | 原站英文关键词，原样保留 |
| `缩略图` / `预览图` / `原图` | 本地相对路径 |
| `检索` | 中文、英文、原分类和 ID 的合并搜索文本 |

原站提供的是英文关键词列表，并非完整句子；部分列表会在颜色或材质处截断。中文通过服装词组优先匹配生成，保留这些尾部信息，不补写未提供的物品。全部原始词汇均有译文，但这不代表逐图人工校订，服装细节仍应对照图片确认。

修改 `scripts/i18n.py` 后重新生成：

```powershell
python scripts/apply_translation.py
```

遇到未收录词汇会直接报错，防止遗漏译文。修改 CSV 不会反向更改词典。

## 下载与检查

```powershell
# 重新检查并补齐缺失图片；已存在且容器完整的文件自动跳过
python scripts/download.py

# 调低并发
python scripts/download.py --workers 12

# 标准库校验：数据、翻译、数量、文件路径和图片容器
python scripts/verify.py

# 安装了 Pillow 的 Python 环境可进行全部图片逐像素解码
python scripts/verify.py --decode
```

下载器只对保存的数据快照补图，不会擅自替换已确认的条目或刷新原始数据。失败会输出文件路径并以非零状态退出；重跑可续传。`--decode` 是验收可选依赖，页面启动及默认下载、校验均不依赖 Pillow。

本次验收结果见 `docs/verification.md` 与 `data/verification-report.json`。手机布局为浏览器视口检查，不等于真实手机触屏手势验收。

## 来源与使用范围

- 服装图片和原始数据：[AI Costume Gallery](https://ai-costume-gallery.pages.dev/)，原作者 [ギア @giaaibusi](https://x.com/giaaibusi)。
- 界面基础样式：[anhao/ai-pose-gallery-zh](https://github.com/anhao/ai-pose-gallery-zh)，Copyright (c) 2026 Anhao，MIT 许可证。
- 本项目 `LICENSE` 仅覆盖界面代码和维护脚本，不覆盖图片与原始数据。原站完整条款及译文见 `docs/source-terms.md` 和页面“注意事项”。
- 原站允许作品创作中的免费使用、商业使用、编辑和参考，但**禁止图片数据本身的再分发、转载和转售（含加工后的图片）**。
- `.gitignore` 排除本地图片、含图截图和原始页面快照；GitHub 仅分发源码、中文元数据及说明。完整图片仍保存在现有本地工作目录，或由使用者根据原站条款自行下载。
