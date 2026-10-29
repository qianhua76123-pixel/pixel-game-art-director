#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eight selected, licensed additions for the pixel-game-art-director skill."""
from pathlib import Path
import importlib.util,json,hashlib,os
import yaml
from PIL import Image
R=Path(__file__).resolve().parents[1]
COMMIT='ce1393eb2c46441d917134a9fd52e15575ee10a7'
rows=json.loads((R/'manifests/supplement-images.json').read_text())
lessons=[
 dict(id='UI-001',slug='nine-slice',title='像素UI九宫格：固定角、可平铺边与文字区',category='ui-design',files=['UI-9-Slice.gif','UI-9-Slice-names.gif'],tags=['UI','nine-slice','9-slice','九宫格','边框','按钮','面板'],summary='让一个像素面板覆盖不同宽高，同时保留角部与边缘的像素结构。',steps=['把矩形拆成4个角、4条边和中心；角部保持尺寸，横边只沿横向扩展，竖边只沿纵向扩展。','原图建议边缘能与角及自身重复衔接；中心与边缘少放高频细节，角部可以更丰富。','边缘优先重复平铺。原作者提醒拉伸只适合很少细节的边；像素图仍要检查实际显示后的网格。','给标题、页脚或特殊顶部另作变体，不必强迫所有面板共用一个外框。','细长的血条、滑块和分隔条可以用三段切片；是否横向或竖向由伸展方向决定。'],reading='第一张原图展示九宫格、横竖扩展、标题/页脚变体和三段条形；第二张是同一教程的corner、edge、middle命名图，不另计新教程。',exercise='整理者练习：为背包做窄提示框、宽物品说明框和高列表框，复用同一组角与边；把真实长中文描述放入中部安静区域。',checks=['角部没有拉伸变形','相邻边重复无明显接缝','文字没有压到纹理与装饰','选中、按下、焦点和禁用仍可区分'],boundary='原图讲的是切片结构，不提供输入逻辑、可访问性认证或引擎按钮状态实现。'),
 dict(id='STYLE-001',slug='one-bit-design',title='双色1-bit画法：形状、抖色与图标辨识',category='drawing',files=['1-bit.gif'],tags=['1-bit','one-bit','双色','单色','风格','图标','抖色'],summary='用两个可见颜色组织大形、阴影和图标，不依赖连续色阶。',steps=['先用轮廓和少量实心阴影块定义大形；原图提示避免过多细节。','需要软阴影观感时可使用规则抖色；过量抖色容易混乱，应在原尺寸检查。','用白描边、黑描边，必要时双层线来分离背景；注意细线意外黏连。','做图标时先选最能代表物体或概念的一个特征；无法识别时从草图重新迭代。','像素抗锯齿空间有限时，直线和规律角度通常更容易组织；也可通过流畅动画补充表达。'],reading='上左讲抖色；上右用脸部对比细节密度；中间展示描边分离与线条黏连；底部是图标简化和规则角度示例。',exercise='整理者练习：仅用两个不透明颜色绘制镰刀、水壶、钥匙、木材四个16×16图标，透明底单独计算；不借助文字让人辨认。',checks=['可见颜色只有约定两色','图标在最终尺寸仍可识别','抖色没有吞没主轮廓','必要孔洞保留'],boundary='这是双色画法配方，不等同某一历史机器的完整硬件限制；透明色、UI文字色和特效例外应单独写进合同。'),
 dict(id='FLOW-001',slug='animation-planning',title='复杂动画规划：草稿、关键姿势与中间帧',category='asset-production',files=['Planning.gif'],tags=['planning','动画规划','关键帧','流程','分层'],summary='先确定动作含义和节奏，再投入细节与插帧。',steps=['先明确正在制作哪个角色、对象与动作；原图从待机的第一帧作为基准。','画粗略动画草稿，建立基本动作和时间感，暂时不追求所有细节。','选择最能描述动作的关键姿势并完成它们。','补充关键姿势之间的空缺；使用局部复制等方法辅助，但以动作节奏为验收。','最后增加额外中间帧，再调时序；草稿可用颜色区分不同深度，复杂动作也可分别管理文件。'],reading='图从静止姿势流向粗稿、关键帧、中间帧、额外帧；底部提示以颜色区分深度，并可将不同动作分别存放。',exercise='整理者练习：为挥锄动作提交粗稿GIF、关键帧版、完成版三个阶段，每阶段记录修改动作原因。',checks=['关键帧即可看懂动作','增加帧数没有掩盖错误姿势','所有阶段保留同一画布与锚点'],boundary='原图是工作习惯建议，不意味着必须把每个动画拆到多个文件；项目工具和团队约定可以决定组织方式。'),
 dict(id='FLOW-002',slug='pixel-art-process',title='像素美术制作顺序：剪影、色块、轮廓与精修',category='asset-production',files=['Pipeline.gif'],tags=['pipeline','美术一致性','剪影','色块','光源','精修'],summary='先建立剪影和大色块，再上光与细节，持续回看姿势和整体阅读。',steps=['先让角色在剪影里可识别；暂不担心细小装饰。','组织大的颜色块；画细节时仍继续保持大色块的主次。','为重要物体与前景加入轮廓分离，必要时在同一对象内也使用内轮廓区分结构。','逐色加入光影，控制噪点；原作者偏好较大的像素簇。','细节阶段继续修剪影、姿势与背景；末尾清理噪点，检查颜色、光源方向和难读区域。'],reading='动态图先演示完整绘制，再以箭头和下方卡片回顾阶段；仅看首帧的空白画布无法理解。本文附后期关键帧供静态阅读。',exercise='整理者练习：做一组村民道具，每件分别保存剪影、色块、光影、精修四版。每轮先对比整组光源与颜色，再继续加细节。',checks=['剪影阶段已经可识别','细节不会破坏大色块','光源方向一致','最终检查包含原始尺寸阅读'],boundary='教程中过程GIF的演示人物是教学参考，不是本skill自动生成的成品素材。'),
 dict(id='MAKE-025',slug='modular-animation',title='模块化像素动画：部件拆分、遮挡与局部逐帧',category='asset-production',files=['Modular.gif'],tags=['modular','模块化','关节','动画','遮挡','机械'],summary='按部件制作较大像素角色，利用遮挡隐藏接缝，并保留需要逐帧重画的部分。',steps=['先画整体草图，确认各部件如何组合及遮挡。','单独制作部件，隐藏在其他部件后方的区域也需补完整。','移动和旋转部件构建动作；并非所有部件都能免于逐帧动画。','把需要弯曲的接缝藏到其他部件后，或用关节材质帮助解释连接处。','机械部件可以加入多层与旋转点附近的细节；避免没有可见支点的旋转。'],reading='大怪物展示部件与遮挡；下方小人物说明小素材也可用但收益有限；机械臂和靴子示范关节材质与旋转连接。',exercise='整理者练习：拆分一只两节机械臂，给旋转关节预留遮挡区域，并在几个关键角度检查像素旋转后的边缘。',checks=['隐藏部分有足够延展','关节没有裂缝','旋转点可被结构解释','需要逐帧修整的区域有记录'],boundary='部件旋转可能改变像素节奏；引擎实时变换与手工像素动画是不同取舍，不能自动宣称所有角度都保持像素完美。')]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def originals(lesson):return [x for x in rows if x['id']==lesson['id'] and x['file'] in lesson['files']]
