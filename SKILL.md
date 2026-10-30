---
name: pixel-game-art-director
description: 按任务检索本地图文教程和配图，用于像素游戏、场景、角色动画、素材制作和游戏UI设计；选择或匹配美术风格，建立项目美术规范，检查像素技术规格与成组素材/UI的视觉一致性。适用于制作、改图或美术审查，不将教程图直接当作游戏成品素材。
---

# Pixel Game Art Director

把用户任务转成可执行的美术与制作方案，再使用相关教程和图像完成工作。知识库位于本skill的 `library/`；检索脚本按自身位置定位，可整体搬迁，不依赖原素材盘。

## 按任务取资料

先确认用户要交付的对象：场景、单件素材、动画、游戏UI、引擎集成，或已有素材审查。已有项目/参考图优先于预设；能从上下文确定的尺寸、视角、引擎和风格无需重复询问。

从本skill目录执行以下命令，或使用脚本的绝对路径：

```bash
python3 scripts/search.py --task '俯视乡村地图，需要农舍、树木和水岸' --limit 6 --json
python3 scripts/search.py --task '暗黑背包UI，九宫格边框和手柄焦点' --kind all --style dark-gothic --ui-style dark-stone --json
python3 scripts/search.py --id ART-008 --json
python3 scripts/search.py --task '世界场景与UI的材质和图标一致性' --kind visual-case --json
python3 scripts/task_bundle.py --task '制作四方向行走和待机角色' --style cozy-rural --out /tmp/pixel-task-brief
```

结果包含匹配原因、教程文件、原图/关键帧路径和授权。先读命中的中文任务导读，再读取需要的原文小节；打开实际配图核对，不能仅凭标题猜内容。资料包是工作输入，不是完成游戏或美术的证据。更多选项与数据格式见 [检索说明](references/retrieval.md)。

## 先继承项目主题，再选择制作方法

- 先读 [主题继承规则](references/theme-cohesion-contract.md)，加载项目的主题 ID、版本、参考资产与 [主题合同](assets/templates/theme-contract.json)。继承顺序是项目主题 → `world/character/item-icon/UI/typography` 用途规则 → 有理由和证据的单资产例外；不能为每张素材重新选择色板、光源、投影或画风。
- 新项目或用户要求换风格：读取 [风格设计](references/style-design.md)，先为整个项目比较候选，再确定用途差异；配置见 [美术风格](references/style-profiles.json) 与 [UI风格](references/ui-profiles.json)。这些是可调起点，不是硬件史事实、特定作者风格分类或统一适用的尺寸。
- 已有项目：先观察参考图与已有资产，记录实际的视角、光源、轮廓、色阶、像素密度和UI材质，再借用相符的教程。保留用户指定的风格。
- 用 [美术规范模板](assets/templates/art-bible.json) 固定共同规则和可接受的例外。场景规范应在批量角色/道具之前确定；同组素材不能各自改变视角、光源、锚点或像素倍率。
- 如需脚手架，运行 `python3 scripts/init_art_bible.py --style cozy-rural --ui-style wood-paper --out /tmp/pixel-art-bible`。它生成的是待项目化的方案，不会把未确定的参数伪装成已确认规格。

需要跨场景、角色、图标与UI的实际画面依据时，检索 `--kind visual-case` 或读 [4组视觉研究与8张官方远程图](references/visual-game-studies.md)。分别阅读可见事实、设计推论和迁移规则；相同身份与状态语义可以跨尺度保留，不要求所有用途同尺寸、同细节密度。图像仅作研究，不是可分发素材。

只按当前任务读取相关参考；不要把所有教程和所有风格JSON装入上下文。

## 制作素材或游戏

将检索结果转成实际产物：先做能验证视角、材质和尺度的小样，再扩展同组资产。需要图片生成时使用当前环境中可用、符合用户选择的图像工具；若安装了适用的像素资产流水线skill，可按其流程衔接。检索与检查功能本身无需生成服务。

- 新素材：记录逻辑画布、透明度、调色板、锚点、方向、帧时长和导出格式；图源教学例子只作为参考，不冒充新生成资产。
- 修复原图：先保存副本与同坐标对比，保持用户要求的构图、尺寸、必要孔洞和细杆。不要默认整图重绘、重新取色或按连通区域裁散素材。
- 游戏集成：匹配目标引擎版本；将绘画视角与实际遮挡、碰撞范围、动画状态、贴图过滤和屏幕倍率一起检查。原库Godot文档是4.5分支，不承诺任意版本相同。
- 原图教程已保留许可和署名；外发作品或教程改编时核对具体资产许可。教程中的示例图并不自动成为项目可分发素材包。

## 游戏UI设计

读取 [UI设计与验证](references/ui-design.md)。先确定玩家要做的决定和系统规则，检索 [16类系统模式](references/ui-system-patterns.md)，整理必须同时看见的对象、成本、条件、效果与后果，再组织界面。可运行 `python3 scripts/search.py --task '乡村商店，比较种子并选择购买数量' --kind system --details --json`。

