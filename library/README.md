# 像素游戏、制作与绘画教程库

收集日期：**2026-10-29**。共 **92 篇独立来源教程**，均衡覆盖像素绘画、动作动画、素材制作和游戏开发，优先支持俯视角游戏。

- **先找教程：** [总目录](CATALOG.md)
- **交给其他 agent：** [阅读与检索说明](AGENT_README.md)
- **按目标学习：** [六条学习路线](LEARNING_PATHS.md)
- **直接导入检索系统：** [catalog.json](catalog.json)、[catalog.jsonl](catalog.jsonl)、[chunks.jsonl](chunks.jsonl)
- **核对交付：** [验证报告](qa/VALIDATION.md)、[来源与许可](LICENSES.md)

## 包含什么

| 分组 | 篇数 | 内容 |
|---|---:|---|
| 像素绘画与场景 | 25 | 像素簇、轮廓、光影、俯视房屋、室内、树木草地、水、岩石、木材、金属等 |
| 角色与动作动画 | 12 | 侧视/俯视行走跑步、攻击、待机、跳跃、缓动、循环、亚像素、挤压与拖影 |
| 素材制作工作流 | 27 | Krita图层、选区、调色板、平铺纹理、动画时间轴、洋葱皮、导入导出等 |
| 游戏开发与引擎 | 24 | Godot场景与输入、完整2D小游戏系列、俯视移动、碰撞、TileSet/TileMapLayer、灯光、清晰缩放等 |
| 游戏UI与界面设计 | 4 | 九宫格、主题资源、容器布局、HUD锚点与界面状态 |

当前清单登记 **661 个本地图像文件**，包含原始教学图/GIF以及辅助抽帧；抽帧不计为新教程。同一主题的原图与关键帧也不重复计入篇数。正文约 **1.14 MiB Markdown**，不包含图片大小。

## 阅读示例

### 俯视房屋与场景

[ART-008 · 俯视斜视角房屋：从体块到屋顶材质](tutorials/drawing/ART-008-top-down-houses.md)、[ART-011 · 树冠：剪影、体积与有节制的叶片纹理](tutorials/drawing/ART-011-vegetation-volume.md)、[ART-010 · 俯视场景的脚底排序、复杂遮挡与碰撞投影](tutorials/drawing/ART-010-top-down-depth-sorting.md)。

![Saint11俯视房屋教程原图，CC BY 4.0](assets/drawing/ART-008/Top-Down-Houses-Compressed.gif)

图源：Pedro Medeiros（Saint11），[固定来源](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/Top-Down-Houses-Compressed.gif)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。中文步骤在对应MD中，原始GIF原样保存。

### 四方向角色与游戏接入

[ANIM-003 · 俯视行走：六帧周期与四方向遮挡](tutorials/animation/ANIM-003-top-down-walk.md) → [ANIM-004 · 俯视跑步：层叠体块、腾空与恢复](tutorials/animation/ANIM-004-top-down-run.md) → [DEV-013 · 把角色帧图和精灵表接成二维动画](tutorials/game-development/DEV-013-sprite-animation.md) → [DEV-012 · 俯视角色的八向移动、朝向与点击移动](tutorials/game-development/DEV-012-top-down-movement.md)。

![Saint11俯视行走教程原图，CC BY 4.0](assets/animation/ANIM-003/TopDownWalkCycle.gif)

图源：Pedro Medeiros（Saint11），[固定来源](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/TopDownWalkCycle.gif)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。

## 每篇怎么组织

像素绘画与动画篇以作者原始图片教程为依据，提供中文概念、步骤、图示读法、本地原图与关键帧，再附练习和验收。它们是人工读图整理，不声称逐字OCR。

Krita与Godot篇提供中文任务导读、具体操作路线、练习、验收与版本说明，并保留获许可的英文主内容、代码、表格和教学图。**中文导读不等于整篇英文逐句翻译。** 未收录的外部延伸网页仍以链接引用。

Godot文档固定为 **4.5分支**；Krita抓取页面标注 **Manual 5.3.0**，这是文档快照标识，不声称已验证本机软件功能。Saint11固定到仓库提交 `ce1393eb2c46441d917134a9fd52e15575ee10a7`。

## 本地搜索

```bash
python3 tools/search.py '俯视 房屋' --top 5
python3 tools/search.py '行走' --category animation --json
python3 tools/search.py 'TileMapLayer' --fulltext
```

普通阅读无需安装软件；`search.py`只用Python标准库。重建索引或继续采集参见 [维护说明](MAINTENANCE.md)。

## 完成范围

这是可以离线阅读主体图文的教程库，不是已经逐篇运行验证的游戏工程。保留了作者、来源、许可和整理边界；未将付费视频或未观看的视频伪称为已转录教程。少量无明确全文许可的参考材料列在延伸阅读中，不计入以上篇数。
