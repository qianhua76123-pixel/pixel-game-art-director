#!/usr/bin/env python3
"""Build a source-backed task brief with tutorials, figures and workflow checks."""
from pathlib import Path
import argparse,hashlib,json,shutil,sys
from search import Library,ROOT

NOTICE='这是制作任务的阅读与执行简报，不是已生成的游戏资产。教学配图用于理解方法，不能因可离线阅读就当作项目成品素材。'

def file_link(label,path):
    return '['+str(label).replace(']','\\]')+'](<'+str(path)+'>)'

def build(task,out,limit=8,style=None,ui_style=None,copy_figures=False,library_root=ROOT):
    lib=Library(library_root)
    result=lib.search(task,'all',limit,2,style,ui_style,False,True)
    tutorials=[x for x in result['results'] if x['kind']=='tutorial']
    style_candidates=[x for x in result['results'] if x['kind']=='style']
    ui_candidates=[x for x in result['results'] if x['kind']=='ui']
    cases=[x for x in result['results'] if x['kind']=='case']
    matched=lib.match_routes(task)
    selected_routes=matched[:2] if len(matched)>1 and matched[1]['score']>=matched[0]['score']*.75 else matched[:1]
    # Keep UI or audit work primary when it explicitly occurs in the request.
    if selected_routes and selected_routes[0]['id'] in ['game-ui','consistency-audit','asset-cleanup']:
        selected_routes=selected_routes[:1]
    out=Path(out).expanduser().resolve()
    if out==lib.root or lib.root in out.parents:raise ValueError('Choose --out outside the installed skill folder to keep the knowledge package unchanged.')
    out.mkdir(parents=True,exist_ok=True)
    copied=[]
    if copy_figures:
        for tutorial in tutorials:
            for n,figure in enumerate(tutorial.get('figures',[]),1):
                source=Path(figure['absolute_path']);dest=out/'figures'/f'{tutorial["id"]}-{n:02}-{source.name}'
                dest.parent.mkdir(exist_ok=True)
                shutil.copyfile(source,dest)
                figure['bundle_path']=dest.relative_to(out).as_posix()
                copied.append(dict(figure,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
        # Preserve local license texts along with exported teaching figures.
        license_sources={'CC-BY-4.0':'CC-BY-4.0.txt','CC-BY-3.0':'CC-BY-3.0.html','GFDL-1.3-or-later':'krita-GFDL-1.3.txt'}
        for image in copied:
            name=license_sources.get(image.get('license'))
            if name:
                source=lib.library/'licenses'/name
                if not source.is_file():raise ValueError('Required local license document is missing: '+str(source))
                destination=out/'licenses'/name;destination.parent.mkdir(exist_ok=True)
                shutil.copyfile(source,destination)
                image['bundle_license_file']=destination.relative_to(out).as_posix()
        (out/'figure-attributions.json').write_text(json.dumps(copied,ensure_ascii=False,indent=2)+'\n')
    bundle={'schema_version':1,'status':result['status'],'task':task,'notice':NOTICE,
            'skill_root':str(lib.root),'selected_style':style,'selected_ui_style':ui_style,
            'style_selection_state':'selected' if style else ('candidates-only' if style_candidates else 'unspecified'),
            'ui_style_selection_state':'selected' if ui_style else ('candidates-only' if ui_candidates else 'unspecified'),
            'tutorials':tutorials,'style_candidates':style_candidates,'ui_style_candidates':ui_candidates,
            'ui_case_references':cases,
            'workflow':[{'route_id':r['id'],'name':r['name'],'steps':r['steps'],'acceptance':r['acceptance']} for r in selected_routes],
            'review_requirements':{'machine':'Run scripts/audit_assets.py against a configured contract when assets exist. Unconfigured checks do not imply PASS.',
                'visual':['视角与接地','主光与阴影方向','轮廓节奏与细节密度','材质语法','UI文字与交互状态'],
                'evidence':'实际原图、同倍率联系表、项目规范与真实界面截图；不能用检索结果代替审美通过。'},
            'copied_figure_count':len(copied),
            'no_match_note':result['note'] if result['status']=='no_match' else None}
    (out/'task-brief.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n')
    lines=['# 像素制作任务简报','',task,'',NOTICE,'']
    if not tutorials:
        lines+=['## 检索状态','',result['note'],'']
    lines+=['## 风格约定','']
    if not style_candidates and not ui_candidates:
        lines+=['本次任务没有足够线索选择风格。沿用项目已有规范；若没有，先明确视角、逻辑像素、调色板、主光、轮廓和材质，再制作。','']
    for title,profiles,explicit in [('美术风格',style_candidates,style),('UI风格',ui_candidates,ui_style)]:
        if profiles:
            lines+=[f'### {title}'+('（本次调用指定，非用户审批记录）' if explicit else '（候选，尚未锁定）'),'']
            for p in profiles:
                lines+=['- **'+str(p['title'])+'** `'+p['id']+'`：'+str(p.get('summary','')),
                        '  '+file_link('完整规范',p['absolute_path'])+'；匹配依据：'+'；'.join(p['reasons'])]
                checks=p.get('visual_checks',[])
                if checks:lines+=['  检查重点：'+'；'.join(str(x) for x in checks[:3])]
            lines+=['']
    lines+=['## 核心教程与配图','']
    for t in tutorials:
        lines+=[f'### {t["id"]} · {t["title"]}','',str(t.get('summary','')),'',
                file_link('阅读完整MD',t['absolute_path'])+' · [原始来源]('+t['source_url']+')',
                '', '匹配依据：'+'；'.join(t['reasons'])+'。',
                '',f'版本：{t["version"]}；许可：[{t["license"]}]({t["license_url"]})；作者：'+str(t['author'])+'。','']
        for i,figure in enumerate(t.get('figures',[])):
            image_path=figure.get('bundle_path',figure['absolute_path'])
            label=figure.get('caption','教学图') or '教学图'
            if i==0:lines+=['!['+label.replace(']','\\]')+'](<'+str(image_path)+'>)','']
            else:lines+=[file_link('辅助图：'+label,image_path),'']
            lines+=['配图来源：[原图]('+figure['source_url']+')；许可：'+str(figure['license'])+'。仅作教学参考。','']
    if cases:
        lines+=['## 真实游戏 UI 案例参考','',
                '以下为官方截图的静态观察与整理者评析。图片仅保留远程链接，不随 --copy-figures 复制；不能用于提取可分发游戏素材，也不能代替中文/手柄/交互实测。','']
        for c in cases:
            lines+=['### '+c['title'],'','[官方来源]('+c['source_url']+') · '+c['summary'],'',
                    '可借鉴：'+'；'.join(c['strengths']),'',
                    '局限：'+'；'.join(c['limitations']),'']
            for figure in c['figures']:
                lines+=['[参考截图：'+figure['caption']+']('+figure['url']+')','']
    lines+=['## 制作路线（整理者编排）','']
    if not selected_routes:
        lines+=['未匹配到已有制作路线。请读取命中的教程并据项目约束拟定步骤，不把一般流程冒充当前任务的已验证方案。','']
    for route in selected_routes:
        lines+=['### '+route['name'],'']
        lines += [f'{n}. {step}' for n,step in enumerate(route['steps'],1)]+['','验收条件：','']
        lines += ['- [ ] '+item for item in route['acceptance']]+['']
    lines+=['## 检查与交付边界','',
        '- 建立或沿用项目美术规范；候选风格不表示已替用户决定。明确哪些参数是固定要求、哪些是可调建议。',
        '- 有实际素材后，按合同运行一致性测量，生成联系表与报告。尺寸、色板、透明度等实测结果不能代替视角、光源、材质与UI观感审阅。',
        '- 以真实原图、同倍率比较和实际游戏界面为证据；没有素材或运行画面时，不声称效果已经通过。',
        '- 记录读取过的教程ID与图源；图像生成或编辑使用当前项目可用且获授权的工具，本简报不自动调用收费服务。','']
    if copied:lines+=['选定教学配图已复制到 `figures/`；逐图出处、哈希和随附许可文件见 [figure-attributions.json](figure-attributions.json)。重分发时继续保留各自许可与署名。','']
    (out/'task-brief.md').write_text('\n'.join(lines)+'\n')
    return {'status':bundle['status'],'task':task,'tutorials':len(tutorials),'style_candidates':len(style_candidates),
            'ui_style_candidates':len(ui_candidates),'copied_figures':len(copied),
            'markdown':str(out/'task-brief.md'),'json':str(out/'task-brief.json')}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='');p.add_argument('--task');p.add_argument('--out',required=True)
    p.add_argument('--limit',type=int,default=8);p.add_argument('--style');p.add_argument('--ui-style')
    p.add_argument('--copy-figures',action='store_true',help='Copy selected teaching figures with attribution records into the task bundle')
    a=p.parse_args(argv);task=a.task if a.task is not None else a.query
    if not task.strip():p.error('Provide --task or a positional task')
    if not 1<=a.limit<=30:p.error('--limit must be between 1 and 30')
    try:result=build(task,a.out,a.limit,a.style,a.ui_style,a.copy_figures)
    except (ValueError,OSError,json.JSONDecodeError) as ex:
        print(json.dumps({'status':'error','error':str(ex)},ensure_ascii=False));return 2
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':sys.exit(main())
