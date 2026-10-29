# Pixel Game Art Director

给 AI agent 使用的像素游戏美术资料与制作辅助 skill：按任务检索教程和配图，建立共同美术规范，准备制作资料包，并检查已有素材的技术一致性。

优先服务俯视角像素游戏，也覆盖动画、素材工作流、Godot 集成和游戏 UI。**本库提供知识与检查工具；检索到教程、通过技术检查，都不等于已经做完游戏美术或验证了 UI。**

v1.3.1 重做乡村商店三方案的字体、边框和内容结构：上一版的视觉效果被用户明确否定，交互测试通过没有解决这个问题。本版保留 v1.3 的历史证据，重新提供界面审阅。教程库的 92 篇教程、661 个教学图像文件、既有 14 例 UI 案例，以及新增 4 例视觉一致性研究仍独立统计。

## 内容与范围

| 内容 | 数量 | 实际包含 |
|---|---:|---|
| 独立来源教程 | 92 篇 | 25 绘画、12 动画、27 素材制作、24 游戏开发、4 UI 专题 |
| 教程本地图像文件 | 661 个 | 原始教程图/GIF、截图和辅助抽帧；不等于 661 件可用游戏素材 |
| 美术风格配方 | 8 套 | 乡村、限色掌机、双色、街机、低饱和幻想、哥特、等距、霓虹 |
| UI 视觉主题配方 | 6 套 | 木框纸面、紧凑掌机、醒目街机、幻想装饰、暗石铁器、全息终端 |
| UI 设计维度 | 8 个轴 / 27 个可组合值 | 视觉表现、世界关系、空间位置、信息编码、密度、出现时机、时间策略、输入导航 |
| UI 系统模式 | 16 类 | 玩家决策、内容字段、结构、状态、输入、异常恢复和验收 |
| 真实游戏 UI 案例 | 14 例 / 28 个图像链接 | 分别标记官方截图、开发者设计稿、官方指南；商业图不打包为开放素材 |
| UI 与世界／素材一致性研究 | 4 例 / 8 个官方图像链接 | HLD、Children of Morta、Chained Echoes、DAVE THE DIVER；逐图观察、设计推论、迁移规则分开记录 |
| 乡村商店交互小样 | 3 个界面方案 | 共用中文商品、购买数量、余额、库存和背包数据；可切换正常、钱不足、满包和售罄状态 |
| 小样图像与字体 | 5 个 AI 示例 PNG / 1 个字体文件 | 共享场景、账本、商品图集、新朴素纸木面板及保留的旧框源图；Fusion Pixel 简体中文 WOFF2；与教程图像分开统计 |
| 设计研究与规范 | 22 个不同来源 | 原始研究、设计理论、平台指南、评估方法；保留适用范围与局限 |
| 任务路由 | 11 类 | 从场景、角色与动画，到 UI、引擎和已有素材审查 |

风格配方是整理者编写的可调参数建议。引用图用于讲解技法，**不是每种风格的完整成品示例**。四篇 UI 专题覆盖九宫格、Theme、容器布局和锚点；已有 HUD 与显示缩放资料可配合阅读。新增设计研究是原创综合说明，不计为新抓取的完整教程。八个设计轴与十六个系统是工作框架，不宣称为统一学术分类。

- [Skill 入口](SKILL.md)：供 agent 按任务逐步读取。
- [完整教程目录](library/CATALOG.md)：逐篇查来源、许可、正文和配图。
- [风格设计](references/style-design.md) · [UI 设计与验证](references/ui-design.md)
- [UI 研究图谱（HTML）](review/ui-design-atlas/index.html) · [设计基础与分类](references/ui-design-foundations.md) · [16 类系统模式](references/ui-system-patterns.md)
- [UI 评估方法](references/ui-evaluation-method.md) · [设计合同模板](assets/templates/ui-design-contract.json) · [乡村商店推演示例](examples/ui-design-reasoning.md)
- [真实游戏 UI 案例](references/ui-case-studies.md) · [UI 内容审核与缺口](references/ui-content-audit.md)
- [四组视觉一致性研究](references/visual-game-studies.md) · [结构化案例](references/visual-game-studies.json)
- [乡村商店可操作小样](examples/rural-shop-demo/README.md) · [小样主题合同](examples/rural-shop-demo/theme-contract.json)
- [一致性检查方法](references/consistency-review.md) · [技术检查输出示例](examples/audit-demo/EXAMPLE.md)
- [来源与许可](THIRD_PARTY_NOTICES.md)：代码和第三方内容不是同一许可证。

## UI 资料怎样用于实际设计

先说明玩家在当前情境要做的决定，再从系统模式提取真实内容字段与操作路径。随后独立选择拟物/平面等视觉表现、世界归属、屏幕或空间位置等维度，补齐成功、空、禁用、错误和恢复状态。最后按 [评估方法](references/ui-evaluation-method.md) 做静态检查、原型走查或用户任务观察，并记录证据等级。