需要选择或比较设计方向时，读 [设计基础与八个维度](references/ui-design-foundations.md)：分别决定视觉语言、虚构世界关系、空间位置、信息表征、注意需求、出现方式、世界时间与输入。六套旧UI配方只是视觉主题；木框不自动等于世界内UI，拟物也不决定系统内容。用 [UI设计合同](assets/templates/ui-design-contract.json)记录本次选择、真实内容、状态、输入和失败恢复；[乡村商店推演](examples/ui-design-reasoning.md)说明取舍，[三个可运行小样](examples/rural-shop-demo/README.md)用相同中文商品、图集与交易数据比较结构。

需要真实界面参考时，运行 `python3 scripts/search.py --task '背包和商店UI' --kind case --json`，或读取 [14个游戏案例与28张官方配图链接](references/ui-case-studies.md)。打开所选截图，分别记录画面事实、设计评析与未验证项；风格关联不表示整套游戏同款。脚本不下载商业截图，`--copy-figures` 仅复制教学配图，案例图不能直接当作游戏素材；覆盖范围见 [内容审核](references/ui-content-audit.md)。

商店任务优先看 [真实商店并排与原图局部](review/shop-benchmark/README.md)：Pierre 的买种菜单和 Moonlighter 的药水商人服务，不能把对白或背包截图当成商店证据。按构图、文字、素材、可见像素簇逐项比较；缩略全图只评布局，颗粒看原尺寸局部。随后为整套资产固定一种方向，重做共同母版与实际界面；[v2实例](examples/rural-shop-demo/art-direction-v2.md)使用同母版的店主与六商品、续作柜台与面板，以及统一逻辑舞台。渲染网格统一和源素材原生网格合格是两个结论。

先用最长真实中文、数值和边界状态验证布局，再制作装饰；文字保留为可变内容层，九宫格保留角部与像素网格。按 [UI审查协议](references/ui-evaluation-method.md)分别检查任务、信息、交互、视觉与技术证据。可运行UI实际走完打开、选择、执行/取消、恢复路径；静态稿不能证明焦点、可用性或沉浸感，未测项目保留 `UNDETERMINED`。

检查实际成图的主次：装饰不得压过商品/角色，像素字体不承担所有文字层级，框体和图标应共享可解释的抽象程度。拟物账本要按货目与购入记录组织信息；轻界面要实际减少遮挡和常驻内容。视觉不合格时重做构图与层级，不能用真实文案、生成图、功能测试或合同完整来宣布视觉完成；未售商品在格子层也须有可见状态。

## 一致性检查

先读 [检查方法与边界](references/consistency-review.md)。先验证主题合同的继承与引用，再使用项目的明确规格配置 [机器检查合同](assets/templates/audit-contract.json)，按角色/文件覆盖不同尺寸要求。这是两种合同，不能互换。

```bash
python3 scripts/validate_theme_contract.py /path/to/project/theme-contract.json --json
python3 scripts/audit_assets.py /path/to/project/assets --contract /path/to/audit-contract.json --out /tmp/pixel-art-review
```

`validate_theme_contract.py` 只核对结构、主题/role引用、来源及已记录证据，未定关键参数保留 `INCOMPLETE`，不自动鉴定画风。`audit_assets.py` 依赖Pillow，检索、资料包和主题验证器仅依赖Python标准库。需要时安装本skill的 `requirements.txt`；图片审查只读取源图，不自动修图。

必须分别报告：

- **机器证据**：尺寸、已指定的网格倍率、alpha、色板、边距和锚点等；未配置为`NOT_CONFIGURED`。
- **视觉证据**：打开联系表与原图，比较视角、光源、材质、轮廓节奏、色彩角色和场景融合。需要游戏/UI截图才能判断集成效果；缺少证据则记录`UNDETERMINED`。
- **问题与修正**：指出具体文件、局部区域、严重度和修复建议。修后用同样尺度对比，再复查受影响项。

机器通过不能替代美术通过。脚本的 `overall_status=NEEDS_VISUAL_REVIEW` 是明确边界，不把颜色数量相近或透明像素比例当成风格一致性证明。

当前商店小样改用三张同源风格的新PNG，详见 [v2主题合同](examples/rural-shop-demo/theme-contract-v2.json)。原始母版仍有部分透明像素，源图原生网格与严格有限色板尚未通过；640×360逻辑采样和整数显示不改写这些源素材结论。历史五张PNG与旧合同保留为旧版证据，不能当作当前图像或以新截图背书。

## 交付给用户或下游agent

交付与当前请求相符的产物、风格/规格说明、用到的教程ID、图源、检查证据及仍未验证的内容。任务资料包可作为下游agent输入；创建新聊天、发消息或发布资源仍遵循用户授权，不由本skill默认代办。