def build_images(l):
 out=[]
 for r in originals(l):
  p=R/r['path'];im=Image.open(p)
  out.append(dict(path=r['path'],source_url=r['source_url'],caption=l['reading'],sha256=sha(p),author='Pedro Medeiros (Saint11)',license='CC-BY-4.0',role='original'))
  indexes=sorted(set([0,im.n_frames//2,im.n_frames-1]))
  if l['id']=='FLOW-002':indexes=[19,22,24,27]
  for n in indexes:
   im.seek(n);dest=p.parent/(p.stem+f'-frame-{n:03}.png');im.convert('RGBA').save(dest)
   out.append(dict(path=dest.relative_to(R).as_posix(),source_url=r['source_url'],caption=f'{r["file"]} 第{n}帧截取（0开始，非逐帧全集）',sha256=sha(dest),author='Pedro Medeiros (Saint11)',license='CC-BY-4.0',role='keyframe',derived=True))
 return out

def make_saint(l):
 md=R/'tutorials/supplement'/f'{l["id"]}-{l["slug"]}.md';md.parent.mkdir(parents=True,exist_ok=True)
 source=f'https://github.com/saint11/Saint11Tutorials/blob/{COMMIT}/{l["files"][0]}'
 entry={k:l[k] for k in ['id','title','category','tags','summary']}
 entry.update(path=md.relative_to(R).as_posix(),source_url=source,source_title=l['files'][0],author='Pedro Medeiros (Saint11)',license='CC-BY-4.0',license_url='https://creativecommons.org/licenses/by/4.0/',retrieved_at='2026-10-29',language='zh-CN',source_language='en',level='intermediate',content_mode='translated-image-tutorial',version='git:'+COMMIT,prerequisites=['能读取像素画布与时间轴'],learning_objectives=l['steps'],images=build_images(l))
 fm={k:v for k,v in entry.items() if k!='images'}
 text='---\n'+yaml.safe_dump(fm,allow_unicode=True,sort_keys=False)+'---\n\n# '+l['title']+'\n\n'+l['summary']+'\n\n'
 text+='## 原图与静态辅助图\n\n'
 for im in entry['images']:
  text+=f'![{im["caption"]}]({os.path.relpath(R/im["path"],md.parent)})\n\n'
 text+='## 读图\n\n'+l['reading']+'\n\n## 根据原图整理的步骤\n\n'+''.join(f'{i}. {s}\n' for i,s in enumerate(l['steps'],1))+'\n'
 text+='## 练习（整理者补充）\n\n'+l['exercise']+'\n\n## 验收（整理者补充）\n\n'+''.join('- [ ] '+s+'\n' for s in l['checks'])+'\n'
 text+='## 适用边界\n\n'+l['boundary']+' 原图为教学材料；不可把阅读或插入参考图说成已制作游戏美术。\n\n'
 text+=f'## 来源与许可\n\n作者Pedro Medeiros（Saint11），[固定来源]({source})。仓库[README许可声明](https://github.com/saint11/Saint11Tutorials/blob/{COMMIT}/README.md)为[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。原GIF保持原样；PNG为抽帧；中文为人工读图整理而非逐字OCR；练习与验收为整理者补充。新增内容继续按CC BY 4.0提供并保留原作者署名。\n'
 md.write_text(text);return entry

guides=[
 dict(id='UI-002',slug='gui-theme-system',source_path='tutorials/ui/gui_skinning.html',title='游戏UI主题：颜色、字体、图标与状态外观的统一',level='intermediate',tags=['UI','theme','StyleBox','皮肤','美术一致性','按钮'],summary='使用Theme资源统一项目界面的颜色、字体、图标与StyleBox，并理解局部覆盖的优先级。',prerequisites=['DEV-001','基本Control节点'],steps=['先列出按钮、标签和面板在项目中共享的颜色、字体大小、图标和背景外观。','创建共享Theme资源，在项目级或Control分支根节点应用，并在各独立场景预览。','使用type variation区分Header等语义角色，避免每个节点重复局部修改。','焦点StyleBox覆盖在基础状态上；设计为边缘或适当透明的框，避免遮住普通/按下外观。','出现不一致时先检查local override，再查最近的父Control主题和项目主题，避免误改全局资源。'],exercise='整理者练习：用同一Theme做背包、商店与设置三张面板，修改一个字体参数后检查三处都更新；刻意保留一个局部覆盖并解释其例外原因。',checks=['组件状态语义一致','局部覆盖有明确理由','焦点可见且不掩盖按下状态','长中文文案可读'],caution='本篇是主题机制，原站游戏示例图不等于可直接复用的UI成品素材。'),
 dict(id='UI-003',slug='ui-containers',source_path='tutorials/ui/gui_containers.html',title='游戏UI布局：容器、物品网格、长文本与可变尺寸',level='intermediate',tags=['UI','Container','layout','背包','物品栏','容器'],summary='用布局容器组织背包网格、属性行与可滚动说明，避免图文重叠。',prerequisites=['UI-002'],steps=['选择适合信息结构的HBox/VBox/Grid或Margin等容器，不先把每个子控件固定到绝对位置。','加入Container的Control子节点由父容器管理位置；手工拖动结果可能在下一次布局时被覆盖。','分别检查横向和纵向的Fill、Expand和Shrink设置，控制谁获得剩余空间。','用嵌套容器组合物品网格、说明区和底部操作；用PanelContainer保留面板样式边距。','加入最长名称、最大数量和最低支持窗口尺寸；必要时滚动或重排，避免把全部文本缩得更小。'],exercise='整理者练习：做一个4列背包和物品说明面板；使用短名、长中文名、99与9999数量以及空物品栏测试。',checks=['容器调整时不覆盖文字','按钮仍在可视区域','扩展与收缩行为能解释','九宫格装饰不占正文空间'],caution='容器决定布局，不决定美术风格。原文提及某些工具式UI，不要求把游戏改成网页仪表盘。'),
 dict(id='UI-004',slug='ui-anchors',source_path='tutorials/ui/size_and_anchors.html',title='游戏HUD锚点：宽高比变化中的定位与安全边距',level='beginner',tags=['UI','HUD','anchors','锚点','分辨率','布局'],summary='让角落HUD、居中弹窗和边缘控件在窗口变化时维持合理关系。',prerequisites=['DEV-020'],steps=['确认Control以父Control或视口作为参考。','用0到1的anchor位置表示相对边缘，用offset描述相对于anchor的像素距离。','固定在右下角的控件按右/下锚点设置偏移；居中控件可采用0.5锚点与半尺寸的正负偏移。','使用编辑器Anchor预设提高效率，再检查是否需要容器接管复杂排布。','在多个宽高比和界面倍率下检查四角HUD、居中面板、文字与安全边距。'],exercise='整理者练习：为像素村庄做左上状态、右下快捷栏和居中对话框，改变窗口宽高比并记录它们各自的参考边。',checks=['关键HUD未出屏','弹窗居中且文字未截断','offset与anchor的意义清楚','游戏世界像素倍率与UI阅读倍率分别考虑'],caution='锚点是布局关系，不是整数像素缩放的替代方案；清晰度还需DEV-021与DEV-022。')]

if __name__=='__main__':
 entries=[make_saint(l) for l in lessons]
 spec=importlib.util.spec_from_file_location('collector',R/'tools/collect_game_development.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 for g in guides:
  e=mod.collect(g);e['category']='ui-design'
  md=R/e['path'];txt=md.read_text().replace('category: game-development\n','category: ui-design\n',1);md.write_text(txt)
  e['markdown_sha256']=sha(md);entries.append(e)
 (R/'manifests/supplement.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
 print('Supplement tutorials:',len(entries))
