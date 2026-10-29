#!/usr/bin/env python3
"""Collect 24 licensed Krita manual pages and their figures, with Chinese task guides.
Run with Python plus requests, beautifulsoup4, markdownify, pillow and pyyaml.
All requests are read-only; bounded at four pages concurrently. No paid services.
"""
import concurrent.futures, hashlib, io, json, os, re, sys, threading, time
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import requests, yaml
from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-29'
BASE='https://docs.krita.org/en/'
LICENSE_URL='https://www.gnu.org/licenses/fdl-1.3.html'
LICENSE_SOURCE='https://invent.kde.org/documentation/docs-krita-org/-/raw/master/LICENSE'
CONVENTIONS='https://docs.krita.org/en/contributors_manual/krita_manual_conventions.html'
VERSION='Krita Manual 5.3.0 documentation (snapshot 2026-10-29)'
# Briefs are original editorial guidance; the complete source body follows separately.
D=[
('common-workflows','tutorials/common_workflows','像素素材、平铺纹理与索引色工作流','beginner',['pixel-art','tiles','texture','index-color','素材','平铺'],
 '在同一制作流程里区分构图草稿、平涂、无缝纹理和索引色效果。重点阅读原文 Preparing Tiles and Textures 与 Creating Pixel Art。',
 ['建立独立原稿与导出副本，先决定目标画布尺寸、色板和光源。','制作地表纹理时开启 View → Wrap Around Mode；在边缘落笔并观察相邻副本的接缝。','需要灰度映射工作流时，在绘画层上方添加 Index Color 滤镜层，指定各明度对应的颜色。','按原文图层示意将抖色图案放在绘画层上方、索引色层下方；最后在原始尺寸检查轮廓与碎点。'],
 '用 32×32 画布做一块草地，连续平铺 3×3 观察边界；再制作一个保持相同色板的泥地变体。',
 ['四边连续平铺无突然断纹。','缩回 100% 时主要形状仍可读。','交付尺寸、色板与透明边界有记录。'],
 '原文的高分辨率像素效果方法不等于逐像素精修；自动索引和抖色后仍需检查边缘、细杆和孔洞。'),
('image-size-export','user_manual/working_with_images','画布尺寸、像素尺寸、裁切与素材导出','beginner',['canvas','size','export','png','尺寸','导出'],
 '避免混淆扩大画布与重采样图像，建立可回到原稿的素材文件流程。',
 ['先在图像属性中记录实际宽高像素；PPI 主要关系到印刷尺寸，不是游戏精灵的网格尺寸。','使用 Resize Canvas 增加留白，并用偏移控制已有内容的位置。','只有确需改变内容大小时才用 Scale Image to New Size；像素素材应检查所选插值算法。','保留含图层的 .kra 主文件，再另行导出透明 PNG，重新打开导出文件检查。'],
 '把 32×32 的道具放入 48×48 画布，保持底部接地点一致；输出原尺寸 PNG 与原稿。',
 ['扩画布后道具本身的像素不变。','透明边缘没有被背景色填实。','导出 PNG 与原稿能对应同一版本。'],
 '一般绘画的分辨率建议不直接适用于游戏素材；以最终像素尺寸与引擎显示倍率为准。'),
('layers-masks','user_manual/layers_and_masks','分层、图层组与遮罩：保持素材可修改','beginner',['layers','masks','alpha','分层','透明度'],
 '为树、建筑和家具拆出轮廓、底色、阴影与细节，同时理解组内合成。',
 ['把底色、描边、阴影和高光放在独立图层，按物体建立图层组。','观察原文 Layer-composite 图，确认上层、下层及组的合成顺序。','需要限定阴影区域时使用组内 Alpha Inheritance，并检查组的 Pass Through 设置。','对可回退的修正优先使用遮罩或滤镜层；导出前检查隐藏层与合成结果。'],
 '为一间房子建立屋顶、墙体、门窗三组，每组至少有底色和阴影；只改屋顶配色而不影响其他组。',
 ['各部件可独立修改。','透明洞口仍保持透明。','组的显示结果与导出一致。'],
 '图层类型和遮罩是编辑结构，不自动对应引擎中的可交互物件；导出前仍需确定精灵拆分方式。'),
('alpha-inheritance','tutorials/clipping_masks_and_alpha_inheritance','用 Alpha Inheritance 给素材分层上色','beginner',['clipping','alpha','shading','遮罩','阴影'],
 '在既有物体轮廓内添加多层阴影与高光，减少改色时损伤边缘。',
 ['把需要作为剪裁范围的底色层放进同一个普通图层组。','在底色层上方新建阴影或高光层，先画一笔明显越界的颜色用于观察。','打开该层 Alpha Inheritance；对照原文前后图确认颜色仅出现在组内下方合成的不透明区域。','需要快速建立结构时使用 Ctrl+Shift+G 创建快速剪裁组，并确认没有启用组的 Pass Through。'],
 '给一棵树的树冠增加两层受同一轮廓限制的阴影与高光，随后改变底色测试可维护性。',
 ['越界笔触不会污染透明背景。','树冠和树干的范围没有意外合并。','改变底色后阴影结构仍可编辑。'],
 'Krita 的组内透明度继承与其他软件的单层剪贴遮罩规则不同，不要直接套用别的软件图层操作。'),
('flat-coloring','tutorials/flat-coloring','平涂上色：填充、选区与色块拆分','beginner',['flat-color','lineart','fill','平涂','色块'],
 '把线稿转换成干净、可编辑的分色素材，比较不同填色方法的边界表现。',
 ['先判断线稿是否在独立透明图层，白底线稿需选定处理方式再上色。','新建底色层，在封闭区域使用填充，或用选区明确要填的范围。','参考原文多种方法的优缺点，比较 Multiply、选区、Color to Alpha 与 Colorize Mask。','在透明或对比色背景上检查线条与底色之间的空隙，再按部件保留色块图层。'],
 '画一个带把手的水壶，分别用填充和选区上色，比较把手孔洞与细线的保留情况。',
 ['把手内孔没有被误填。','底色没有穿过细轮廓。','改一个部件颜色不会污染相邻部件。'],
 '原文含普通插画的抗锯齿处理；严格像素资产应根据目标规范关闭羽化并重新检查边界颜色。'),
('selections','user_manual/selections','选区、透明度选区与局部修整','beginner',['selection','mask','cleanup','选区','修整'],
 '把修改限定到精确范围，防止重着色或清理时破坏相邻像素。',
 ['根据目标形状选矩形、多边形、自由或颜色相关选区工具。','在工具选项中确认当前是替换、增加、减去还是相交模式。','需要按素材已有轮廓选择时，从图层透明度建立选区；复杂边缘可查看全局选区遮罩。','完成局部操作后取消选区，并在 100% 与放大视图分别检查成品。'],
 '只修改竹椅坐面颜色，同时保留椅腿和中间镂空；保存修改前后的同坐标截图。',
 ['选区没有遗漏孤立但有效的像素。','羽化设置符合像素素材要求。','取消选区后无被遮住的边缘错误。'],
 '像素选区与向量选区的编辑方式不同；从高分辨率插画迁移时不要默认沿用平滑边缘设置。'),
('mirror-tools','user_manual/mirror_tools','镜像工具：对称道具与建筑结构','beginner',['symmetry','mirror','architecture','镜像','建筑'],
 '快速建立双侧对称的主体，并保留之后手工调整光照和材质的空间。',
 ['开启水平或垂直镜像，把镜像轴移到主体需要的中心线。','在一侧绘制门、瓶或正面建筑，检查另一侧的同步结果。','需要固定中心时锁定镜像轴，避免继续绘画时移动手柄。','基础形体完成后关闭镜像，分别处理投影、磨损和光源造成的不对称细节。'],
 '制作一扇正面木门：先镜像构建门框，再独立添加一侧门把手和光源方向一致的阴影。',
 ['镜像中心与像素网格匹配。','有效宽度没有多出中心列。','照明没有被机械镜像成双光源。'],
 '此工具只提供水平、垂直轴；旋转角度的镜像需要 Multibrush。'),
('brush-presets','user_manual/loading_saving_brushes','保存与共享一致的像素绘画笔刷预设','intermediate',['brush','preset','resources','笔刷','一致性'],
 '把尺寸、笔尖与输入响应保存为可复用预设，降低不同素材间的工具差异。',
 ['复制一个接近目标的预设，在 F5 设置面板逐项检查笔尖、尺寸与间距。','对像素精修单独建立固定尺寸、固定不透明度的预设；用测试笔画确认压力是否改变结果。','通过 Save New Brush Preset 保存名称和图标，保留原预设用于回退。','共享时检查预设是否依赖额外笔尖和图案；优先用资源包一起导出。'],
 '保存“1px 修边”和“色块铺底”两个预设；重启后用相同输入比较笔画是否一致。',
 ['预设重载后尺寸和边缘行为一致。','使用者能找到依赖的笔尖与图案。','软边绘画预设不会混入严格像素修边流程。'],
 '原文示例为勾线笔刷并建议抗锯齿；像素修边预设需要另行关闭平滑相关参数，不能照搬示例数值。'),
('pixel-brush-engine','reference_manual/brushes/brush_engines/pixel_brush_engine','理解 Pixel Brush 引擎：笔尖、间距与颜色变化','intermediate',['brush-engine','spacing','opacity','笔尖','间距'],
 '了解一次笔画由连续笔尖印记组成，找出边缘软化和意外颜色变化来自哪里。',
 ['选择笔尖类型并用短笔画观察单个印记形状。','改变间距，比较连续线与可见印记之间的差异。','逐项检查尺寸、透明度和 HSV 参数是否由压力、速度或随机传感器控制。','保存一个固定参数版本，和原笔刷并排测试颜色数及边缘清晰度。'],
 '在 32×32 画布上用同一颜色画三条线，只改变间距或压力响应，记录结果。',
 ['能够说明每种笔画变化对应哪个参数。','目标固定色笔刷没有随机 HSV 变化。','边缘是否有半透明像素已检查。'],
 'Pixel Brush 是 Krita 的通用栅格笔刷引擎名称，不代表默认配置天然适合逐像素绘画。'),
('palette-docker','reference_manual/dockers/palette_docker','调色板：分组色阶、命名与素材统一','beginner',['palette','swatches','color-ramp','调色板','色阶'],
 '把一个场景的地面、木材、植被和高光色整理成可共享的色板。',
 ['在 Palette Docker 创建新色板并命名，或导入已有资源。','为木材、植物、石材等用途建立分组，将亮暗色阶相邻排列。','给关键色块添加名称或 ID，使用色板取色，避免靠视觉重新选近似色。','保存色板到资源或文档，重新打开检查分组与色值。'],
 '建立 12 色乡村素材色板，至少含木材与植被两条色阶；用同一色板给木桶和树冠配色。',
 ['同用途颜色有稳定名称。','重新打开文档后色板仍可用。','未因随意拾色增加大量近似色。'],
 '调色板在 4.2 有过重做；本页按 5.3 手册阅读，旧版的保存与排列入口可能不同。'),
('grids-guides','reference_manual/dockers/grids_and_guides','网格与辅助线：图块尺寸、偏移与对齐','beginner',['grid','guides','tile','网格','图块'],
 '为图块、精灵表和建筑部件设置统一的坐标基准。',
 ['使用矩形网格，将 X/Y 间距设置为素材约定的图块尺寸。','检查 Grid Offset；有边距或间隔的图集需把它们纳入布局记录。','开启或关闭吸附，分别测试绘制与移动是否符合预期。','为角色脚底、房屋接地点或图集边界添加辅助线并保存文档模板。'],
 '建立 16×16 图块网格，在一张 64×64 图集中排列四类地表，并标记外边界。',
 ['图块边界与源像素坐标对齐。','辅助线不会出现在导出 PNG 中。','变更偏移后没有误以为素材自身移动。'],
 '本页区分旧版与新版等距网格；等距网格不支持吸附，不能把矩形网格的行为直接套用。'),
('walk-cycle','user_manual/animation','从关键姿势到循环：Krita 行走动画实作','beginner',['animation','walk-cycle','frames','行走','动画'],
 '通过官方行走示例理解关键帧、保持帧、洋葱皮和循环节奏，再迁移到像素角色。',
 ['进入动画工作区，先设置画布、时间范围和帧率；把背景与动画图层分开。','在动画图层创建关键帧，建立身体与四肢的主要姿势。','开启洋葱皮，用相邻帧对齐头部与脚底，继续补中间姿势。','循环播放并调整帧间距，最后导出图像序列供引擎使用。'],
 '制作一个 4～6 个绘制帧的行走循环；固定脚底基线，并分别观察轮廓和最终配色版本。',
 ['首尾衔接不突然跳位。','背景层不会随角色帧一起变化。','脚底锚点和帧尺寸一致。'],
 '官方案例为侧面普通绘画，不是俯视像素成品；姿势与时间轴方法可迁移，视角与像素轮廓需另作设计。'),
('animation-timeline','reference_manual/dockers/animation_timeline','动画时间轴：关键帧、保持帧与播放范围','intermediate',['timeline','keyframes','timing','时间轴','节奏'],
 '让动画速度由时间安排控制，而不是随意复制帧；理解时间轴上的不同帧状态。',
 ['把需要编辑的图层固定显示到 Animation Timeline，确认当前帧与当前图层。','先区分创建空白关键帧、复制关键帧和已有内容持续显示的保持区间。','移动或插入关键帧调整动作节奏，必要时用帧颜色帮助区分动作阶段。','设置播放范围和帧率，循环检查后再导出。'],
 '为同一待机动作做均匀节奏与“停留后快速摆动”两个版本，保持绘制帧数相同。',
 ['没有意外在错误图层上创建帧。','动作时长和帧率可由记录复现。','循环范围不会包含空白尾帧。'],
 '时间轴教程跨多个 Krita 版本；菜单名、帧状态图示以所用版本为准，先用小文档验证。'),
('onion-skin','reference_manual/dockers/onion_skin','洋葱皮：比较前后姿势与消除帧间漂移','beginner',['onion-skin','alignment','animation','洋葱皮','对齐'],
 '在当前帧上显示前后关键姿势，检查轮廓变化、重心和锚点。',
 ['在包含关键帧的透明动画图层上打开灯泡图标。','在 Onion Skin Docker 选定要显示的前后帧偏移，先只保留最近一帧。','调节总透明度、每个偏移的透明度与前后帧颜色，保持当前帧最清楚。','逐帧检查脚底、头部及道具位置，修正无意的漂移，再关闭洋葱皮看真实播放。'],
 '用洋葱皮检查一个四帧眨眼或呼吸循环，列出并修正三处无意移动。',
 ['当前帧与参考帧可清晰区分。','背景的白色没有被误当透明。','关闭洋葱皮后最终轮廓无残留。'],
 '完全不透明的默认像素图层不能正常提供所需洋葱皮效果；使用新建透明动画图层。'),
('render-animation','reference_manual/render_animation','导出动画：PNG 序列、像素放大与编码','intermediate',['export','png-sequence','nearest','导出','帧序列'],
 '把可编辑动画变成引擎可接收的图像序列，同时理解预览视频的缩放与编码限制。',
 ['设置 First Frame 与 Last Frame，并核对导出范围是否包含完整循环。','启用图像序列导出，选择保存位置、基础名称与编号起点。','区分逐时间帧导出与 Only Unique Frames；后者需要另行保留各关键帧的持续时长。','需要放大预览时选整数倍和 Nearest Neighbour；保存后检查透明度、帧数与顺序。'],
 '把同一循环导出为透明 PNG 序列与两倍预览，比较每帧尺寸和时长是否可重建。',
 ['实际序列帧数与导出范围对应。','透明资产没有只保留带黑底的视频。','放大预览没有引入模糊插值。'],
 '手册注明 5.2 起包含部分 FFmpeg 功能；Android 路径不同。原文某些旧编号例子可能有笔误，实际文件名需检查。'),
('import-animation','reference_manual/import_animation','导入精灵表与序列帧：顺序和帧率换算','intermediate',['spritesheet','import','frame-rate','精灵表','导入'],
 '把已有角色动作导入为可编辑帧，避免文件排序和帧率变化造成动作错乱。',
 ['精灵表需先按确定的行列或切片数拆成等尺寸图像；原文示例展示九张精灵的切分。','新建目标文档，通过 File → Import Animation Frames 添加图像。','检查数字排序与字母排序，尤其是 frame_2 和 frame_10 等未补零名称。','设置 Start at 与 Step；例如 6 fps 的动作进入 24 fps 文档，可用 Step=4 保持时长。'],
 '把六张编号帧导入 24 fps 文档，先采用 Step=1 再改为 Step=4，记录时长区别。',
 ['帧顺序与动作原意相同。','所有帧画布与锚点一致。','导入后的动作时长与目标一致。'],
 '原文演示使用 Libre Pixel Cup 角色，引用保留在原文脚注；下载成品用于游戏时需另核资产许可和署名。'),
('transform-tool','reference_manual/tools/transform','变换工具：缩放、翻转与形变的适用边界','intermediate',['transform','resize','rotate','变换','像素边缘'],
 '区分可保留网格结构的简单操作与需要重新精修的任意变形。',
 ['先复制图层或保存原稿，再选择当前图层或选区作为变换对象。','在 Tool Options 输入可复现的位置、尺寸和角度，避免仅凭拖拽估计。','对像素资产优先测试整数平移、整倍缩放和 90° 旋转；对任意角度或形变单独审查。','确认后在原始尺寸对比边缘、色数、细杆和透明孔洞，必要时手工重画受损部分。'],
 '对一把像素椅子做 90° 旋转和小角度旋转两个副本，对比轮廓、细腿与孔洞。',
 ['原图留存且可回退。','变换的插值与目标规范一致。','薄结构没有被缩放或形变吞掉。'],
 '本页的透视、网格和液化面向一般绘画；它们不保证像素网格或既定俯视投影保持一致。'),
('reusable-plant','tutorials/making_an_azalea_with_the_transformation_masks','可复用植物组件：克隆图层与变换遮罩','intermediate',['plant','clone','transform-mask','植物','组件'],
 '理解从少量花叶母版组合成植物的编辑结构，再决定哪些部分适合像素素材复用。',
 ['按原文将树干、花朵和叶片分开制作，保留清楚的母版图层。','为重复花簇创建 Clone Layer，使母版修正可以传播到克隆。','给克隆加 Transform Mask，调整位置与朝向以组织植物轮廓。','在组内使用透明度继承添加阴影，最后统一检查尺度、光源与重复痕迹。'],
 '用两种叶簇母版组合一个灌木；修改其中一个母版，检查所有克隆是否同步。',
 ['母版与克隆关系可追溯。','花叶重复不造成明显机械图案。','像素版导出后仍保持统一光源与网格。'],
 '原文为普通绘画示范；像素版任意旋转和缩放后需重新整理轮廓，不能把克隆结果直接当合格精灵。'),
('multibrush','reference_manual/tools/multibrush','多重笔刷：径向结构与重复装饰','intermediate',['multibrush','symmetry','pattern','重复','对称'],
 '用同一笔画同步测试对称或平移结构，适合花朵、轮盘及重复装饰的草稿。',
 ['选择 Multibrush，在 Tool Options 选择 Symmetry、Mirror 或 Translate 等模式。','设置中心、实例数或半径，小范围试画确认分布。','使用 Copy Translate 时先开启 Add 标定副本位置，再关闭 Add 进行绘制。','结构确定后关闭多重绘制，单独处理光照、轮廓和非对称变化。'],
 '建立四瓣花的对称结构，再手工把其中两瓣改成不同形状，保持整体方向一致。',
 ['实例位置可复现。','中心没有叠加出多余暗点。','最终形体经过单独的像素轮廓检查。'],
 'Copy Translate at Interval 标注为 5.3 新增，最多 50 个画笔实例；旧版不应假定有同一模式。'),
('fill-tool','reference_manual/tools/fill','填充工具：连通区域、边界与缝隙','intermediate',['fill','threshold','gap','填充','边界'],
 '通过填充模式与参考图层设置控制“该填哪里”，尤其适合封闭道具与地表色块。',
 ['先确认填充范围是当前选区、连通区域还是全图相似颜色。','选择参考当前层、所有层或带颜色标签的层，使边界来源明确。','调整 Threshold、Spread 与选区增减，观察是否跨过细线；严格像素边缘另查抗锯齿与羽化。','有断口时比较 Close Gap 的前后效果，保留真正应当开放的孔洞。'],
 '制作含窄把手与 1px 缝隙的杯子，比较不同填充模式并保存参数。',
 ['只填目标区域，没有穿出边界。','孔洞与窄通道的处理符合形体意图。','低分辨率边缘没有残留白缝。'],
 'Close Gap 标注为 5.3 新增；类似颜色区域和若干扩张选项在 5.2 才出现。'),
('contiguous-selection','reference_manual/tools/contiguous_select','连续选区：按颜色精确选择局部区域','beginner',['magic-wand','selection','threshold','魔棒','选区'],
 '通过连续颜色范围建立局部选区，用于修边、重着色和检查封闭区域。',
 ['点击目标区域，先用较保守阈值查看选择范围。','使用增加、减去或相交模式处理多个局部，避免每次点击替换已选区域。','检查 Reference 设置与 Grow Selection，决定边界来自哪个图层以及是否扩张。','完成操作前检查羽化、抗锯齿与 Close Gap，避免跨越细杆或真正的开口。'],
 '选择树冠中同一连续色块并改色，同时保留树叶间透明空隙；与全图同色选择进行对比。',
 ['没有选到不连通的背景区域。','选区边缘与需要修整的像素一致。','选择模式与阈值已记录。'],
 'Close Gap 属于 5.3 功能，Spread 在 5.1 加入；不同版本的工具选项需先核对。'),
('colorize-mask','reference_manual/tools/colorize_mask','着色遮罩：从颜色提示生成可编辑底色','intermediate',['colorize-mask','flats','line-art','着色遮罩','底色'],
 '理解按颜色提示填色的流程和限制，适合概念或底色阶段的快速试色。',
 ['选择独立线稿层，添加 Colorize Mask 并用少量笔画标记各区域颜色。','为背景指定透明提示色，再点击 Update 查看填色结果。','按需要调整边缘检测、缝隙处理和清理参数，检查算法误连通之处。','确认颜色布局后保留原遮罩，另存或转换副本做逐像素修整。'],
 '为一个简单农具线稿标注三种颜色和透明背景，比较更新前的提示笔画与最终输出。',
 ['透明提示没有变成实际背景色。','颜色边界没有越过细线。','输出前已人工检查像素轮廓。'],
 '原文开头保留 3.1 实验开关的历史说明；4.0 起已正式提供，不要在新版本照抄旧配置步骤。'),
('indexed-colors','reference_manual/filters/artistic','索引色、像素化与色阶压缩的区别','intermediate',['index-color','pixelize','posterize','索引色','像素化'],
 '区分颜色映射、降低空间细节和减少色阶，避免把滤镜效果误当完整像素画制作。',
 ['先复制原稿，对同一小区域分别测试 Index Color、Pixelize 和 Posterize。','在 Index Color 中指定颜色与明度映射，观察灰阶转色板后的信息保留。','使用 Pixelize 时明确区块尺寸；随后对照目标像素网格检查细节与轮廓。','根据结果选择辅助步骤，并在输出前重整必要的边缘、色簇与透明孔洞。'],
 '对同一块岩石草稿做三种滤镜对照，列出颜色、轮廓和纹理分别发生什么变化。',
 ['能够分辨三种处理影响的对象。','目标颜色数量和网格大小有明确记录。','没有用“已像素化”代替视觉质量验收。'],
 '本篇保留全部 Artistic 滤镜参考；与严格像素制作直接相关的是 Index Color、Pixelize 和 Posterize 段落。'),
]
D.append(('perspective-assistants','user_manual/painting_with_assistants','透视辅助工具：为建筑和道具建立一致的空间关系','intermediate',['perspective','assistant','architecture','透视','建筑'],
 '认识平行投影与消失点透视的差别，先选择与游戏视角相符的结构，再用辅助线组织建筑。',
 ['先在项目规范里确定俯视正交、斜投影、等距还是消失点透视；不要把不同透视混入同一组素材。','按目标选择尺、平行尺或透视辅助工具，设置基线、方向和必要的消失点。','启用画笔对辅助工具的吸附，用简单箱体验证墙面、屋顶与门窗方向。','空间结构确定后缩回目标像素尺寸，人工整理斜线节奏和轮廓，不让辅助曲线代替像素精修。'],
 '为同一间小屋画平行投影与一点透视两份结构草图，标出两者哪些边平行、哪些边汇聚。',
 ['主体采用同一种投影约定。','门窗与墙面的方向一致。','辅助线只作为编辑参照，不混入导出精灵。'],
 '官方页面介绍多种一般绘画透视；俯视游戏通常需要固定投影规范，是否采用消失点必须由项目视角决定。'))
