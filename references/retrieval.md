# 按任务检索教程、UI系统、主题一致性与图示

本页说明离线检索命令。脚本从自身位置定位 `library/`，不依赖原素材盘、不需要联网或第三方Python包。运行时的当前目录不影响检索；把整个skill文件夹复制到另一台机器后仍可使用。

## 检索

以下命令假设当前目录是skill根目录；其他目录下使用脚本的实际绝对路径。

```bash
python3 scripts/search.py --task '做南方乡村俯视像素游戏，需要农舍、树木和草地地图' --limit 6 --json
python3 scripts/search.py '给村民做四方向行走和待机动画' --images 1
python3 scripts/search.py --task '设计暗黑奇幻背包UI，九宫格面板与手柄焦点' --kind all --style dark-gothic --ui-style dark-stone --json
python3 scripts/search.py --id ART-008 --json
python3 scripts/search.py --list styles --json
python3 scripts/search.py --list ui-styles --json
python3 scripts/search.py --task '商店比较种子，选择数量并购买' --kind system --details --json
python3 scripts/search.py --id shop-trade --details --json
python3 scripts/search.py --list systems --json
python3 scripts/search.py --task '拟物账本，世界内界面与屏幕叠加' --kind axis --json
python3 scripts/search.py --id visual-treatment --json
python3 scripts/search.py --list ui-axes --json
python3 scripts/search.py --task '背包和商店UI' --kind case --json
python3 scripts/search.py --id UI-CASE-003 --json
python3 scripts/search.py --list cases --json
python3 scripts/search.py --task '世界场景与UI的材质和图标一致性' --kind visual-case --json
python3 scripts/search.py --id ART-CASE-001 --json
python3 scripts/search.py --list visual-cases --json
python3 scripts/search.py --task '小屏掌机风格' --kind style --details --json
```

长中文描述直接输入即可。检索器从本地主题词、精选任务路线和教程元数据识别概念，不要求空格分词；它不是语义向量模型。没有命中时返回 `status: no_match`，不会把任意六篇教程填充成答案。

| 参数 | 行为 |
|---|---|
| 位置参数或 `--task` | 自然语言任务，`--task`优先 |
| `--kind tutorial/style/ui/case/visual-case/system/axis/all` | 默认教程；`ui`为视觉主题，`case`为UI案例，`visual-case`为世界/素材/UI跨角色画面研究，`system`为系统任务模式，`axis`为设计维度；`all`合并相关结果 |
| `--style ID`、`--ui-style ID` | 明确风格约束；不存在的ID返回错误，不静默改成别的风格 |
| `--id ID` | 直接查询教程、风格、案例、系统模式或设计维度；`UI-CASE-003` 是UI案例，`ART-CASE-001` 是跨角色画面研究，`shop-trade` 是系统，`visual-treatment` 是维度 |
| `--list styles/ui-styles/cases/visual-cases/systems/ui-axes/routes` | 列出配方、14个UI案例、4个画面研究、16类系统、8个维度或任务路线，不加载配图，也不自动选择 |
| `--limit N` | 默认6，范围1–30；`all`下教程最多N个，风格/UI主题各最多2、系统最多3、维度最多2；相关UI任务另附最多3个UI案例，有画面研究意图时另附最多3个 `visual-case`；不是总结果数上限 |
| `--images N` | 每个结果最多配图数，默认2，范围0–5；优先原图和关键帧，避免把全库图片输出到上下文 |
| `--fulltext` | 在主题检索基础上补充正文匹配，仍不是向量检索 |
| `--details` | 风格结果补充参数、混用风险和视觉检查；系统结果补充信息结构、组件、状态、输入、恢复、视觉取舍和验收条件 |
| `--json` | 机器可读结果；失败时也输出JSON并返回退出码2 |

结果包括匹配原因、真实Markdown路径、图片路径与说明、原作者、许可和来源。相对路径相对于skill根目录；`absolute_path`在本次运行时生成。部分教学图是动画，静态关键帧不能替代完整时序。

UI任务先查 `system`，确定玩家决策与必须内容，再查 `axis` 比较视觉、世界归属、空间、表意、注意需求、出现方式、时间和输入。系统是编辑综合，维度是允许交叉的工作框架；均不是质量排名或官方穷尽分类。`axis` 返回维度定义和全部候选 `values`，不会替项目选值。六套 `ui` 配方只是视觉主题，不能替代上述决定。

系统结果的 `required_content`、`source_ids` 和关联教程可帮助收窄阅读；完整行为请用 `--details`。维度与系统的依据分别在 [设计基础来源](ui-foundation-sources.json)和 [系统规范来源](ui-system-sources.json)，先核对每条来源的适用范围。对应MD可能较长，按命中的ID/名称定位相关段落，不必整份装入上下文。

案例结果的 `figures` 是远程官方截图、设计稿或指南配图链接，按 `evidence_type` 区分，标记 `remote_only: true`，没有本地图像 `absolute_path`。`source_url` 指向图本身，`source_page` 指向官方页面。离线可检索元数据，但查看图需联网。不能因为风格参数命中就推断整套设计同款；UI案例优先阅读 `summary`、`limitations` 和 `editorial_notice`。