例如，乡村商店可以使用纸质账本，也可以使用平面商品列表；两者都需要明确价格、数量、总价、余额与背包接收。详见 [同一个商店任务的三种表达](examples/ui-design-reasoning.md)。拟物不自动等于世界内界面，也不自动提升沉浸或可用性。

HTML 图谱可在下载后用浏览器打开；公开版本从原站加载参考图，完整分析和来源同时保存在 Markdown / JSON 中，agent 不依赖网页运行。

## 对比三个实际商店界面

[青禾种子铺](examples/rural-shop-demo/README.md) 使用真实中文文案与本地图像，可以选商品、修改数量、购买并检查余额、库存和行囊变化。三种表达共享交易数据；本版调整各方案的内容组织，不再只给同一张表单换底图：

| 方案 | 组织方式 | 小样截图 |
|---|---|---|
| 木框纸面 | 列表与详情同屏，使用朴素纸面与窄木边，取消原金色宝石角框 | [查看](examples/rural-shop-demo/screenshots/01-wood.jpg) |
| 柜台账本 | 左页选货，右页组织“本次购入”账目，将种植/使用条件改为精简真实摘要 | [查看](examples/rural-shop-demo/screenshots/02-ledger.jpg) |
| 世界与轻面板 | 店主入口配底部短交易窗；桌面最大宽 870px，3×2 商品格 | [查看](examples/rural-shop-demo/screenshots/03-world.jpg) |

![青禾种子铺：木框纸面](examples/rural-shop-demo/screenshots/01-wood.jpg)

![青禾种子铺：柜台账本](examples/rural-shop-demo/screenshots/02-ledger.jpg)

![青禾种子铺：世界与轻面板](examples/rural-shop-demo/screenshots/03-world.jpg)

主阅读层级收敛为身份标题 24px、决策重点 18px、正文 14px、辅助信息 12px。Fusion Pixel 用于店名等身份标题，商品、数值和说明主要采用系统中文字体；底部比较工具的个别文字为 10–12px，不属于游戏主阅读区。短名商品格保留完整可访问名称，详情继续显示商品全名。桌面预览按原生 1280×720 输出，窄屏审阅尺寸为 390×844；本次截图与运行证据见 [v1.3.1 审阅记录](validation/UI-REVISION-V1.3.1.md)。

小样由 HTML、CSS 与 ES modules 构成，需要本地 HTTP 服务。在仓库根目录运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

然后打开 <http://127.0.0.1:8000/examples/rural-shop-demo/>。这是商店交互对比原型，尚不是可漫游的完整游戏。仓库共保留五张 AI 示例图，旧 `wood-panel.png` 已退出当前界面；新 `plain-paper-panel.png` 使用源图 24px 切片与 8px 显示边框做九宫格。商品图集的**硬 alpha 检查仍失败**，统一逻辑网格仍待确定，重做 UI 没有使这些源图自动成为生产像素成品。来源、提示词与实测数据见 [原四图记录](examples/rural-shop-demo/assets/asset-provenance.json) 和 [新面板记录](examples/rural-shop-demo/assets/plain-panel-provenance.json)。

## 保持世界、素材和 UI 一致

全局 `theme_contract` 先规定项目身份、视角、光照、颜色职责、像素策略和字体，再由角色、道具、场景与 UI 继承。**禁止每件资产另选一套画风。** 不同任务可以使用不同面板家族，但例外必须记录理由、适用范围、继承关系和审阅证据；不能用例外豁免硬 alpha 等生产门槛。

[四组视觉研究](references/visual-game-studies.md) 提供可迁移的组织方法，不提供可直接使用的商业游戏素材。`validate_theme_contract.py` 检查合同结构、引用、资产绑定和已记录证据；它不会自动看图判断美术是否统一。结构通过不等于视觉通过，待定与已失败事项必须继续保留。

## 看看现有教学图

### 俯视房屋与场景

![Saint11 俯视房屋教学原图](library/assets/drawing/ART-008/Top-Down-Houses-Compressed.gif)

Pedro Medeiros / Saint11，[*Top-Down Houses*](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/Top-Down-Houses-Compressed.gif)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。原图原样保存；[对应中文导读](library/tutorials/drawing/ART-008-top-down-houses.md)为整理改编。

### UI 九宫格的结构

![Saint11 UI 九宫格教学原图](library/assets/supplement/UI-001/UI-9-Slice.gif)

Pedro Medeiros / Saint11，[*UI 9-Slice*](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/UI-9-Slice.gif)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。这张图说明可缩放边框的原理，不代表六种 UI 配方的最终视觉效果。

## 安装与调用

