# Tiled 场景地图补充阅读导航

核验日期：2026-10-29。以下是 14 个已成功访问的官方页面，仅提供短导读与链接，不计入 24 篇 Krita 完整图文教程。

## 为什么这里保留导航

本次检查了 Tiled 官网页脚、仓库 `COPYING`、文档目录和 README：`COPYING` 列明软件部分的 GPL/BSD；TMX 格式参考页明确注明 CC BY-SA 3.0，但没有查到可明确覆盖整部用户手册的统一再发布声明。因此这里没有复制整部 Tiled 手册正文或教学截图，也没有把软件许可证套用到手册。可从下列原站链接继续阅读。

- [仓库 COPYING](https://github.com/mapeditor/tiled/blob/master/COPYING)
- [文档 README](https://github.com/mapeditor/tiled/blob/master/docs/README.md)
- [TMX 格式参考及其许可声明](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/)

## 按工作任务选读

| 任务 | 官方页面 | 阅读用途 |
|---|---|---|
| 建立项目、地图与外置图块集 | [Introduction](https://doc.mapeditor.org/en/stable/manual/introduction/) | 从新建项目、创建地图到首次绘制图块，适合作为入门起点。 |
| 组织地图项目 | [Projects](https://doc.mapeditor.org/en/stable/manual/projects/) | 集中组织地图、图块、对象模板和团队项目配置。 |
| 选择地图与投影类型 | [Editing Maps](https://doc.mapeditor.org/en/stable/manual/maps/) | 比较正交、等距和其他地图方向，先固定项目使用的投影。 |
| 规划地图图层 | [Working with Layers](https://doc.mapeditor.org/en/stable/manual/layers/) | 区分图块、对象、图像和组图层的职责。 |
| 使用图块笔刷与选区 | [Editing Tile Layers](https://doc.mapeditor.org/en/stable/manual/editing-tile-layers/) | 学习批量绘制和修改地图布局。 |
| 使用对象层标注交互 | [Working with Objects](https://doc.mapeditor.org/en/stable/manual/objects/) | 用形状和图块对象表达出生点、触发区域及可交互物。 |
| 图块集、动画与碰撞 | [Editing Tilesets](https://doc.mapeditor.org/en/stable/manual/editing-tilesets/) | 在图块层面维护重用信息，阅读时重点查动画和碰撞编辑器。 |
| 让地图数据可被游戏读取 | [Custom Properties](https://doc.mapeditor.org/en/stable/manual/custom-properties/) | 为地图和对象附加自定义字段并统一数据约定。 |
| 对象模板复用 | [Using Templates](https://doc.mapeditor.org/en/stable/manual/using-templates/) | 把重复对象的共同属性整理成模板。 |
| 自动连接地形边界 | [Using Terrains](https://doc.mapeditor.org/en/stable/manual/terrain/) | 学习角、边及混合 terrain set 的标记和连接方式。 |
| 无限地图与分块 | [Using Infinite Maps](https://doc.mapeditor.org/en/stable/manual/using-infinite-maps/) | 理解不同于固定宽高地图的编辑方式。 |
| 把多张地图放入同一世界 | [Working with Worlds](https://doc.mapeditor.org/en/stable/manual/worlds/) | 在更大的空间中布置相邻地图。 |
| 自动映射规则 | [Automapping](https://doc.mapeditor.org/en/stable/manual/automapping/) | 用规则地图处理重复地形和局部模式。 |
| 地图导出与消费方兼容 | [Export Formats](https://doc.mapeditor.org/en/stable/manual/export/) | 核对目标引擎能读取的格式及导出选项。 |

## 版本与引擎边界

抓取时页面标题标为 Tiled 1.12.2。Tiled 负责地图编辑和数据输出；目标引擎是否识别某项自定义属性、对象模板、碰撞或地形数据，需要单独核对导入器。先做一张含图块、碰撞和交互对象的小测试地图，再扩展到完整场景。以上导读由整理者编写，未声称已在本机运行或验证引擎导入。
