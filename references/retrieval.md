# 按任务检索教程、风格与图示

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
python3 scripts/search.py --task '背包和商店UI' --kind case --json
python3 scripts/search.py --id UI-CASE-003 --json
python3 scripts/search.py --list cases --json
python3 scripts/search.py --task '小屏掌机风格' --kind style --details --json
```

长中文描述直接输入即可。检索器从本地主题词、精选任务路线和教程元数据识别概念，不要求空格分词；它不是语义向量模型。没有命中时返回 `status: no_match`，不会把任意六篇教程填充成答案。

| 参数 | 行为 |
|---|---|
| 位置参数或 `--task` | 自然语言任务，`--task`优先 |
| `--kind tutorial/style/ui/case/all` | 默认教程；`case`返回真实游戏案例；`all`返回教程、最多各2个风格候选，UI任务另附最多3个案例 |
| `--style ID`、`--ui-style ID` | 明确风格约束；不存在的ID返回错误，不静默改成别的风格 |
| `--id ID` | 直接查询一个教程、风格或案例的元数据 |
| `--list styles/ui-styles/cases/routes` | 列出可用配方、案例或任务路线，不加载配图，也不自动选择 |
| `--limit N` | 默认6，范围1–30；`all`下控制教程数，风格候选各不超过2 |
| `--images N` | 每个结果最多配图数，默认2，范围0–5；优先原图和关键帧，避免把全库图片输出到上下文 |
| `--fulltext` | 在主题检索基础上补充正文匹配，仍不是向量检索 |
| `--details` | 风格结果额外返回参数、混用风险和视觉检查项 |
| `--json` | 机器可读结果；失败时也输出JSON并返回退出码2 |

结果包括匹配原因、真实Markdown路径、图片路径与说明、原作者、许可和来源。相对路径相对于skill根目录；`absolute_path`在本次运行时生成。部分教学图是动画，静态关键帧不能替代完整时序。

案例结果的 `figures` 是远程官方截图链接，标记 `remote_only: true`，没有本地 `absolute_path`。`source_url` 指向图本身，`source_page` 指向官方页面。离线可检索元数据，但查看图需联网。不能因为风格参数命中就推断整套设计同款；优先阅读 `summary`、`limitations` 和 `editorial_notice`。

风格候选是建议，不是自动锁定。已有项目美术规范优先；显式 `--style` / `--ui-style` 只代表本次调用指定了配方，可能来自agent提案；是否为用户选择以会话为准，不构成用户批准全部参数的证据。若任务表达了“不要暗黑”等直接否定，候选检索会排除对应线索，但复杂否定仍需agent自行核对。

## 生成可执行任务简报

```bash
python3 scripts/task_bundle.py --task '做一套乡村俯视农舍、树木和草地' --style cozy-rural --out /tmp/village-art-brief
python3 scripts/task_bundle.py --task '暗黑背包UI，九宫格面板、选中与禁用状态' --style dark-gothic --ui-style dark-stone --limit 8 --copy-figures --out /tmp/inventory-ui-brief
```

输出：

- `task-brief.md`：任务、选定/候选风格、核心阅读、配图、具体制作路线、验收点和来源。
- `task-brief.json`：相同信息的机器结构，保留每个教程与图的真实路径、适用版本及许可。
- 使用 `--copy-figures` 时增加 `figures/`、对应的 `licenses/` 和 `figure-attributions.json`，复制选定教学图并记录逐图出处、许可与SHA-256。
- UI任务的简报另含 `ui_case_references` 与官方截图链接；商业案例图片不会被 `--copy-figures` 下载或复制。

默认输出8篇核心阅读，可用 `--limit`调整。不同任务使用不同制作步骤和验收条件；没有路线时明确指出缺口，不编造已验证流程。输出目录必须在skill目录之外，保持知识包只读；对相同输出目录重新执行会更新同名简报，复制图像如有旧文件需自行管理。

这些输出供agent继续制作、实现或审查；脚本本身不生成游戏资产，不调用收费服务，不修改输入美术，也不证明某个画风或UI已经通过检验。教学图片必须与实际项目资产区分，不能直接把整张教程图当作可交付的游戏素材。

## 推荐读取策略

先看检索结果摘要，再按ID打开相关MD的中文导读、配图与原文小节。处理自然语言任务时，原文可带引擎版本和工具前提；按目标环境核对后再执行。涉及一致性时继续读 [一致性审阅](consistency-review.md)，以实际素材和项目合同测量；风格判断仍需要看图。

任务路由维护在 [task-routing.json](task-routing.json)。新增教程只需进入 `library/catalog.json`，即可参与元数据匹配；加入精选任务路线可以提高复杂请求的命中稳定性。没有对应ID的可选教程被跳过，不会生成假文件路径。