CACHE=Path('/tmp/pixel-tutorial-krita-cache'); CACHE.mkdir(exist_ok=True)
cache_lock=threading.Lock(); url_locks={}
def get(url):
 key=hashlib.sha256(url.encode()).hexdigest()
 with cache_lock: lock=url_locks.setdefault(key,threading.Lock())
 with lock:
  p=CACHE/key
  if p.exists(): return p.read_bytes()
  for attempt in range(3):
   try:
    r=requests.get(url,timeout=(15,60),headers={'User-Agent':'PixelTutorialLibrary/1.0 (educational, bounded offline collection)'})
    r.raise_for_status()
    if len(r.content)>30*1024*1024: raise ValueError('Resource exceeds 30 MiB: '+url)
    p.write_bytes(r.content); return r.content
   except Exception:
    if attempt==2: raise
    time.sleep(1+attempt)
def authors_from_rst(raw):
 m=re.search(r':authors:\s*(.*?)(?=\n\s*:license:)',raw,re.S)
 if not m: return ['Krita Documentation Contributors (no page-specific author metadata found)']
 return [re.sub(r'\s*<[^>]+>','',x).strip() for x in re.split(r'(?:^|\n)\s*-\s*',m.group(1)) if x.strip()]
def find_caption(img,n):
 alt=img.get('alt','')
 if not alt or '/' in alt: alt=Path(urlparse(img.get('src','')).path).stem.replace('_',' ').replace('-',' ')
 fig=img.find_parent('figure') or img.find_parent('div',class_='figure')
 cap=fig.select_one('figcaption,.caption') if fig else None
 if cap: alt=cap.get_text(' ',strip=True)
 return f'Figure {n}: {alt}'
