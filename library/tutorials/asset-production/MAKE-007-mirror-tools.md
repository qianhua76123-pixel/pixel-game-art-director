---
id: MAKE-007
title: 镜像工具：对称道具与建筑结构
category: asset-production
path: tutorials/asset-production/MAKE-007-mirror-tools.md
source_url: https://docs.krita.org/en/user_manual/mirror_tools.html
source_title: Mirror Tools
author:
- Scott Petrovic
- Nmagfurusman
license: GFDL-1.3-or-later
license_url: https://www.gnu.org/licenses/fdl-1.3.html
license_evidence_url: https://docs.krita.org/en/_sources/user_manual/mirror_tools.rst.txt
retrieved_at: '2026-10-29'
language: zh-CN+en
source_language: en
level: beginner
tags:
- symmetry
- mirror
- architecture
- 镜像
- 建筑
summary: 快速建立双侧对称的主体，并保留之后手工调整光照和材质的空间。
content_mode: licensed-fulltext-with-chinese-guide
version: Krita Manual 5.3.0 documentation (snapshot 2026-10-29)
prerequisites:
- 能够新建、保存和打开 Krita 文档
- 已有明确的目标像素尺寸或练习画布
source_rst_path: sources/asset-production/MAKE-007/original.rst
source_html_sha256: f46e506770cc08864df20d63faae10eae2f4e4c5a1c4ba0e76816115b004f71b
source_rst_sha256: 418ff67b3787f402395c18e9c050b0adf74b8cf197632efdbace1d4781e29660
version_notes: 此工具只提供水平、垂直轴；旋转角度的镜像需要 Multibrush。
---

# 镜像工具：对称道具与建筑结构

> **内容边界**：下方“授权原文”是官方主内容的 Markdown 转换；中文操作路线、练习与验收由整理者编写，不是作者逐句翻译，也不代表已在本机运行软件验证。

## 中文任务导读

快速建立双侧对称的主体，并保留之后手工调整光照和材质的空间。

**前提**：能够新建、保存和打开 Krita 文档；先确定目标像素尺寸、色板与透明度要求。

### 操作路线

1. 开启水平或垂直镜像，把镜像轴移到主体需要的中心线。
2. 在一侧绘制门、瓶或正面建筑，检查另一侧的同步结果。
3. 需要固定中心时锁定镜像轴，避免继续绘画时移动手柄。
4. 基础形体完成后关闭镜像，分别处理投影、磨损和光源造成的不对称细节。

### 配图怎么读

![镜像工具：对称道具与建筑结构：官方示意图](../../assets/asset-production/MAKE-007/Mirror-tool.png)

剑的上下两侧围绕同一轴同步绘制；先检查轴的位置，再决定哪些非对称细节应在关闭镜像后处理。 图内界面与作品保留原貌；示例转用于像素素材时仍按本篇验收条件检查。

### 练习与验收（整理者补充）

制作一扇正面木门：先镜像构建门框，再独立添加一侧门把手和光源方向一致的阴影。

- [ ] 镜像中心与像素网格匹配。
- [ ] 有效宽度没有多出中心列。
- [ ] 照明没有被机械镜像成双光源。

### 版本与适用边界

此工具只提供水平、垂直轴；旋转角度的镜像需要 Multibrush。

抓取时页面标题标注 **Krita Manual 5.3.0**；这是文档快照版本，不构成已发布软件版本或本机功能的验证。原文中保留的 `Added/Changed/Deprecated in version` 是兼容性依据。

## 来源、许可与修改记录

- 原文：[Mirror Tools](https://docs.krita.org/en/user_manual/mirror_tools.html)
- 作者：Scott Petrovic；Nmagfurusman
- 页内作者与许可原始声明：[RST 源文件](../../sources/asset-production/MAKE-007/original.rst)；[线上原始声明](https://docs.krita.org/en/_sources/user_manual/mirror_tools.rst.txt)。
- 许可：[GNU Free Documentation License 1.3 or later](https://www.gnu.org/licenses/fdl-1.3.html)；[本地许可证全文](../../licenses/krita-GFDL-1.3.txt)。各图若有独立作者或许可，沿用原文紧邻图像的署名，不把作品许可自动泛化为文档许可。
- 修改历史：2026-10-29，Codex 为本教程库新增中文导读、练习和验收；将官方 HTML 主内容转换为 Markdown，去除导航与页脚，将控制图标转为文字、将教学图像存为本地文件。正文、步骤、代码、表格与图像说明保留。
- 本修改版沿用 GFDL 1.3 或更新版本。保留作者声明和上游链接；未添加 Invariant Sections、Front-Cover Texts 或 Back-Cover Texts。外链视频、安装包和关联页面没有自动下载或转录。

## 授权原文（英语，完整主内容转换）

<a id="mirror-tools"></a>

<a id="index-0"></a>
<a id="id1"></a>

## Mirror Tools

Draw on one side of a mirror line while the Mirror Tool copies the results to the other side. The Mirror Tools are accessed along the toolbar. You can move the location of the mirror line by grabbing the handle.

![Figure 1: Mirror tool](../../assets/asset-production/MAKE-007/Mirror-tool.png)

Mirror Tools give a similar result to the [Multibrush Tool](https://docs.krita.org/en/reference_manual/tools/multibrush.html#multibrush-tool), but unlike the Multibrush which only traces brush strokes like the [Freehand Brush Tool](https://docs.krita.org/en/reference_manual/tools/freehand_brush.html#freehand-brush-tool), the Mirror Tools can be used with any other tool that traces strokes, such as the [Straight Line Tool](https://docs.krita.org/en/reference_manual/tools/line.html#line-tool) and the [Bezier Curve Tool](https://docs.krita.org/en/reference_manual/tools/path.html#path-tool), and even with the Multibrush Tool.

Horizontal Mirror Tool
:   Mirror the results along the horizontal axis.

Vertical Mirror Tool
:   Mirror the results along the vertical axis.

There are additional options for each tool. You can access these by the clicking the drop-down arrow located on the right of each tool.

- Hide Mirror X/Y Line (toggle) – Locks the mirror axis and hides the axis line.
- Lock X/Y Line (toggle) – hides the move icon on the axis line.
- Move to Canvas Center X/Y – Moves the axis line to the center of the canvas.

<a id="mirroring-along-a-rotated-line"></a>

### Mirroring along a rotated line

The Mirror Tool can only mirror along a perfectly vertical or horizontal line. To mirror along a line that is at a rotated angle, use the [Multibrush Tool](https://docs.krita.org/en/reference_manual/tools/multibrush.html#multibrush-tool) and its various parameters, it has more advanced options besides basic symmetry.

## 本地配图清单

| 图 | 本地文件 | 原始来源 |
|---|---|---|
| 1 | [Figure 1: Mirror tool](../../assets/asset-production/MAKE-007/Mirror-tool.png) | [原图](https://docs.krita.org/en/_images/Mirror-tool.png) |
