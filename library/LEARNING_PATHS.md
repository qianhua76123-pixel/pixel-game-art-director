# 六条学习路线

以下顺序是整理者为使用本库而编排，不是原作者联合课程。每阶段都有可交付的小成果，优先完成场景规范与可复用素材，再扩展角色和引擎功能。

## 1. 初学像素画：从可读轮廓到材质

[ART-001 · 像素簇、孤立像素与画面噪点](tutorials/drawing/ART-001-pixel-clusters.md) → [ART-002 · 直线步长、曲线与意外方块](tutorials/drawing/ART-002-lines-curves-corners.md) → [ART-005 · 用剪影建立角色与道具识别性](tutorials/drawing/ART-005-silhouette-design.md) → [ART-003 · 光影体积、色相偏移与受光面](tutorials/drawing/ART-003-shading-hue-shift.md) → [ART-004 · 外轮廓、选择性描边与形状分离](tutorials/drawing/ART-004-outlines.md) → [ART-014 · 木材：树桩、木板、年轮和木纹](tutorials/drawing/ART-014-wood-material.md) → [ART-015 · 岩石：大面、层理与不同地质形状](tutorials/drawing/ART-015-rock-formations.md)

产出：一组相同尺寸、相同光源、同一调色板的六个小道具。100%尺寸下可区分；必要孔洞与细杆没有被清理掉。

## 2. 俯视乡村场景：房屋、草地、树与水

[ART-008 · 俯视斜视角房屋：从体块到屋顶材质](tutorials/drawing/ART-008-top-down-houses.md) → [ART-011 · 树冠：剪影、体积与有节制的叶片纹理](tutorials/drawing/ART-011-vegetation-volume.md) → [ART-012 · 草地与土层：地面纹理的分层和疏密](tutorials/drawing/ART-012-vegetation-ground-layers.md) → [ART-013 · 植物多样性：叶形、茎干与远近层次](tutorials/drawing/ART-013-vegetation-variety.md) → [ART-016 · 水面、波纹、瀑布和水下位移](tutorials/drawing/ART-016-water-surfaces.md) → [ART-007 · 无缝主图块、边缘块与变体](tutorials/drawing/ART-007-seamless-tiles.md) → [ART-010 · 俯视场景的脚底排序、复杂遮挡与碰撞投影](tutorials/drawing/ART-010-top-down-depth-sorting.md) → [DEV-017 · TileSet：图集切分、碰撞、遮挡与地形规则](tutorials/game-development/DEV-017-tileset-authoring.md) → [DEV-018 · TileMapLayer：分层绘图、图案与自动地形](tutorials/game-development/DEV-018-tilemap-layer-painting.md)

产出：一张小村庄测试地图，包含房屋、树、道路和水边。先固定视角与逻辑像素尺寸；检验平铺接缝、地面过渡、脚底遮挡与碰撞范围。

## 3. 素材制作：可编辑源文件到引擎贴图

[MAKE-001 · 像素素材、平铺纹理与索引色工作流](tutorials/asset-production/MAKE-001-common-workflows.md) → [MAKE-002 · 画布尺寸、像素尺寸、裁切与素材导出](tutorials/asset-production/MAKE-002-image-size-export.md) → [MAKE-003 · 分层、图层组与遮罩：保持素材可修改](tutorials/asset-production/MAKE-003-layers-masks.md) → [MAKE-006 · 选区、透明度选区与局部修整](tutorials/asset-production/MAKE-006-selections.md) → [MAKE-010 · 调色板：分组色阶、命名与素材统一](tutorials/asset-production/MAKE-010-palette-docker.md) → [MAKE-011 · 网格与辅助线：图块尺寸、偏移与对齐](tutorials/asset-production/MAKE-011-grids-guides.md) → [MAKE-017 · 变换工具：缩放、翻转与形变的适用边界](tutorials/asset-production/MAKE-017-transform-tool.md) → [DEV-022 · 像素图片导入：压缩、纹理与透明边缘](tutorials/game-development/DEV-022-image-import-pipeline.md) → [DEV-021 · 像素清晰度：基础分辨率、缩放与宽高比](tutorials/game-development/DEV-021-pixel-perfect-resolutions.md)

