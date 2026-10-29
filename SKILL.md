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
python3 scripts/task_bundle.py --task '制作四方向行走和待机角色' --style cozy-rural --out /tmp/pixel-task-brief
```

结果包含匹配原因、教程文件、原图/关键帧路径和授权。先读命中的中文任务导读，再读取需要的原文小节；打开实际配图核对，不能仅凭标题猜内容。资料包是工作输入，不是完成游戏或美术的证据。更多选项与数据格式见 [检索说明](references/retrieval.md)。

## 选择风格并固定项目规范

- 新项目或用户要求换风格：读取 [风格设计](references/style-design.md)，按任务选择配方；配置见 [美术风格](references/style-profiles.json) 与 [UI风格](references/ui-profiles.json)。这些是可调起点，不是硬件史事实、特定作者风格分类或统一适用的尺寸。
- 已有项目：先观察参考图与已有资产，记录实际的视角、光源、轮廓、色阶、像素密度和UI材质，再借用相符的教程。保留用户指定的风格。
- 用 [美术规范模板](assets/templates/art-bible.json) 固定共同规则和可接受的例外。场景规范应在批量角色/道具之前确定；同组素材不能各自改变视角、光源、锚点或像素倍率。
- 如需脚手架，运行 `python3 scripts/init_art_bible.py --style cozy-rural --ui-style wood-paper --out /tmp/pixel-art-bible`。它生成的是待项目化的方案，不会把未确定的参数伪装成已确认规格。

只按当前任务读取相关参考；不要把所有教程和所有风格JSON装入上下文。

## 制作素材或游戏

将检索结果转成实际产物：先做能验证视角、材质和尺度的小样，再扩展同组资产。需要图片生成时使用当前环境中可用、符合用户选择的图像工具；若安装了适用的像素资产流水线skill，可按其流程衔接。检索与检查功能本身无需生成服务。

- 新素材：记录逻辑画布、透明度、调色板、锚点、方向、帧时长和导出格式；图源教学例子只作为参考，不冒充新生成资产。
- 修复原图：先保存副本与同坐标对比，保持用户要求的构图、尺寸、必要孔洞和细杆。不要默认整图重绘、重新取色或按连通区域裁散素材。
- 游戏集成：匹配目标引擎版本；将绘画视角与实际遮挡、碰撞范围、动画状态、贴图过滤和屏幕倍率一起检查。原库Godot文档是4.5分支，不承诺任意版本相同。
- 原图教程已保留许可和署名；外发作品或教程改编时核对具体资产许可。教程中的示例图并不自动成为项目可分发素材包。

## 游戏UI设计

读取 [UI设计与验证](references/ui-design.md)，把界面材质与世界风格绑定，再明确任务、内容和交互。

需要真实界面参考时，运行 `python3 scripts/search.py --task '背包和商店UI' --kind case --json`，或读取 [6个游戏案例](references/ui-case-studies.md)。案例包含官方截图链接、可见事实、设计评析与局限；脚本不下载商业截图，`--copy-figures` 仅复制原教程的配图。必须打开所选截图再判断。风格关联只是借鉴维度，不意味着该游戏完整匹配配方；[内容审核](references/ui-content-audit.md)列明未覆盖的风格与验证缺口。

先用真实最长中文标签、价格/数量、图标与状态验证布局；文字应留在可变内容层，避免烘焙进装饰背景。九宫格需保留角部与像素网格；按钮、焦点、选中、禁用、空态和错误应有一致且可辨认的表示。复杂背包/商店信息确实需要时再增加面板结构，不把所有游戏UI套成网页仪表盘。

需要可运行UI时，交付并操作真实界面，检查键盘/手柄焦点、不同显示尺寸与关闭动作。仅有静态稿时明确它尚未验证交互。

## 一致性检查

先读 [检查方法与边界](references/consistency-review.md)，使用项目的明确规格配置 [机器检查合同](assets/templates/audit-contract.json)，按角色/文件覆盖不同尺寸要求。

```bash
python3 scripts/audit_assets.py /path/to/project/assets --contract /path/to/audit-contract.json --out /tmp/pixel-art-review
```

审查脚本依赖Pillow，其余检索与资料包脚本仅依赖Python标准库。需要时安装本skill的 `requirements.txt`。脚本只读取输入图片，输出测量报告和最近邻联系表，不自动修图。

必须分别报告：

- **机器证据**：尺寸、已指定的网格倍率、alpha、色板、边距和锚点等；未配置为`NOT_CONFIGURED`。
- **视觉证据**：打开联系表与原图，比较视角、光源、材质、轮廓节奏、色彩角色和场景融合。需要游戏/UI截图才能判断集成效果；缺少证据则记录`UNDETERMINED`。
- **问题与修正**：指出具体文件、局部区域、严重度和修复建议。修后用同样尺度对比，再复查受影响项。

机器通过不能替代美术通过。脚本的 `overall_status=NEEDS_VISUAL_REVIEW` 是明确边界，不把颜色数量相近或透明像素比例当成风格一致性证明。

## 交付给用户或下游agent

交付与当前请求相符的产物、风格/规格说明、用到的教程ID、图源、检查证据及仍未验证的内容。任务资料包可作为下游agent输入；创建新聊天、发消息或发布资源仍遵循用户授权，不由本skill默认代办。