`visual-case` 独立收录4例/8张官方远程图，见 [画面研究](visual-game-studies.md)。结果分别提供 `observed`、`design_inferences`、`cohesion_rules`、`exceptions_and_limits` 与 `transfer_to_rural_game`，用于区分可见事实、设计推论和迁移规则；`absolute_path` 指向原创分析MD，`absolute_registry_path` 指向本地元数据，均不是商业原图路径。按返回的 `anchor` 定位案例，不把整篇研究装入每次任务。

风格候选是建议，不是自动锁定。已有项目美术规范优先；显式 `--style` / `--ui-style` 只代表本次调用指定了配方，可能来自agent提案；是否为用户选择以会话为准，不构成用户批准全部参数的证据。若任务表达了“不要暗黑”等直接否定，候选检索会排除对应线索，但复杂否定仍需agent自行核对。

执行顺序是项目主题 → 对应role及有据覆盖 → 单资产例外 → 兼容的教程与制作方法。先读取实际项目 [主题合同](theme-cohesion-contract.md)，再使用候选；不能因为每次检索都得到新候选，就为按钮、树木和商品各换一种风格。

## 生成可执行任务简报

```bash
python3 scripts/task_bundle.py --task '做一套乡村俯视农舍、树木和草地' --style cozy-rural --out /tmp/village-art-brief
python3 scripts/task_bundle.py --task '暗黑背包UI，九宫格面板、选中与禁用状态' --style dark-gothic --ui-style dark-stone --limit 8 --copy-figures --out /tmp/inventory-ui-brief
```

输出：

- `task-brief.md`：任务、选定/候选风格、核心阅读、配图、具体制作路线、验收点和来源。
- `task-brief.json`：相同信息的机器结构，保留每个教程与图的真实路径、适用版本及许可。
- 使用 `--copy-figures` 时增加 `figures/`、对应的 `licenses/` 和 `figure-attributions.json`，复制选定教学图并记录逐图出处、许可与SHA-256。
- UI任务的简报包含命中的 `ui_system_patterns`、`ui_design_axes` 与 `ui_case_references`：分别供任务/内容设计、维度比较和画面观察。数组为空表示本次没有匹配，不表示系统没有需求或项目已作出选择。
- `visual_game_references` 保存命中的跨角色画面研究；为空表示本次未匹配，不把任意研究填入任务。
- `theme_cohesion` 始终提供主题说明、模板、继承顺序和验证命令；`project_contract_status: NOT_LOADED` 明确表示脚本尚未读取实际项目合同。它是下游agent的执行入口，不是主题验收报告。
- 商业案例配图是官方外链，不会被 `--copy-figures` 下载或复制，也不能当作成品游戏素材；只复制已选教学图并保留授权记录。

默认输出8篇核心阅读，可用 `--limit`调整。不同任务使用不同制作步骤和验收条件；没有路线时明确指出缺口，不编造已验证流程。输出目录必须在skill目录之外，保持知识包只读；对相同输出目录重新执行会更新同名简报，复制图像如有旧文件需自行管理。

这些输出供agent继续制作、实现或审查；脚本本身不生成游戏资产，不调用收费服务，不修改输入美术，也不证明某个画风或UI已经通过检验。教学图片必须与实际项目资产区分，不能直接把整张教程图当作可交付的游戏素材。

## 推荐读取策略

先加载项目主题与资产用途，再看检索结果摘要，按ID打开相关MD的中文导读、配图与原文小节。处理自然语言任务时，原文可带引擎版本和工具前提；按目标环境核对后再执行。涉及一致性时继续读 [一致性审阅](consistency-review.md)：`validate_theme_contract.py` 仅检查合同结构、继承引用与已记录证据，`audit_assets.py` 按另一份测量合同检查图片。主题结构通过不能证明视觉一致，未定参数和未审画面分别保留 `INCOMPLETE` / `UNDETERMINED`。

UI制作按需读取 [系统模式](ui-system-patterns.md) → [设计基础](ui-design-foundations.md) → [制作与验证](ui-design.md)，把本次决定写入 [UI设计合同](../assets/templates/ui-design-contract.json)。审查时读 [证据协议](ui-evaluation-method.md)，不要把检索匹配分数当作设计质量或用户测试结果；不清楚怎样组合时可看 [乡村商店推演](../examples/ui-design-reasoning.md) 和 [三个可运行小样](../examples/rural-shop-demo/README.md)。小样图集存在软alpha，严格硬alpha检查失败；可运行界面不是原生像素素材已生产合格的证明。

任务路由维护在 [task-routing.json](task-routing.json)。新增教程只需进入 `library/catalog.json`，即可参与元数据匹配；加入精选任务路线可以提高复杂请求的命中稳定性。没有对应ID的可选教程被跳过，不会生成假文件路径。