def collect(index,entry):
 slug,source,title,level,tags,summary,steps,exercise,checks,note=entry
 ident=f'MAKE-{index:03d}'
 url=BASE+source+'.html'; rst_url=BASE+'_sources/'+source+'.rst.txt'
 raw=get(url); rst=get(rst_url).decode('utf-8')
 if 'free documentation license' not in rst.lower(): raise RuntimeError('Missing GFDL page notice: '+url)
 author=authors_from_rst(rst)
 soup=BeautifulSoup(raw,'html.parser',from_encoding='utf-8')
 body=soup.select_one('[itemprop=articleBody]')
 if not body or 'File Not Found' in body.get_text():raise RuntimeError('No article: '+url)
 source_title=body.h1.get_text(' ',strip=True).replace('¶','').strip()
 images=[]; image_urls={}; icon_count=0
 article_path=ROOT/'tutorials'/'asset-production'/f'{ident}-{slug}.md'
 asset_dir=ROOT/'assets'/'asset-production'/ident
 asset_dir.mkdir(parents=True,exist_ok=True); article_path.parent.mkdir(parents=True,exist_ok=True)
 # Control glyphs become explicit text, so they are readable by text-only agents.
 for img in list(body.select('img')):
  src=urljoin(url,img.get('src','')); name=Path(unquote(urlparse(src).path)).name
  alt=img.get('alt','')
  is_icon=('Krita_mouse_' in name or re.match(r'^(tool|mouse|onionon|onionoff|duplicateframe|scalaradd|pintimeline)',alt.lower()) or name in ['pixelbrush.svg'] or name.startswith('colorize-'))
  if is_icon:
   token={'mouseleft':'left mouse button','mouseright':'right mouse button','mousescroll':'mouse wheel'}.get(alt,alt or name)
   img.replace_with(NavigableString(' ['+token+'] '));icon_count+=1;continue
  if src in image_urls:
   obj=image_urls[src]
  else:
   dat=get(src); local=asset_dir/name
   local.write_bytes(dat)
   dimensions=None; frames=1
   if local.suffix.lower()!='.svg':
    with Image.open(io.BytesIO(dat)) as im:
     dimensions=list(im.size);frames=getattr(im,'n_frames',1);im.verify()
   obj={'path':str(local.relative_to(ROOT)),'source_url':src,'caption':find_caption(img,len(images)+1),'sha256':hashlib.sha256(dat).hexdigest(),'bytes':len(dat),'dimensions':dimensions,'frames':frames,'license':'GFDL-1.3-or-later unless the source body states a separate image credit','author':'See page authors and any image-specific credit retained in the source body'}
   if name=='Pepper-speedpaint-deevad.jpg':obj.update(license='CC-BY-3.0',author='David Revoy',license_url='https://creativecommons.org/licenses/by/3.0/')
   images.append(obj);image_urls[src]=obj
  img['src']=os.path.relpath(ROOT/obj['path'],article_path.parent)
  img['alt']=obj['caption'];img.attrs={k:v for k,v in img.attrs.items() if k in ['src','alt']}
  # Linked full-size figures should also open the offline file.
  if img.parent.name=='a': img.parent['href']=img['src']
 if not images:raise RuntimeError('No teaching figures: '+url)
 for x in body.select('a.headerlink,script,style,iframe'):
  if x.name=='iframe':
   link=x.get('src','');x.replace_with(NavigableString('Embedded media (not downloaded or transcribed): '+urljoin(url,link)))
  else:x.decompose()
 for a in body.select('a[href]'):
  h=a['href']
  if not h.startswith('../../assets/') and not h.startswith('#'):a['href']=urljoin(url,h)
 for h in body.select('h1,h2,h3,h4,h5'):
  h.name='h'+str(min(6,int(h.name[1])+1))
 # Preserve anchors so #links in the converted source remain meaningful.
 anchors={}
 for n,x in enumerate(body.select('[id]')):
  if x.get('id'):
   token=f'KritaAnchorQ{n:05d}Z'
   anchors[token]='<a id="'+x['id']+'"></a>'
   x.insert_before(NavigableString('\n\n'+token+'\n\n'))
 content=markdownify(str(body),heading_style='ATX',bullets='-',wrap=False,strip=['span'])
 for token,value in anchors.items():content=content.replace(token,value)
 content=re.sub(r'\n{3,}','\n\n',content).strip()
 src_dir=ROOT/'sources'/'asset-production'/ident;src_dir.mkdir(parents=True,exist_ok=True)
 src_file=src_dir/'original.rst';src_file.write_text(rst,encoding='utf-8')
 meta={'id':ident,'title':title,'category':'asset-production','path':str(article_path.relative_to(ROOT)), 'source_url':url,'source_title':source_title,'author':author,'license':'GFDL-1.3-or-later','license_url':LICENSE_URL,'license_evidence_url':rst_url,'retrieved_at':DATE,'language':'zh-CN+en','source_language':'en','level':level,'tags':tags,'summary':summary,'images':images,'content_mode':'licensed-fulltext-with-chinese-guide','version':VERSION,'prerequisites':['能够新建、保存和打开 Krita 文档','已有明确的目标像素尺寸或练习画布'],'learning_objectives':[steps[0],steps[-1]],'source_rst_path':str(src_file.relative_to(ROOT)),'source_html_sha256':hashlib.sha256(raw).hexdigest(),'source_rst_sha256':hashlib.sha256(rst.encode()).hexdigest(),'editorial_exercise':exercise,'version_notes':note,'control_icons_replaced_with_text':icon_count}
 fm={k:v for k,v in meta.items() if k not in ['images','learning_objectives','editorial_exercise','control_icons_replaced_with_text']}
 guide='---\n'+yaml.safe_dump(fm,allow_unicode=True,sort_keys=False,width=120)+'---\n\n# '+title+'\n\n'
 guide+='> **内容边界**：下方“授权原文”是官方主内容的 Markdown 转换；中文操作路线、练习与验收由整理者编写，不是作者逐句翻译，也不代表已在本机运行软件验证。\n\n'
 guide+='## 中文任务导读\n\n'+summary+'\n\n**前提**：能够新建、保存和打开 Krita 文档；先确定目标像素尺寸、色板与透明度要求。\n\n'
 guide+='### 操作路线\n\n'+'\n'.join(f'{i}. {v}' for i,v in enumerate(steps,1))+'\n\n'
 # Choose a useful lead figure, avoiding the conceptual painting at start of common workflows.
 lead_names={1:'Layer-docker-pixelart.png',2:'Resize_Canvas.png',3:'Layer-composite.png',12:'animation_walkcycle_2021_4_frames.gif',23:'Index-color-filter.png',24:'Assistants_dimetric.png'}
 lead=next((obj for obj in images if Path(obj['path']).name==lead_names.get(index)),images[0])
 guide+='### 配图怎么读\n\n'
 guide+=f'![{title}：官方示意图]({os.path.relpath(ROOT/lead["path"],article_path.parent)})\n\n'
 readings={
 1:'图层堆叠展示索引色、抖色图案与底稿的相对位置；重点看每一层负责改变颜色还是改变画面本身。',
 2:'这里是扩展画布对话框，重点看宽高、保持比例和偏移控制；增加空白不应自动改变原有精灵的像素尺寸。',
 3:'合成示意图把图层当作依次叠放的透明平面；先确认组内合成，再理解上层如何受到下层透明范围限制。',
 4:'动态图展示图层组先单独合成，再参与整幅图像的叠放；后续逐步截图对比普通笔触与继承透明度后的边界。',
 5:'截图把底色和线稿分开；阅读时比较当前选中图层、混合模式以及填充是否伸入线条下方。',
 6:'蚂蚁线只表示选区边界，并不显示全部透明程度；后续遮罩显示方式可以帮助判断柔边或遗漏区域。',
 7:'剑的上下两侧围绕同一轴同步绘制；先检查轴的位置，再决定哪些非对称细节应在关闭镜像后处理。',
 8:'预设保存对话框同时包含名称和预览图；保存成功后还要重载，确认笔尖、压力响应等参数一并保留。',
 9:'笔刷设置面板中的参数列表提示哪些属性可能影响笔触；图中的软笔刷只是引擎示例，不是推荐的像素修边配置。',
 10:'色板截图展示了按行列和分组存放的颜色；把同材质的亮暗色排在一起，可以让不同素材复用同一色阶。',
 11:'网格图中主线和细分线颜色不同；右侧参数控制间距与细分，不能只根据屏幕显示猜测实际像素间距。',
 12:'循环示例用少量姿势构成连续步态；看脚的接触顺序、身体上下运动以及最后一帧回到第一帧的衔接。',
 13:'带标注的时间轴截图把图层、帧和播放控制放在同一面板；区分当前帧指示与真正存有图像内容的关键帧。',
 14:'洋葱皮面板把当前帧两侧的偏移分开控制，红绿颜色区分过去与未来；透明度只影响参照，不应写进输出图。',
 15:'导出窗口同时显示序列与视频设置；源截图采用旧版界面，重点识别范围、尺寸和编码器字段，再对照所用版本。',
 16:'第一张图展示在等间隔精灵表上切分；后续图片展示添加序列与导入后的时间轴，注意切片数和输出帧数的差别。',
 17:'变换面板含坐标、尺寸与过滤器；过滤器会影响低分辨率边缘，不能仅凭预览位置正确就认定像素未受损。',
 18:'成品植物由多个花叶簇组合而成；后续截图追踪母版、克隆和变换遮罩，重点学习编辑结构而不是复制成品造型。',
 19:'放射状笔触围绕中心重复，展示实例数量和角度的影响；像素资产还需单独处理中心重叠和不对称照明。',
 20:'四个并排图对比同一次点击在不同填充模式下影响的范围；看绿色覆盖了选区、连通块还是所有相似颜色。',
 21:'原图、未闭合缝隙时的选区和闭合缝隙后的选区并排出现；粉色用于突出选择范围，不是作品最终颜色。',
 22:'图层面板中独立的线稿是着色遮罩的输入；后续截图依次展示提示色、透明色与更新结果，避免把提示笔画当输出。',
 23:'索引色设置图把选定颜色对应到亮暗范围；它主要重新分配颜色，并不会自动修复不合适的轮廓或透视。',
 24:'平行投影示意中的各组边保持各自方向；与后文一点、两点透视的汇聚线比较，先确定项目到底使用哪种投影。'}
 guide+=readings[index]+' 图内界面与作品保留原貌；示例转用于像素素材时仍按本篇验收条件检查。\n\n'
 guide+='### 练习与验收（整理者补充）\n\n'+exercise+'\n\n'+'\n'.join('- [ ] '+x for x in checks)+'\n\n'
 guide+='### 版本与适用边界\n\n'+note+'\n\n抓取时页面标题标注 **Krita Manual 5.3.0**；这是文档快照版本，不构成已发布软件版本或本机功能的验证。原文中保留的 `Added/Changed/Deprecated in version` 是兼容性依据。\n\n'
 guide+='## 来源、许可与修改记录\n\n'
 guide+=f'- 原文：[{source_title}]({url})\n- 作者：'+ '；'.join(author)+'\n'
 guide+=f'- 页内作者与许可原始声明：[RST 源文件]({os.path.relpath(src_file,article_path.parent)})；[线上原始声明]({rst_url})。\n'
 guide+=f'- 许可：[GNU Free Documentation License 1.3 or later]({LICENSE_URL})；[本地许可证全文](../../licenses/krita-GFDL-1.3.txt)。各图若有独立作者或许可，沿用原文紧邻图像的署名，不把作品许可自动泛化为文档许可。\n'
 guide+='- 修改历史：2026-10-29，Codex 为本教程库新增中文导读、练习和验收；将官方 HTML 主内容转换为 Markdown，去除导航与页脚，将控制图标转为文字、将教学图像存为本地文件。正文、步骤、代码、表格与图像说明保留。\n'
 guide+='- 本修改版沿用 GFDL 1.3 或更新版本。保留作者声明和上游链接；未添加 Invariant Sections、Front-Cover Texts 或 Back-Cover Texts。外链视频、安装包和关联页面没有自动下载或转录。\n\n'
 guide+='## 授权原文（英语，完整主内容转换）\n\n'+content+'\n\n'
 guide+='## 本地配图清单\n\n| 图 | 本地文件 | 原始来源 |\n|---|---|---|\n'
 for i,obj in enumerate(images,1):
  cap=obj['caption'].replace('|','\\|').replace('\n',' ')
  guide+=f'| {i} | [{cap}]({os.path.relpath(ROOT/obj["path"],article_path.parent)}) | [原图]({obj["source_url"]}) |\n'
 article_path.write_text(guide,encoding='utf-8')
 print(ident,source_title,len(content),len(images),flush=True)
 return meta

