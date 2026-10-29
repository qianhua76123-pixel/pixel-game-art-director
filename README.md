# Pixel Game Art Director

给 AI agent 使用的像素游戏美术资料与制作辅助 skill：按任务检索教程和配图，建立共同美术规范，准备制作资料包，并检查已有素材的技术一致性。

优先服务俯视角像素游戏，也覆盖动画、素材工作流、Godot 集成和游戏 UI。**本库提供知识与检查工具；检索到教程、通过技术检查，都不等于已经做完游戏美术或验证了 UI。**

## 内容与范围

| 内容 | 数量 | 实际包含 |
|---|---:|---|
| 独立来源教程 | 92 篇 | 25 绘画、12 动画、27 素材制作、24 游戏开发、4 UI 专题 |
| 本地图像文件 | 661 个 | 原始教程图/GIF、截图和辅助抽帧；不等于 661 件可用游戏素材 |
| 美术风格配方 | 8 套 | 乡村、限色掌机、双色、街机、低饱和幻想、哥特、等距、霓虹 |
| UI 风格配方 | 6 套 | 木框纸面、紧凑掌机、醒目街机、幻想装饰、暗石铁器、全息终端 |
| 真实游戏 UI 案例 | 6 例 / 12 个截图链接 | 官方截图观察与原创评析；商业截图不打包为开放素材 |
| 任务路由 | 11 类 | 从场景、角色与动画，到 UI、引擎和已有素材审查 |

风格配方是整理者编写的可调参数建议。引用图用于讲解技法，**不是每种风格的完整成品示例**。四篇 UI 专题覆盖九宫格、Theme、容器布局和锚点；已有 HUD 与显示缩放资料可配合阅读。

- [Skill 入口](SKILL.md)：供 agent 按任务逐步读取。
- [完整教程目录](library/CATALOG.md)：逐篇查来源、许可、正文和配图。
- [风格设计](references/style-design.md) · [UI 设计与验证](references/ui-design.md)
- [真实游戏 UI 案例](references/ui-case-studies.md) · [UI 内容审核与缺口](references/ui-content-audit.md)
- [一致性检查方法](references/consistency-review.md) · [技术检查输出示例](examples/audit-demo/EXAMPLE.md)
- [来源与许可](THIRD_PARTY_NOTICES.md)：代码和第三方内容不是同一许可证。

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

## 验证与维护

```bash
python3 scripts/test_retrieval.py
python3 scripts/test_audit_assets.py
python3 scripts/test_ui_cases.py
```

发布前已检查本地链接、图像解码和哈希，并运行任务检索、资料包署名、搬迁路径与检查器行为测试。详细边界见 [验证报告](validation/FINAL.md)。这些检查不代表逐篇运行过原教程，也不代表已经验证某个游戏的真实 UI 交互。

[资料库维护说明](library/MAINTENANCE.md)介绍索引重建与采集。Godot 内容固定到 4.5 分支，Saint11 图源固定到提交 `ce1393eb2c46441d917134a9fd52e15575ee10a7`；版本快照不代表最新软件行为。

## 许可

原创脚本、技能编排、独立风格配方和测试夹具采用 [MIT](LICENSE)。第三方教程及其改编保留 **CC BY 4.0、CC BY 3.0、GFDL 1.3 或更新版本**等原许可。图片上的商标、游戏角色或署名截图不会因汇编进入此库而成为本项目原创资产。

再分发或改编资料时，保留对应作者、来源、许可和修改说明。详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [library/LICENSES.md](library/LICENSES.md)。
