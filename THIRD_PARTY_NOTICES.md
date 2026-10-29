# Third-party notices / 第三方内容说明

本仓库是原创工具与第三方教程的汇编，并不使用单一许可证覆盖全部文件。根目录 [LICENSE](LICENSE) 的 MIT 许可只涵盖原创脚本、技能编排、独立配方、模板与测试夹具。任何第三方图像、正文、源快照及其中文改编仍受对应来源许可约束。

## 逐项定位

[完整目录](library/catalog.json) 与 `library/manifests/` 为每篇记录作者、标题、原始 URL、抓取日期、许可、图像来源和哈希。正文开头及末尾也保留来源；Krita 的 `library/sources/asset-production/*/original.rst` 保留原页作者元数据。它们是归属核验的入口，不应在下游打包时丢弃。

| 内容 | 原作者/项目 | 适用许可与证据 | 本库的变化 |
|---|---|---|---|
| Saint11 图片教程，包括绘画、动画、九宫格和流程补充 | Pedro Medeiros / Saint11 | [固定提交 README](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/README.md)，[CC BY 4.0 全文](library/licenses/CC-BY-4.0.txt) | 原始 GIF 保留；抽帧 PNG、中文导读、练习及元数据明确为整理/改编 |
| Godot 4.5 文档正文、文档图与示例 | Juan Linietsky、Ariel Manzur 和 Godot 社区；个别图另署名 | [文档仓库许可声明](https://github.com/godotengine/godot-docs/blob/4.5/README.md#license)，[本地许可全文](library/licenses/godot-docs-4.5-LICENSE.txt) | HTML 主体转为 Markdown，图像本地化，增加中文任务导读；版本固定为 4.5 |
| Krita 文档与一般教学图片 | 各页 RST 元数据中列明的作者 | [许可证据](library/licenses/krita-licensing-evidence.md)，[GFDL 1.3 全文](library/licenses/GFDL-1.3.txt)；原页声明 1.3 或更新版本 | HTML 主体转换，保留透明可编辑的 Markdown/RST 与许可，增加中文导读与修改历史 |
| MAKE-001 中 Pepper & Carrot 相关示例 | David Revoy / deevad | 原文图旁独立标明 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | 保留图旁署名和来源；不套用 MIT 或其他图的许可 |
| UI-002 中 Tank Kings “Gear Up!” 截图 | Winterpixel Games | Godot 原文署名 “courtesy of Winterpixel Games”；随所在文档保留，其来源记录见 [UI-002](library/tutorials/game-development/UI-002-gui-theme-system.md) | 作为主题系统说明图引用；不能把文档许可记录解释成作者向本项目另行提供游戏素材包 |

关于各图的范围：本库按所在获许可文档保存教学说明图；若图旁列出不同作者、来源或独立许可，以该项声明为准。文档所示软件、游戏、商标和角色仍归各自权利人；本库不声称作者认可本项目。把截图中的角色、图标或界面裁出用于游戏，不能只靠此汇编的 MIT 许可。

## GFDL 文档的改编与源文件

Krita 各页与对应中文整理继续保留 GFDL 1.3 或更新版本声明。保留原作者列表、页面源 RST、原图、许可全文，以及每页的转换/中文补充历史。Markdown 与 RST 都是可修改的文本形式。下游如果分发修改版，应继续满足 GFDL 的署名、修改和许可保留要求，不得只附本仓库的 MIT 文件。

## 分发任务资料包

`scripts/task_bundle.py --copy-figures` 会附图源与许可记录，且把涉及的许可证文本带入资料包。该工具用于保留归属信息，不代表它已经替某个商业项目完成全部资产权利核验。新加入的外部案例只有在许可允许时才加入可离线分发的图片；仅做链接和评论的案例不算作已授权素材。

完整历史与说明见 [library/LICENSES.md](library/LICENSES.md)。