将此仓库完整复制到 agent 的 skills 目录，保留所有相对路径。例如 Codex 可使用 `~/.codex/skills/pixel-game-art-director/`，入口为 `SKILL.md`。不要只复制入口文件。客户端需要重新读取技能目录时，开启新会话。

可直接向 agent 发出任务：

> 用 $pixel-game-art-director 为乡村俯视游戏检索房屋、树木和水岸教程，建立共同视角、光源和像素密度规范，再制作小样。

> 用 $pixel-game-art-director 设计暗黑背包 UI，检查最长中文名称、焦点、选中和禁用状态。

完整说明见 [INSTALL.md](INSTALL.md)。没有技能自动发现功能的 agent，也可以直接读取入口和运行下面的脚本。

## 命令行

从仓库根目录执行；检索与资料包功能仅需 Python 3.9+ 标准库。

```bash
python3 scripts/search.py --task '俯视农舍、树木和草地' --limit 6 --json
python3 scripts/search.py --task '暗黑背包UI' --kind all --style dark-gothic --ui-style dark-stone --json
python3 scripts/search.py --id ART-008 --json
python3 scripts/search.py --task '背包和商店UI' --kind case --json
python3 scripts/search.py --task '经营餐厅 拟物小游戏 一致性研究' --kind visual-case --json
python3 scripts/search.py --task '制作配方界面' --kind system --json
python3 scripts/search.py --task '拟物化菜单' --kind axis --json
python3 scripts/search.py --id shop-trade --json
python3 scripts/search.py --list ui-axes --json
python3 scripts/search.py --list visual-cases --json
python3 scripts/task_bundle.py --task '乡村地图的房屋和植被' --style cozy-rural --out ../pixel-output/village-brief --copy-figures
python3 scripts/init_art_bible.py --style cozy-rural --ui-style wood-paper --out ./outputs/village-art-bible
```

资料包保留教程 ID、来源、许可和配图归属；美术规范初稿不会把建议色板或未知尺寸变成已经确认的硬性规则。

检查已有图片需要 Pillow：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/audit_assets.py /path/to/project/assets --contract /path/to/audit-contract.json --out ./outputs/asset-review
```

检查器只读取输入图片，输出报告和最近邻联系表。没有配置的规则显示 `NOT_CONFIGURED`；缺少完整技术证据时显示 `INCOMPLETE`。机器结果无论通过与否，整体都仍标记 `NEEDS_VISUAL_REVIEW`，因为视角、光源、材质、轮廓节奏与场景融合需要看图判断。

检查示例主题合同：

```bash
python3 scripts/validate_theme_contract.py examples/rural-shop-demo/theme-contract.json --json
```

退出码 `0` 表示记录完整且没有失败项，`1` 表示结构错误或已记录的硬门槛失败，`2` 表示决策／证据未完成。当前小样包含明确的生产失败，不能把非零退出码改写为总体美术通过。

## 验证与维护

```bash
python3 scripts/test_retrieval.py
python3 scripts/test_audit_assets.py
python3 scripts/test_ui_cases.py
python3 scripts/test_ui_design.py
```

本次字体、布局与边框重做的证据和未完成项见 [v1.3.1 审阅记录](validation/UI-REVISION-V1.3.1.md)。[v1.3.0 历史报告](validation/SHOP-COHESION-V1.3.md) 继续保留，不能把其测试结果当作重做版的审阅证据，也不能用测试通过数量证明美术质量。v1.2.0 的设计研究与脚本验证见 [此前版本报告](validation/UI-DESIGN-V1.2.md)；既有教程与素材检查见 [验证报告](validation/FINAL.md)。结构校验、交易测试、实际运行截图和用户视觉反馈分别记录。

[资料库维护说明](library/MAINTENANCE.md)介绍索引重建与采集。Godot 内容固定到 4.5 分支，Saint11 图源固定到提交 `ce1393eb2c46441d917134a9fd52e15575ee10a7`；版本快照不代表最新软件行为。

## 许可

原创脚本、技能编排、独立风格配方和测试夹具采用 [MIT](LICENSE)。第三方教程及其改编保留 **CC BY 4.0、CC BY 3.0、GFDL 1.3 或更新版本**等原许可。图片上的商标、游戏角色或署名截图不会因汇编进入此库而成为本项目原创资产。

商店的五张 AI 示例图仅在项目实际持有权利的范围内按 MIT 提供，不保证独占性、唯一性或独立版权保护。Fusion Pixel 字体仍采用 **SIL OFL 1.1**，保留字体本身和上游组件的原始声明；字体不随示例代码改为 MIT。视觉研究的商业原图仅引用官方远程链接，不纳入本库开放许可或离线素材包。

再分发或改编资料时，保留对应作者、来源、许可和修改说明。详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [library/LICENSES.md](library/LICENSES.md)。