产出：源文件、透明PNG、命名表和尺寸/锚点说明。导出前后保持逻辑尺寸，实际引擎显示没有线性过滤模糊或边缘串色。

## 4. 四方向角色：待机、行走、跑步与攻击

[ANIM-006 · 待机动画：两帧、三帧、六帧与次级运动](tutorials/animation/ANIM-006-character-idle.md) → [ANIM-003 · 俯视行走：六帧周期与四方向遮挡](tutorials/animation/ANIM-003-top-down-walk.md) → [ANIM-004 · 俯视跑步：层叠体块、腾空与恢复](tutorials/animation/ANIM-004-top-down-run.md) → [ANIM-005 · 俯视攻击：预备、斩击与回收](tutorials/animation/ANIM-005-top-down-attack.md) → [ANIM-011 · 亚像素运动错觉：轮廓、内部与色阶](tutorials/animation/ANIM-011-subpixel-illusion.md) → [MAKE-013 · 动画时间轴：关键帧、保持帧与播放范围](tutorials/asset-production/MAKE-013-animation-timeline.md) → [MAKE-014 · 洋葱皮：比较前后姿势与消除帧间漂移](tutorials/asset-production/MAKE-014-onion-skin.md) → [MAKE-015 · 导出动画：PNG 序列、像素放大与编码](tutorials/asset-production/MAKE-015-render-animation.md) → [DEV-013 · 把角色帧图和精灵表接成二维动画](tutorials/game-development/DEV-013-sprite-animation.md) → [DEV-023 · AnimationTree：动作混合与状态机](tutorials/game-development/DEV-023-animation-tree-state-machine.md)

产出：四向行走与待机精灵表，加一组攻击；记录每帧时长、脚底锚点和状态标签。左右不对称装备不能直接镜像后忽略修正。

## 5. 第一个完整2D游戏：可玩循环

[DEV-001 · 用节点与场景组织像素游戏](tutorials/game-development/DEV-001-nodes-and-scenes.md) → [DEV-003 · 读取玩家输入并驱动角色](tutorials/game-development/DEV-003-player-input.md) → [DEV-004 · 用信号连接按钮、计时器与游戏事件](tutorials/game-development/DEV-004-signals.md) → [DEV-005 · 完整二维小游戏：项目与素材准备](tutorials/game-development/DEV-005-first-game-project-setup.md) → [DEV-006 · 完整二维小游戏：玩家场景与动画资源](tutorials/game-development/DEV-006-first-game-player-scene.md) → [DEV-007 · 完整二维小游戏：移动、动画切换与受击](tutorials/game-development/DEV-007-first-game-player-code.md) → [DEV-008 · 完整二维小游戏：敌人场景与离屏清理](tutorials/game-development/DEV-008-first-game-enemies.md) → [DEV-009 · 完整二维小游戏：生成、计分与回合循环](tutorials/game-development/DEV-009-first-game-main-loop.md) → [DEV-010 · 完整二维小游戏：HUD、开始按钮与重开](tutorials/game-development/DEV-010-first-game-hud.md) → [DEV-011 · 完整二维小游戏：声音、背景与交付检查](tutorials/game-development/DEV-011-first-game-finishing.md)

产出：能够开始、移动、生成敌人、计分、结束并重新开始的小项目。这组原教程是通用2D入门，资产画风不是必须照抄的像素风规范。

## 6. 俯视玩法接入与表现检查

