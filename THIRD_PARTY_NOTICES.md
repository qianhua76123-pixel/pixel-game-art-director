# Third-party notices / 第三方内容说明

本仓库是原创工具、案例评论与第三方教程的汇编，并不使用单一许可证覆盖全部文件。根目录 [LICENSE](LICENSE) 的 MIT 许可涵盖原创脚本、技能编排、独立配方、模板、案例评论与测试夹具；AI 示例图的范围见下文。任何第三方图像、字体、正文、源快照及其中文改编仍受对应来源许可约束。以下声明随 v1.5.0 补充。

## 逐项定位

[完整目录](library/catalog.json) 与 `library/manifests/` 为每篇记录作者、标题、原始 URL、抓取日期、许可、图像来源和哈希。正文开头及末尾也保留来源；Krita 的 `library/sources/asset-production/*/original.rst` 保留原页作者元数据。它们是归属核验的入口，不应在下游打包时丢弃。

| 内容 | 原作者/项目 | 适用许可与证据 | 本库的变化 |
|---|---|---|---|
| Saint11 图片教程，包括绘画、动画、九宫格和流程补充 | Pedro Medeiros / Saint11 | [固定提交 README](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/README.md)，[CC BY 4.0 全文](library/licenses/CC-BY-4.0.txt) | 原始 GIF 保留；抽帧 PNG、中文导读、练习及元数据明确为整理/改编 |
| Godot 4.5 文档正文、文档图与示例 | Juan Linietsky、Ariel Manzur 和 Godot 社区；个别图另署名 | [文档仓库许可声明](https://github.com/godotengine/godot-docs/blob/4.5/README.md#license)，[本地许可全文](library/licenses/godot-docs-4.5-LICENSE.txt) | HTML 主体转为 Markdown，图像本地化，增加中文任务导读；版本固定为 4.5 |
| Krita 文档与一般教学图片 | 各页 RST 元数据中列明的作者 | [许可证据](library/licenses/krita-licensing-evidence.md)，[GFDL 1.3 全文](library/licenses/GFDL-1.3.txt)；原页声明 1.3 或更新版本 | HTML 主体转换，保留透明可编辑的 Markdown/RST 与许可，增加中文导读与修改历史 |
| MAKE-001 中 Pepper & Carrot 相关示例 | David Revoy / deevad | 原文图旁独立标明 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | 保留图旁署名和来源；不套用 MIT 或其他图的许可 |
| UI-002 中 Tank Kings “Gear Up!” 截图 | Winterpixel Games | Godot 原文署名 “courtesy of Winterpixel Games”；随所在文档保留，其来源记录见 [UI-002](library/tutorials/game-development/UI-002-gui-theme-system.md) | 作为主题系统说明图引用；不能把文档许可记录解释成作者向本项目另行提供游戏素材包 |
| 商店示例中的 Fusion Pixel 12px Proportional zh-Hans 字体 | TakWolf 及上游字体贡献者 | [官方 2026.10.25 发行版](https://github.com/TakWolf/fusion-pixel-font/releases/tag/2026.10.25)、[OFL 全文](examples/rural-shop-demo/assets/font/OFL.txt)、[来源与哈希](examples/rural-shop-demo/assets/font/font-source.json) | 官方 WOFF2 原文件，未子集化或转换；保留 Fusion Pixel 与上游组件声明 |
| 四组视觉一致性研究的 8 张官方截图 | Heart Machine、Dead Mage／11 bit studios、Umami Tiger／发行商、MINTROCKET 及各自权利人 | [逐图原始来源与哈希](references/visual-game-studies.json)；未发现开放再分发许可 | 仅保存官方图像链接和原创评论，商业图像二进制不打包 |
| 商店并排对照的 2 张官方截图 | Moonlighter：Digital Sun／11 bit studios；Stardew Valley：ConcernedApe | [原始来源与证据](review/shop-benchmark/benchmark.json)；未发现开放素材再分发许可 | 远程引用，附原创观察；不作为生成输入或项目成品素材 |

关于各图的范围：本库按所在获许可文档保存教学说明图；若图旁列出不同作者、来源或独立许可，以该项声明为准。文档所示软件、游戏、商标和角色仍归各自权利人；本库不声称作者认可本项目。把截图中的角色、图标或界面裁出用于游戏，不能只靠此汇编的 MIT 许可。

## 商业游戏案例的链接与评论

原有 [14 例 UI 案例](references/ui-case-studies.md) 共 28 个参考图像链接；新增 [4 例视觉一致性研究](references/visual-game-studies.md) 共 8 个官方图像链接。另有 [商店并排对照](review/shop-benchmark/README.md) 的 2 张官方参考图，分别为 Moonlighter 商人服务与 Stardew Valley 种子购买；它们独立计数，不增加教程数，也不把商业游戏截图加入开放素材包。Markdown 及审核页面可从原站显示图像；远程显示不授予素材再利用权。

游戏名称、商标、角色、场景、界面与截图归对应权利人。新增研究区分可见事实与原创设计推论，供学习和审阅；不得从原图裁切、描摹或提取人物、图标、纹样或地图用于游戏生产。截图中的宣传叠字也不能未经区分地当成游戏内 UI 证据。若原站链接失效，不应以未经授权的转载副本补入分发包。

## 商店 AI 示例图与运行截图

`examples/rural-shop-demo/assets/` 及其 `v2/`、`v3/` 子目录共保留十张由本项目通过内置图像生成工具制作的源 PNG；当前界面使用 v3 两张，历史八张保留。未使用本库商业案例截图作为成品素材。原四图 `village-shop.png`、`wood-panel.png`、`counter-ledger.png`、`item-atlas.png` 的提示词、源文件哈希和观察记录保存在 [prompt-set.md](examples/rural-shop-demo/assets/prompt-set.md) 与 [asset-provenance.json](examples/rural-shop-demo/assets/asset-provenance.json)。旧 `wood-panel.png` 已退出当前界面，仍作为历史源图保留。

v1.3.1 新增 `plain-paper-panel.png`，经一次独立的内置 `image_gen` 调用生成，原 PNG 未重绘、裁切、重采样或重新量化。完整提示词见 [plain-panel-prompt.md](examples/rural-shop-demo/assets/plain-panel-prompt.md)，原图哈希、尺寸、观察结果及九宫格切片记录见 [plain-panel-provenance.json](examples/rural-shop-demo/assets/plain-panel-provenance.json)。该历史界面的 CSS 九宫格显示不改变所保存的源文件。

v1.4.0 新增三张原 PNG，共三次内置 `image_gen` 调用：

- `assets/v2/merchant-and-goods-source.png`：原创店主与六商品母版，[提示词](examples/rural-shop-demo/assets/v2/merchant-and-goods-prompt.md)、[来源与限制](examples/rural-shop-demo/assets/v2/merchant-and-goods-provenance.json)。
- `assets/v2/environment.png`：引用原创母版作配色／画法参考的室内背景，[提示词](examples/rural-shop-demo/assets/v2/environment-prompt.md)、[来源](examples/rural-shop-demo/assets/v2/environment-provenance.json)。
- `assets/v2/panel.png`：引用原创母版作风格参考的纸木面板，[提示词](examples/rural-shop-demo/assets/v2/panel-prompt.md)、[来源与切片](examples/rural-shop-demo/assets/v2/panel-provenance.json)。

这三张历史图均保留生成原文件，商业截图没有用于这三次生成。`atlas.json` 只记录主体范围；Canvas `drawImage` 在运行时采样、取图与九宫格合成，不修改源图，也不代表已导出通过验收的原生像素 PNG。

v1.5.0 新增两张最终源 PNG：[shop-scene.png](examples/rural-shop-demo/assets/v3/shop-scene.png) 与 [goods-source.png](examples/rural-shop-demo/assets/v3/goods-source.png)。本轮四次成功的内置 `image_gen` 调用分别完成初始场景、构图修改、商品图集和像素简化修改，当前分发的是两张最终图；来源与提示词见 [provenance.json](examples/rural-shop-demo/assets/v3/provenance.json)、[prompts.md](examples/rural-shop-demo/assets/v3/prompts.md)。商品图集与修改只引用本项目原创场景，商业参考没有用于生成。v3 的 [atlas.json](examples/rural-shop-demo/assets/v3/atlas.json) 只记录主体范围，源 PNG 未改写。

这十张图仅在项目实际持有权利的范围内按根目录 MIT 许可提供（to the extent rights are held）。本项目不保证 AI 输出的独占性、唯一性、手绘作者身份或独立版权保护。运行截图展示本项目代码、AI 示例图与所附字体；截图不会改变各组成部分的许可。

这些图是像素风原型示例，严格原生网格、硬 alpha 与生产导出尚未完成验收。运行时采样不使源图获得生产认证，商业参考的许可也不会因并排显示而改变。v2 是用户已否定的历史视觉稿；v3 仍待用户看图审核。

## Fusion Pixel 字体及上游声明

字体文件 `fusion-pixel-12px-proportional-zh_hans.otf.woff2` 来自 Fusion Pixel 官方 `2026.10.25` 发行版，未做子集化、转换或其他修改，继续采用 SIL Open Font License 1.1。再分发时保留以下原始声明，不将字体改为 MIT：

- [Fusion Pixel OFL.txt](examples/rural-shop-demo/assets/font/OFL.txt)
- [Ark Pixel OFL.txt](examples/rural-shop-demo/assets/font/LICENSES/ark-pixel/OFL.txt)
- [Cubic 11 OFL.txt](examples/rural-shop-demo/assets/font/LICENSES/cubic-11/OFL.txt)
- [Galmuri LICENSE.txt](examples/rural-shop-demo/assets/font/LICENSES/galmuri/LICENSE.txt)

官方来源、下载地址、版本、字体与发行包 SHA-256 见 [font-source.json](examples/rural-shop-demo/assets/font/font-source.json)。使用或分发修改版时继续按原许可处理版权声明、保留字体名等要求；本库没有修改这些上游条款。

## GFDL 文档的改编与源文件

Krita 各页与对应中文整理继续保留 GFDL 1.3 或更新版本声明。保留原作者列表、页面源 RST、原图、许可全文，以及每页的转换/中文补充历史。Markdown 与 RST 都是可修改的文本形式。下游如果分发修改版，应继续满足 GFDL 的署名、修改和许可保留要求，不得只附本仓库的 MIT 文件。

## 分发任务资料包

`scripts/task_bundle.py --copy-figures` 会附图源与许可记录，且把涉及的许可证文本带入资料包。该工具用于保留归属信息，不代表它已经替某个商业项目完成全部资产权利核验。新加入的外部案例只有在许可允许时才加入可离线分发的图片；仅做链接和评论的案例不算作已授权素材。

完整历史与说明见 [library/LICENSES.md](library/LICENSES.md)。
