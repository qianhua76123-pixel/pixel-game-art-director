#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
items=json.loads((R/'catalog.json').read_text());byid={e['id']:e for e in items}
def link(tid):
 e=byid[tid];return f'[{tid} · {e["title"]}]({e["path"]})'
def series(ids):return ' → '.join(link(x) for x in ids)
stats=json.loads((R/'manifests/collection-stats.json').read_text())
text=f'''# 像素游戏、制作与绘画教程库

收集日期：**2026-10-29**。共 **{len(items)} 篇独立来源教程**，均衡覆盖像素绘画、动作动画、素材制作和游戏开发，优先支持俯视角游戏。

- **先找教程：** [总目录](CATALOG.md)
- **交给其他 agent：** [阅读与检索说明](AGENT_README.md)
- **按目标学习：** [六条学习路线](LEARNING_PATHS.md)
- **直接导入检索系统：** [catalog.json](catalog.json)、[catalog.jsonl](catalog.jsonl)、[chunks.jsonl](chunks.jsonl)
- **核对交付：** [验证报告](qa/VALIDATION.md)、[来源与许可](LICENSES.md)

## 包含什么

| 分组 | 篇数 | 内容 |
|---|---:|---|
| 像素绘画与场景 | {stats['by_category'].get('drawing',0)} | 像素簇、轮廓、光影、俯视房屋、室内、树木草地、水、岩石、木材、金属等 |
| 角色与动作动画 | {stats['by_category'].get('animation',0)} | 侧视/俯视行走跑步、攻击、待机、跳跃、缓动、循环、亚像素、挤压与拖影 |
| 素材制作工作流 | {stats['by_category'].get('asset-production',0)} | Krita图层、选区、调色板、平铺纹理、动画时间轴、洋葱皮、导入导出等 |
| 游戏开发与引擎 | {stats['by_category'].get('game-development',0)} | Godot场景与输入、完整2D小游戏系列、俯视移动、碰撞、TileSet/TileMapLayer、灯光、清晰缩放等 |
| 游戏UI与界面设计 | {stats['by_category'].get('ui-design',0)} | 九宫格、主题资源、容器布局、HUD锚点与界面状态 |

当前清单登记 **{stats['unique_image_paths']} 个本地图像文件**，包含原始教学图/GIF以及辅助抽帧；抽帧不计为新教程。同一主题的原图与关键帧也不重复计入篇数。正文约 **{stats['markdown_bytes']/1024/1024:.2f} MiB Markdown**，不包含图片大小。

## 阅读示例

### 俯视房屋与场景

{link('ART-008')}、{link('ART-011')}、{link('ART-010')}。

![Saint11俯视房屋教程原图，CC BY 4.0](assets/drawing/ART-008/Top-Down-Houses-Compressed.gif)

图源：Pedro Medeiros（Saint11），[固定来源](https://github.com/saint11/Saint11Tutorials/blob/ce1393eb2c46441d917134a9fd52e15575ee10a7/Top-Down-Houses-Compressed.gif)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。中文步骤在对应MD中，原始GIF原样保存。

### 四方向角色与游戏接入

{series(['ANIM-003','ANIM-004','DEV-013','DEV-012'])}。

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
'''
(R/'README.md').write_text(text)
paths='# 六条学习路线\n\n以下顺序是整理者为使用本库而编排，不是原作者联合课程。每阶段都有可交付的小成果，优先完成场景规范与可复用素材，再扩展角色和引擎功能。\n\n'
routes=[
('1. 初学像素画：从可读轮廓到材质',['ART-001','ART-002','ART-005','ART-003','ART-004','ART-014','ART-015'],'产出：一组相同尺寸、相同光源、同一调色板的六个小道具。100%尺寸下可区分；必要孔洞与细杆没有被清理掉。'),
('2. 俯视乡村场景：房屋、草地、树与水',['ART-008','ART-011','ART-012','ART-013','ART-016','ART-007','ART-010','DEV-017','DEV-018'],'产出：一张小村庄测试地图，包含房屋、树、道路和水边。先固定视角与逻辑像素尺寸；检验平铺接缝、地面过渡、脚底遮挡与碰撞范围。'),
('3. 素材制作：可编辑源文件到引擎贴图',['MAKE-001','MAKE-002','MAKE-003','MAKE-006','MAKE-010','MAKE-011','MAKE-017','DEV-022','DEV-021'],'产出：源文件、透明PNG、命名表和尺寸/锚点说明。导出前后保持逻辑尺寸，实际引擎显示没有线性过滤模糊或边缘串色。'),
('4. 四方向角色：待机、行走、跑步与攻击',['ANIM-006','ANIM-003','ANIM-004','ANIM-005','ANIM-011','MAKE-013','MAKE-014','MAKE-015','DEV-013','DEV-023'],'产出：四向行走与待机精灵表，加一组攻击；记录每帧时长、脚底锚点和状态标签。左右不对称装备不能直接镜像后忽略修正。'),
('5. 第一个完整2D游戏：可玩循环',['DEV-001','DEV-003','DEV-004','DEV-005','DEV-006','DEV-007','DEV-008','DEV-009','DEV-010','DEV-011'],'产出：能够开始、移动、生成敌人、计分、结束并重新开始的小项目。这组原教程是通用2D入门，资产画风不是必须照抄的像素风规范。'),
('6. 俯视玩法接入与表现检查',['DEV-012','DEV-014','DEV-015','DEV-016','DEV-019','DEV-020','DEV-021','ANIM-008','ANIM-009'],'产出：可走动、被墙阻挡、拾取物品和进出区域的测试场景；在不同窗口尺寸验证像素清晰度，检查角色在建筑前后的位置排序。')]
for title,ids,goal in routes:
 paths+='## '+title+'\n\n'+series(ids)+'\n\n'+goal+'\n\n'
paths+='## 常见任务的直接入口\n\n| 任务 | 先读 |\n|---|---|\n'
for task,ids in [('角色看起来在滑行',['ANIM-001','ANIM-003','DEV-012']),('树冠只有散乱噪点',['ART-001','ART-011','ART-013']),('房屋和人物视角不一致',['ART-008','ART-010','ART-024']),('地图接缝或边缘串色',['ART-007','DEV-017','DEV-022']),('素材导出后变糊',['MAKE-002','DEV-021','DEV-022']),('攻击不够清楚或响应太慢',['ANIM-005','ANIM-008','ANIM-012']),('动画首尾一顿',['ANIM-009','MAKE-013'])]:paths+='| '+task+' | '+'；'.join(link(x) for x in ids)+' |\n'
(R/'LEARNING_PATHS.md').write_text(paths)
print('Wrote README.md and LEARNING_PATHS.md')
