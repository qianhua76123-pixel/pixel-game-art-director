#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Start a project art bible from optional editorial profiles; no asset generation."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]

def profile(filename, ident):
    if not ident:return None
    data=json.loads((ROOT/'references'/filename).read_text())
    for p in data['profiles']:
        if p['id']==ident:return p
    raise ValueError(f'Unknown profile {ident!r}; valid: '+', '.join(p['id'] for p in data['profiles']))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--style');ap.add_argument('--ui-style');ap.add_argument('--name',default='未命名像素项目')
    ap.add_argument('--task',default='');ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--use-palette-for-audit',action='store_true',help='Explicitly require exact starter palette colors; review before use')
    ap.add_argument('--alpha-policy',choices=['binary','opaque','allow_partial'])
    ap.add_argument('--force',action='store_true')
    args=ap.parse_args()
    try:
        art=profile('style-profiles.json',args.style);ui=profile('ui-profiles.json',args.ui_style)
        if args.use_palette_for_audit and not art:raise ValueError('--use-palette-for-audit requires --style')
        out=args.out.expanduser().resolve()
        names=['art-bible.json','audit-contract.json','art-bible.md']
        if not args.force and any((out/n).exists() for n in names):raise ValueError('Output already contains an art bible; choose a new directory or use --force.')
        bible=json.loads((ROOT/'assets/templates/art-bible.json').read_text())
        bible.update(project_name=args.name,task=args.task or None,art_profile_id=args.style,ui_profile_id=args.ui_style)
        bible['profile_proposals']={}
        if art:
            bible['profile_proposals']['art']={k:art[k] for k in ['id','name','parameters','palette','avoid_mixing','tutorial_ids','visual_checks'] if k in art}
            bible['palette']['named_colors']=art.get('palette',{}).get('colors',[])
        if ui:
            bible['profile_proposals']['ui']={k:v for k,v in ui.items() if k not in ['figures','external_sources']}
        bible['open_decisions']=['确认项目参考图与最终投影规则','按角色/建筑/UI分别确定画布和逻辑像素密度','明确主光源方向和局部光例外','决定哪些颜色是必须精确匹配，哪些是可调色阶','在实际显示尺寸决定中文字形、字体与字号','记录动画锚点与UI状态规则']
        contract={'schema_version':1,'project':args.name,'notes':'Draft. Only explicitly requested rules are configured; all others remain NOT_CONFIGURED. Visual review is still required.','defaults':{},'roles':{},'assets':[]}
        if args.alpha_policy:contract['defaults']['alpha_policy']=args.alpha_policy
        if args.use_palette_for_audit:
            colors=[x['hex'] for x in art['palette']['colors']]
            contract['defaults']['palette']={'colors':colors,'max_distance':0}
        out.mkdir(parents=True,exist_ok=True)
        for name,data in [('art-bible.json',bible),('audit-contract.json',contract)]:
            (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        text='# '+args.name+' · 美术规范草案\n\n状态：draft。风格配方是整理者建议；未确定字段保留为空，不能称为项目已确认规格。\n\n'
        text+='任务：'+(args.task or '待项目化')+'\n\n'
        for label,p in [('美术风格',art),('UI风格',ui)]:
            if p:text+=f'## {label}：{p["name"]}\n\n'+p.get('summary','')+'\n\n'+''.join('- '+s+'\n' for s in p.get('visual_checks',[]))+'\n'
        text+='## 需要落实的项目参数\n\n'+''.join('- [ ] '+s+'\n' for s in bible['open_decisions'])+'\n'
        text+='[结构化规范](art-bible.json) · [机器检查合同](audit-contract.json)\n\n'
        if not contract['defaults']:text+='机器合同尚未配置检查，直接运行检查器会返回INCOMPLETE；请依据实际资产规范填写，不套用示例尺寸。\n'
        else:text+='已配置机器项：'+', '.join(contract['defaults'])+'。其他项尚未配置；机器结果不等于视觉一致性结论。\n'
        (out/'art-bible.md').write_text(text)
        print(json.dumps({'status':'draft-created','output':str(out),'configured_machine_checks':list(contract['defaults']),'files':names},ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError) as exc:
        ap.exit(2,str(exc)+'\n')
if __name__=='__main__':main()