def main():
 (ROOT/'licenses').mkdir(exist_ok=True)
 (ROOT/'licenses'/'krita-GFDL-1.3.txt').write_bytes(get(LICENSE_SOURCE))
 (ROOT/'licenses'/'krita-licensing-evidence.md').write_text('# Krita 文档许可核验\n\n核验日期：2026-10-29。\n\n- [官方文档标记规范]('+CONVENTIONS+') 明确说明手册使用 GFDL 1.3。\n- [文档仓库 LICENSE]('+LICENSE_SOURCE+') 的原文保存在 `krita-GFDL-1.3.txt`。\n- 每篇 `sources/asset-production/MAKE-xxx/original.rst` 保留该页作者和 `GNU free documentation license 1.3 or later` 元数据。\n- 每个 Markdown 的历史段明确本次转换与中文补充，修改版沿用同一许可。\n- 图像如有独立许可与作者，保留原文图旁的声明；例如 Common Workflows 中 David Revoy 的 Pepper & Carrot 作品标为 CC BY 3.0。\n\n本次不把软件 GPL 自动套用到文档，也不把 Tiled TMX 格式页面的 CC BY-SA 声明扩展为整个 Tiled 手册的许可。\n',encoding='utf-8')
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  records=list(pool.map(lambda x:collect(*x),enumerate(D,1)))
 records.sort(key=lambda x:x['id'])
 (ROOT/'manifests').mkdir(exist_ok=True)
 (ROOT/'manifests'/'asset-production.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('COMPLETE',len(records),'pages',sum(len(x['images']) for x in records),'figures',flush=True)

if __name__=='__main__':main()
