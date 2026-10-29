# AI 服装参考库实现计划

**目标：** 在 E:\TraeCode\pose-gallery 交付可离线浏览的完整中文服装图库。

**架构：** 页面通过本地 HTTP 读取 data/costume-zh.json；全部媒体使用相对路径。原始页面快照保存在 .source/，供元数据溯源，不作为页面运行依赖。

**技术：** HTML、参考库 MIT CSS、原生 JavaScript、Python 标准库；验收使用实际浏览器与 Pillow 图片解码。

## 执行顺序

- [x] 1. 保存原始数据；创建 scripts/download.py，下载 thumbs/、img/、png/ 的 4,221 个文件。以临时文件原子落盘，支持断点续传、有限重试和失败退出。
- [x] 2. 创建 scripts/i18n.py 与 scripts/apply_translation.py；生成 costume-zh.json、meta-zh.json 与 translations.csv，未覆盖词汇立即失败。
- [x] 3. 创建 index.html、styles.css、app.js；复用参考库设计语言，实现分类与搜索、卡片与加载更多、灯箱与复制/下载、键盘/触屏和移动端筛选。
- [x] 4. 创建 scripts/verify.py、scripts/serve.py、启动图库.cmd、README.md、LICENSE 与来源说明。启动服务仅绑定本机，页面无外部依赖。
- [x] 5. 运行 python scripts/verify.py 和全部图片解码。启动本地服务，检查桌面/手机布局及核心交互，保存截图与验证结果。

## 验收命令

```powershell
python scripts/apply_translation.py
python scripts/download.py
python scripts/verify.py
python scripts/serve.py
```

前三条必须返回 0。浏览器必须显示 1,407 套、8 分类；每个分类计数与原站一致；实际 PNG 下载、中文搜索、清空、加载更多、前后切换、Esc、手机无横向溢出均通过。