[DEV-012 · 俯视角色的八向移动、朝向与点击移动](tutorials/game-development/DEV-012-top-down-movement.md) → [DEV-014 · 角色碰撞：移动、沿墙滑动与反弹](tutorials/game-development/DEV-014-character-body-collisions.md) → [DEV-015 · Area2D：拾取物、门口、伤害区与区域影响](tutorials/game-development/DEV-015-area2d-triggers.md) → [DEV-016 · 二维物理基础：形状、图层、遮罩和物体类型](tutorials/game-development/DEV-016-physics-layers-and-shapes.md) → [DEV-019 · 俯视场景的二维灯光、遮挡与材质响应](tutorials/game-development/DEV-019-lights-and-shadows.md) → [DEV-020 · CanvasLayer：分离游戏世界、背景与HUD](tutorials/game-development/DEV-020-canvas-layers.md) → [DEV-021 · 像素清晰度：基础分辨率、缩放与宽高比](tutorials/game-development/DEV-021-pixel-perfect-resolutions.md) → [ANIM-008 · 动画缓动：用间距表达加速、减速与过冲](tutorials/animation/ANIM-008-easing-timing.md) → [ANIM-009 · 无缝循环：错开周期与粒子出生时刻](tutorials/animation/ANIM-009-seamless-loop.md)

产出：可走动、被墙阻挡、拾取物品和进出区域的测试场景；在不同窗口尺寸验证像素清晰度，检查角色在建筑前后的位置排序。

## 常见任务的直接入口

| 任务 | 先读 |
|---|---|
| 角色看起来在滑行 | [ANIM-001 · 侧视行走：接触、下压、经过与抬升](tutorials/animation/ANIM-001-walk-cycle.md)；[ANIM-003 · 俯视行走：六帧周期与四方向遮挡](tutorials/animation/ANIM-003-top-down-walk.md)；[DEV-012 · 俯视角色的八向移动、朝向与点击移动](tutorials/game-development/DEV-012-top-down-movement.md) |
| 树冠只有散乱噪点 | [ART-001 · 像素簇、孤立像素与画面噪点](tutorials/drawing/ART-001-pixel-clusters.md)；[ART-011 · 树冠：剪影、体积与有节制的叶片纹理](tutorials/drawing/ART-011-vegetation-volume.md)；[ART-013 · 植物多样性：叶形、茎干与远近层次](tutorials/drawing/ART-013-vegetation-variety.md) |
| 房屋和人物视角不一致 | [ART-008 · 俯视斜视角房屋：从体块到屋顶材质](tutorials/drawing/ART-008-top-down-houses.md)；[ART-010 · 俯视场景的脚底排序、复杂遮挡与碰撞投影](tutorials/drawing/ART-010-top-down-depth-sorting.md)；[ART-024 · 2:1像素等距风格网格与立体造型](tutorials/drawing/ART-024-isometric-grid.md) |
| 地图接缝或边缘串色 | [ART-007 · 无缝主图块、边缘块与变体](tutorials/drawing/ART-007-seamless-tiles.md)；[DEV-017 · TileSet：图集切分、碰撞、遮挡与地形规则](tutorials/game-development/DEV-017-tileset-authoring.md)；[DEV-022 · 像素图片导入：压缩、纹理与透明边缘](tutorials/game-development/DEV-022-image-import-pipeline.md) |
| 素材导出后变糊 | [MAKE-002 · 画布尺寸、像素尺寸、裁切与素材导出](tutorials/asset-production/MAKE-002-image-size-export.md)；[DEV-021 · 像素清晰度：基础分辨率、缩放与宽高比](tutorials/game-development/DEV-021-pixel-perfect-resolutions.md)；[DEV-022 · 像素图片导入：压缩、纹理与透明边缘](tutorials/game-development/DEV-022-image-import-pipeline.md) |
| 攻击不够清楚或响应太慢 | [ANIM-005 · 俯视攻击：预备、斩击与回收](tutorials/animation/ANIM-005-top-down-attack.md)；[ANIM-008 · 动画缓动：用间距表达加速、减速与过冲](tutorials/animation/ANIM-008-easing-timing.md)；[ANIM-012 · 运动拖影：用少量帧连接快速动作](tutorials/animation/ANIM-012-motion-smear.md) |
| 动画首尾一顿 | [ANIM-009 · 无缝循环：错开周期与粒子出生时刻](tutorials/animation/ANIM-009-seamless-loop.md)；[MAKE-013 · 动画时间轴：关键帧、保持帧与播放范围](tutorials/asset-production/MAKE-013-animation-timeline.md) |
