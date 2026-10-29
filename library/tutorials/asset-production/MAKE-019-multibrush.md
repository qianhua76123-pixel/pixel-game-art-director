---
id: MAKE-019
title: 多重笔刷：径向结构与重复装饰
category: asset-production
path: tutorials/asset-production/MAKE-019-multibrush.md
source_url: https://docs.krita.org/en/reference_manual/tools/multibrush.html
source_title: Multibrush Tool
author:
- Wolthera van Hövell tot Westerflier
- Nmaghrufusman
license: GFDL-1.3-or-later
license_url: https://www.gnu.org/licenses/fdl-1.3.html
license_evidence_url: https://docs.krita.org/en/_sources/reference_manual/tools/multibrush.rst.txt
retrieved_at: '2026-10-29'
language: zh-CN+en
source_language: en
level: intermediate
tags:
- multibrush
- symmetry
- pattern
- 重复
- 对称
summary: 用同一笔画同步测试对称或平移结构，适合花朵、轮盘及重复装饰的草稿。
content_mode: licensed-fulltext-with-chinese-guide
version: Krita Manual 5.3.0 documentation (snapshot 2026-10-29)
prerequisites:
- 能够新建、保存和打开 Krita 文档
- 已有明确的目标像素尺寸或练习画布
source_rst_path: sources/asset-production/MAKE-019/original.rst
source_html_sha256: c6cf6a7b6b89868d7f5c4fb9f6b255dbd6404ea113da43dca93b14c95fd6835f
source_rst_sha256: 3b514eea8edbc17f4c776fc98aeb4fa2e4a1f02a2fde6485cf5276bb47ef0ed8
version_notes: Copy Translate at Interval 标注为 5.3 新增，最多 50 个画笔实例；旧版不应假定有同一模式。
---

# 多重笔刷：径向结构与重复装饰

> **内容边界**：下方“授权原文”是官方主内容的 Markdown 转换；中文操作路线、练习与验收由整理者编写，不是作者逐句翻译，也不代表已在本机运行软件验证。

## 中文任务导读

用同一笔画同步测试对称或平移结构，适合花朵、轮盘及重复装饰的草稿。

**前提**：能够新建、保存和打开 Krita 文档；先确定目标像素尺寸、色板与透明度要求。

### 操作路线

1. 选择 Multibrush，在 Tool Options 选择 Symmetry、Mirror 或 Translate 等模式。
2. 设置中心、实例数或半径，小范围试画确认分布。
3. 使用 Copy Translate 时先开启 Add 标定副本位置，再关闭 Add 进行绘制。
4. 结构确定后关闭多重绘制，单独处理光照、轮廓和非对称变化。

### 配图怎么读

![多重笔刷：径向结构与重复装饰：官方示意图](../../assets/asset-production/MAKE-019/Krita-multibrush.png)

放射状笔触围绕中心重复，展示实例数量和角度的影响；像素资产还需单独处理中心重叠和不对称照明。 图内界面与作品保留原貌；示例转用于像素素材时仍按本篇验收条件检查。

### 练习与验收（整理者补充）

建立四瓣花的对称结构，再手工把其中两瓣改成不同形状，保持整体方向一致。

- [ ] 实例位置可复现。
- [ ] 中心没有叠加出多余暗点。
- [ ] 最终形体经过单独的像素轮廓检查。

### 版本与适用边界

Copy Translate at Interval 标注为 5.3 新增，最多 50 个画笔实例；旧版不应假定有同一模式。

抓取时页面标题标注 **Krita Manual 5.3.0**；这是文档快照版本，不构成已发布软件版本或本机功能的验证。原文中保留的 `Added/Changed/Deprecated in version` 是兼容性依据。

## 来源、许可与修改记录

- 原文：[Multibrush Tool](https://docs.krita.org/en/reference_manual/tools/multibrush.html)
- 作者：Wolthera van Hövell tot Westerflier；Nmaghrufusman
- 页内作者与许可原始声明：[RST 源文件](../../sources/asset-production/MAKE-019/original.rst)；[线上原始声明](https://docs.krita.org/en/_sources/reference_manual/tools/multibrush.rst.txt)。
- 许可：[GNU Free Documentation License 1.3 or later](https://www.gnu.org/licenses/fdl-1.3.html)；[本地许可证全文](../../licenses/krita-GFDL-1.3.txt)。各图若有独立作者或许可，沿用原文紧邻图像的署名，不把作品许可自动泛化为文档许可。
- 修改历史：2026-10-29，Codex 为本教程库新增中文导读、练习和验收；将官方 HTML 主内容转换为 Markdown，去除导航与页脚，将控制图标转为文字、将教学图像存为本地文件。正文、步骤、代码、表格与图像说明保留。
- 本修改版沿用 GFDL 1.3 或更新版本。保留作者声明和上游链接；未添加 Invariant Sections、Front-Cover Texts 或 Back-Cover Texts。外链视频、安装包和关联页面没有自动下载或转录。

## 授权原文（英语，完整主内容转换）

<a id="multibrush-tool"></a>

<a id="index-0"></a>
<a id="id1"></a>

## Multibrush Tool

[toolmultibrush]

The Multibrush tool allows you to draw using multiple instances of a freehand brush stroke at once, it can be accessed from the Toolbox docker or with the default shortcut `Q`. Using the Multibrush is similar to toggling the [Mirror Tools](https://docs.krita.org/en/user_manual/mirror_tools.html#mirror-tools), but the Multibrush is more sophisticated, for example it can mirror freehand brush strokes along a rotated axis.

The settings for the tool will be found in the tool options dock.

The multibrush tool has a few modes and the settings for each can be found in the tool options dock. Symmetry and mirror reflect over an axis which can be set in the tool options dock. The default axis is the center of the canvas.

![Figure 1: Krita multibrush](../../assets/asset-production/MAKE-019/Krita-multibrush.png)

The available modes are:

Symmetry
:   Symmetry will reflect your brush around the axis at even intervals. The slider determines the number of instances which will be drawn on the canvas.

Mirror
:   Mirror will reflect the brush across the X axis, the Y axis, or both.

Translate
:   Translate will paint the set number of instances around the cursor at the radius distance.

Snowflake
:   This works as a mirrored symmetry, but is a bit slower than symmetry+toolbar mirror mode.

Copy Translate
:   This allows you to set the position of the copies relative to your own cursor. To set the position of the copies, first toggle Add, and then [left mouse button] the canvas to place copies relative to the multibrush origin. Finally, press Add again, and start drawing to see the copy translate in action.

Copy Translate at Interval
:   This allows for brushes to be applied at an orthogonal interval. The max amount of brushes allowed is 50, so you will need to set the interval high enough to allow for less than 50 brushes to appear over the whole document.

    Interval X
    :   The interval in the horizontal direction.

    Interval Y
    :   The interval in the vertical direction.

    Added in version 5.3.

The assistant and smoothing options work the same as in the [Freehand Brush Tool](https://docs.krita.org/en/reference_manual/tools/freehand_brush.html#freehand-brush-tool), though only on the real brush and not its copies.

## 本地配图清单

| 图 | 本地文件 | 原始来源 |
|---|---|---|
| 1 | [Figure 1: Krita multibrush](../../assets/asset-production/MAKE-019/Krita-multibrush.png) | [原图](https://docs.krita.org/en/_images/Krita-multibrush.png) |
