#!/usr/bin/env python3
"""Read-only pixel asset contract audit. Requires Pillow; no network or image mutation.
Exit 0: configured machine checks pass (visual review still required).
Exit 1: a configured check or image decoding failed.
Exit 2: missing input, invalid contract, no configured checks, or sampled frames.
"""
from __future__ import annotations
import argparse, collections, fnmatch, hashlib, json, math, os, sys
from pathlib import Path
from typing import Any
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit('Pillow is required: python3 -m pip install Pillow')

EXTENSIONS={'.png','.gif','.webp'}
CHECKS=['canvas_size','size_multiple','grid_scale','alpha_policy','palette','max_colors','margins','bottom_anchor','animation_canvas_consistency']
MANUAL=[
    ('perspective','视角、可见屋顶/墙面比例、脚底投影是否与项目参考一致'),
    ('lighting','主光方向、受光面、投影长度和环境光是否协调'),
    ('material','木材、岩石、金属和布料的明暗与纹理是否有统一尺度'),
    ('silhouette','轮廓节奏、细杆、必要透明孔洞和造型识别性是否保留'),
    ('style','色彩关系、细节密度和角色/场景/UI是否属于同一视觉体系'),
    ('animation','关键姿态、重心、节奏、脚部接触与循环接缝是否自然'),
    ('ui','真实显示尺寸下文字、状态、焦点、图标和输入热区是否可读可操作')
]

def positive_int(v): return type(v) is int and v>0

def pair(v): return isinstance(v,list) and len(v)==2 and all(positive_int(n) for n in v)

def nonnegative(v):return type(v) in (int,float) and not isinstance(v,bool) and math.isfinite(v) and v>=0

def rgba_color(value):
    if not isinstance(value,str) or len(value)!=7 or not value.startswith('#'):raise ValueError('Palette colors must be #RRGGBB strings')
    try:return tuple(int(value[i:i+2],16) for i in (1,3,5))
    except ValueError:raise ValueError('Invalid palette color: '+value)

def validate_rules(rules,label):
    if not isinstance(rules,dict):raise ValueError(label+' must be an object')
    unknown=set(rules)-set(CHECKS)
    if unknown:raise ValueError(label+' has unknown check keys: '+', '.join(sorted(unknown)))
    for k,v in rules.items():
        if v is None:continue # explicit disable in role/file override
        if k in ('canvas_size','size_multiple') and not pair(v):raise ValueError(label+'.'+k+' requires [positive_int, positive_int]')
        if k in ('grid_scale','max_colors') and not positive_int(v):raise ValueError(label+'.'+k+' requires a positive integer')
        if k=='alpha_policy' and v not in ('binary','allow_partial','opaque'):raise ValueError(label+'.alpha_policy must be binary, allow_partial or opaque')
        if k=='animation_canvas_consistency' and type(v) is not bool:raise ValueError(label+'.animation_canvas_consistency requires true or false')
        if k=='palette':
            if not isinstance(v,dict) or set(v)-{'colors','max_distance'}:raise ValueError(label+'.palette requires colors and optional max_distance')
            if not isinstance(v.get('colors'),list) or not v['colors']:raise ValueError(label+'.palette.colors must be nonempty')
            for c in v['colors']:rgba_color(c)
            if not nonnegative(v.get('max_distance',0)):raise ValueError(label+'.palette.max_distance must be nonnegative')
        if k=='margins':
            if not isinstance(v,dict) or set(v)-{'min','max'} or not v:raise ValueError(label+'.margins requires min and/or max')
            for mode,values in v.items():
                if not isinstance(values,list) or len(values)!=4 or not all(type(n) is int and n>=0 for n in values):raise ValueError(label+'.margins.'+mode+' requires [left, top, right, bottom] nonnegative integers')
            if 'min' in v and 'max' in v and any(a>b for a,b in zip(v['min'],v['max'])):raise ValueError(label+'.margins min exceeds max')
        if k=='bottom_anchor':
            if not isinstance(v,dict) or set(v)-{'padding','tolerance'} or 'padding' not in v:raise ValueError(label+'.bottom_anchor requires padding and optional tolerance')
            if not all(type(n) is int and n>=0 for n in v.values()):raise ValueError(label+'.bottom_anchor requires nonnegative integers')

def read_contract(path):
    if path is None:return {'schema_version':1,'defaults':{},'roles':{},'assets':[]}
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data,dict) or data.get('schema_version')!=1:raise ValueError('Contract schema_version must be 1')
    if set(data)-{'schema_version','project','notes','defaults','roles','assets'}:raise ValueError('Unknown top-level contract field')
    validate_rules(data.get('defaults',{}),'defaults')
    if not isinstance(data.get('roles',{}),dict):raise ValueError('roles must be an object')
    for role,rules in data.get('roles',{}).items():validate_rules(rules,'roles.'+role)
    if not isinstance(data.get('assets',[]),list):raise ValueError('assets must be an array')
    for i,item in enumerate(data.get('assets',[])):
        if not isinstance(item,dict) or set(item)-{'pattern','role','rules'} or not isinstance(item.get('pattern'),str) or not item['pattern']:raise ValueError(f'assets[{i}] requires a nonempty pattern, optional role/rules')
        if 'role' in item and item['role'] not in data.get('roles',{}):raise ValueError(f'assets[{i}] references unknown role')
        validate_rules(item.get('rules',{}),f'assets[{i}].rules')
    return data

def effective_rules(contract,relative):
    rules=dict(contract.get('defaults',{}));matches=[];roles=[]
    for entry in contract.get('assets',[]):
        if fnmatch.fnmatchcase(relative,entry['pattern']):
            matches.append(entry['pattern'])
            if entry.get('role'):
                roles.append(entry['role']);rules.update(contract.get('roles',{})[entry['role']])
            rules.update(entry.get('rules',{}))
    return rules,matches,roles

def gather(inputs,out):
    found={};errors=[]
    for raw in inputs:
        path=Path(raw).expanduser().resolve()
        if not path.exists():errors.append('Input does not exist: '+str(path));continue
        source=path if path.is_dir() else path.parent
        candidates=path.rglob('*') if path.is_dir() else [path]
        for p in candidates:
            if not p.is_file() or p.suffix.lower() not in EXTENSIONS or any(s.startswith('._') or s=='__pycache__' for s in p.relative_to(source).parts):continue
            resolved=p.resolve()
            if resolved==out or out in resolved.parents:continue
            found[str(resolved)]=(resolved,p.relative_to(source).as_posix(),str(source))
    return [found[k] for k in sorted(found)],errors

def visible_bounds(im):return im.getchannel('A').getbbox()

def grid_measure(im,scale):
    w,h=im.size
    if w%scale or h%scale:return {'misaligned_dimensions':True,'unequal_blocks':None,'sample_blocks':[]}
    px=im.load();bad=0;samples=[]
    for y in range(0,h,scale):
        for x in range(0,w,scale):
            first=px[x,y]; first=first if first[3] else (0,0,0,0)
            mismatch=False
            for yy in range(y,y+scale):
                for xx in range(x,x+scale):
                    c=px[xx,yy];c=c if c[3] else (0,0,0,0)
                    if c!=first:mismatch=True;break
                if mismatch:break
            if mismatch:
                bad+=1
                if len(samples)<8:samples.append([x,y])
    return {'misaligned_dimensions':False,'unequal_blocks':bad,'sample_blocks':samples}

def result(status,expected,observed,reason,frames=None):
    r={'status':status,'expected':expected,'observed':observed,'reason':reason}
    if frames is not None:r['failing_frames']=frames
    return r

def decode_and_measure(path,rules,max_frames):
    frames=[];thumbnails=[];union_colors=collections.Counter();checks={};durations=[]
    with Image.open(path) as src:
        total=getattr(src,'n_frames',1)
        indices=list(range(total)) if total<=max_frames else sorted({round(i*(total-1)/(max_frames-1)) for i in range(max_frames)})
        preview_indices={indices[0],indices[len(indices)//2],indices[-1]}
        palette=[rgba_color(c) for c in rules.get('palette',{}).get('colors',[])] if rules.get('palette') else []
        tolerance=rules.get('palette',{}).get('max_distance',0) if rules.get('palette') else 0
        for fi in indices:
            src.seek(fi);im=src.convert('RGBA');w,h=im.size
            pixels=list(im.getdata());visible=[p for p in pixels if p[3]>0]
            colors=collections.Counter(p[:3] for p in visible);union_colors.update(colors)
            bounds=visible_bounds(im); margins=[bounds[0],bounds[1],w-bounds[2],h-bounds[3]] if bounds else None
            partial=sum(0<p[3]<255 for p in pixels);transparent=sum(p[3]==0 for p in pixels)
            f={'index':fi,'size':[w,h],'duration_ms':src.info.get('duration',0),'visible_bounds':list(bounds) if bounds else None,'margins_ltrb':margins,'visible_pixels':len(visible),'partial_alpha_pixels':partial,'transparent_pixels':transparent,'rgb_color_count':len(colors)}
            if palette:
                outside=[];worst=0;outside_pixels=0
                for c,n in colors.items():
                    distance=math.sqrt(min(sum((a-b)**2 for a,b in zip(c,p)) for p in palette));worst=max(worst,distance)
                    if distance>tolerance:
                        outside_pixels+=n
                        if len(outside)<12:outside.append({'color':'#%02X%02X%02X'%c,'pixels':n,'distance':round(distance,3)})
                f['palette_distance']={'worst_rgb_distance':round(worst,3),'outside_pixels':outside_pixels,'sample_outside_colors':outside}
            if rules.get('grid_scale') is not None:f['grid']=grid_measure(im,rules['grid_scale'])
            frames.append(f);durations.append(f['duration_ms'])
            if fi in preview_indices:thumbnails.append((fi,im.copy(),bounds))
    for key in CHECKS:
        expected=rules.get(key)
        if expected is None or (key=='animation_canvas_consistency' and expected is False):
            checks[key]=result('NOT_CONFIGURED',None,None,'No applicable contract rule; not counted as a pass.');continue
        bad=[];observed={}
        if key=='canvas_size':
            bad=[f['index'] for f in frames if f['size']!=expected];observed={'frame_sizes':sorted({tuple(f['size']) for f in frames})}
            reason='Decoded logical frame canvas dimensions must match the contract.'
        elif key=='size_multiple':
            bad=[f['index'] for f in frames if any(n%m for n,m in zip(f['size'],expected))];observed={'frame_sizes':sorted({tuple(f['size']) for f in frames})};reason='Canvas dimensions must be divisible by the configured x/y multiples.'
        elif key=='grid_scale':
            bad=[f['index'] for f in frames if f['grid']['misaligned_dimensions'] or f['grid']['unequal_blocks']];observed={'frames':[{'index':f['index'],**f['grid']} for f in frames]};reason='Every origin-aligned NxN output block must repeat one RGBA pixel; fully transparent RGB is ignored. This does not infer artistic pixel quality.'
        elif key=='alpha_policy':
            if expected=='binary':bad=[f['index'] for f in frames if f['partial_alpha_pixels']]
            if expected=='opaque':bad=[f['index'] for f in frames if f['partial_alpha_pixels'] or f['transparent_pixels']]
            observed={'partial_alpha_pixels':sum(f['partial_alpha_pixels'] for f in frames),'transparent_pixels':sum(f['transparent_pixels'] for f in frames)}
            reason='Partial alpha is allowed only according to the contract; this measure does not prove white halos or their absence.'
        elif key=='palette':
            bad=[f['index'] for f in frames if f['palette_distance']['outside_pixels']];observed={'frames':[{'index':f['index'],**f['palette_distance']} for f in frames]};reason='Visible RGB colors are compared to the explicit palette using Euclidean RGB distance, not perceptual color similarity.'
        elif key=='max_colors':
            bad=[f['index'] for f in frames if f['rgb_color_count']>expected];observed={'max_colors_in_one_frame':max(f['rgb_color_count'] for f in frames),'union_rgb_colors':len(union_colors)};reason='Limit applies per decoded frame to visible RGB; union count is reported separately. Hidden RGB and alpha values are not separate colors.'
        elif key=='margins':
            for f in frames:
                m=f['margins_ltrb']
                if m is None or ('min' in expected and any(a<b for a,b in zip(m,expected['min']))) or ('max' in expected and any(a>b for a,b in zip(m,expected['max']))):bad.append(f['index'])
            observed={'frames':[{'index':f['index'],'margins_ltrb':f['margins_ltrb']} for f in frames]};reason='Transparent margins use the bounding box of all alpha>0 pixels. Empty frames have no measurable bounds and fail a configured margin rule.'
        elif key=='bottom_anchor':
            padding=expected['padding'];tolerance=expected.get('tolerance',0)
            bad=[f['index'] for f in frames if f['margins_ltrb'] is None or abs(f['margins_ltrb'][3]-padding)>tolerance]
            observed={'frames':[{'index':f['index'],'bottom_padding':f['margins_ltrb'][3] if f['margins_ltrb'] else None} for f in frames]};reason='Measures the lowest nontransparent pixel against the canvas bottom, not a semantic foot, pivot, or engine ground contact.'
        else:
            sizes={tuple(f['size']) for f in frames};bad=[] if len(sizes)==1 else [f['index'] for f in frames]
            observed={'decoded_frame_sizes':sorted(sizes),'frame_count':total};reason='Checks composited logical frames. GIF/WebP internal delta rectangles are not source sprite frame dimensions; PNG sequences are separate assets.'
        checks[key]=result('FAIL' if bad else 'PASS',expected,observed,reason,bad)
    coverage={'total_frames':total,'measured_frames':len(frames),'measured_indices':indices,'complete':total==len(frames)}
    if not coverage['complete']:checks['frame_coverage']=result('INCOMPLETE',{'all_frames':True},coverage,'Frame limit reached; results apply only to measured frames.')
    statuses=[r['status'] for r in checks.values()]
    status='FAIL' if 'FAIL' in statuses else ('INCOMPLETE' if 'INCOMPLETE' in statuses or not any(s=='PASS' for s in statuses) else 'PASS')
    return {'machine_status':status,'coverage':coverage,'checks':checks,'frames':frames,'union_rgb_colors':len(union_colors),'top_visible_colors':[{'hex':'#%02X%02X%02X'%c,'pixels':n} for c,n in union_colors.most_common(12)]},thumbnails

def font(size):
    for p in ['/System/Library/Fonts/Hiragino Sans GB.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','C:/Windows/Fonts/msyh.ttc','/System/Library/Fonts/Menlo.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/consola.ttf']:
        if Path(p).exists():
            try:return ImageFont.truetype(p,size)
            except OSError:pass
    return ImageFont.load_default()

def fit_text(draw,text,x,y,width,f,fill):
    lines=[];line=''
    for c in text:
        if line and draw.textbbox((0,0),line+c,font=f)[2]>width:lines.append(line);line=''
        line+=c
    if line:lines.append(line)
    for n,line in enumerate(lines[:3]):draw.text((x,y+n*18),line,font=f,fill=fill)

def make_sheets(assets,thumbs,out):
    # Paginate to keep each contact sheet inspectable; no sub-pixel resize is used.
    cells=[]
    for asset in assets:
        for fi,im,bounds in thumbs.get(asset['path'],[]):cells.append((asset,fi,im,bounds))
    names=[]
    for page in range(0,len(cells),24):
        group=cells[page:page+24];cols=min(4,len(group));rows=math.ceil(len(group)/cols)
        cw,ch=300,350;sheet=Image.new('RGB',(cols*cw,rows*ch+45),'#1b2027');d=ImageDraw.Draw(sheet);f=font(13);small=font(12)
        d.text((12,10),'CONTRACT AUDIT | NEAREST NEIGHBOR | VISUAL REVIEW REQUIRED',font=f,fill='white')
        for j,(asset,fi,im,bounds) in enumerate(group):
            x=(j%cols)*cw;y=(j//cols)*ch+45
            d.rectangle((x+7,y+6,x+cw-7,y+ch-7),fill='#303741')
            fit_text(d,asset['relative_path'],x+14,y+13,cw-28,f,'#ffffff')
            d.text((x+14,y+70),f'{im.width}x{im.height} | frame {fi} | {asset["machine_status"]}',font=small,fill='#ffd87a')
            box=(x+14,y+96,x+cw-14,y+ch-52);bw=box[2]-box[0];bh=box[3]-box[1]
            for yy in range(box[1],box[3],12):
                for xx in range(box[0],box[2],12):
                    color='#b9bdc3' if ((xx-box[0])//12+(yy-box[1])//12)%2 else '#e2e3e5'
                    d.rectangle((xx,yy,min(xx+11,box[2]-1),min(yy+11,box[3]-1)),fill=color)
            scale=min(bw//im.width,bh//im.height,8)
            if scale>=1:
                view=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);note=f'zoom {scale}x'
            else:
                # Preserve true pixels: use an explicitly labeled top-left crop, never fractional resampling.
                view=im.crop((0,0,min(bw,im.width),min(bh,im.height)));note='1x CROP; open original for full view'
            sheet.paste(view,(box[0]+(bw-view.width)//2,box[1]+(bh-view.height)//2),view)
            d.text((x+14,y+ch-44),note,font=small,fill='#cbd3dd')
            d.text((x+14,y+ch-26),'bounds: '+str(list(bounds) if bounds else None),font=small,fill='#cbd3dd')
        name='contact-sheet.png' if page==0 else f'contact-sheet-{page//24+1:02}.png'
        sheet.save(out/name);names.append(name)
    return names

def write_reports(report,out):
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 像素素材一致性检查报告','',f'机器检查：**{report["machine_status"]}**。整体：**{report["overall_status"]}**。','',
        '此报告只测量明确配置的规则，不给画风、视角、光源或审美质量自动判通过。源图片未修改。','',f'输入素材 {len(report["assets"])} 个；配置合同：`{report["contract_path"] or "未提供"}`。','']
    if report['errors']:lines+=['## 输入或合同错误','']+['- '+e for e in report['errors']]+['']
    for sheet in report['contact_sheets']:lines+=['![原图联系表，最近邻整数放大，超大图以1x裁片标注]('+sheet+')','']
    for a in report['assets']:
        lines += ['## '+a['relative_path'],'',f'原图：[{a["relative_path"]}](<{os.path.relpath(a["path"],out)}>)；机器状态 **{a["machine_status"]}**。','']
        if a.get('error'):lines += [a['error'],''];continue
        fs=a['frames']
        sizes=sorted({tuple(f['size']) for f in fs})
        colors=[f['rgb_color_count'] for f in fs]
        partial=sum(f['partial_alpha_pixels'] for f in fs)
        lines += ['**原始测量（不含合格判断）：** 画布 '+str(sizes)+'；已测各帧可见RGB颜色数 '+str(min(colors))+'–'+str(max(colors))+'；已测帧的半透明像素合计 '+str(partial)+'。', '首个已测帧可见边界 '+str(fs[0]['visible_bounds'])+'；透明边距（左/上/右/下） '+str(fs[0]['margins_ltrb'])+'。完整逐帧数值见 report.json。', '']
        lines += [f'检查帧 {a["coverage"]["measured_frames"]}/{a["coverage"]["total_frames"]}，SHA-256 `{a["sha256"]}`。','', '| 检查项 | 状态 | 期望值 | 实测值 / 解释 |','|---|---|---|---|']
        for key,r in a['checks'].items():
            obs=json.dumps(r['observed'],ensure_ascii=False,separators=(',',':'))
            if len(obs)>650:obs=obs[:650]+'…（完整逐帧数值见report.json）'
            exp=json.dumps(r['expected'],ensure_ascii=False,separators=(',',':'))
            lines.append('| '+key+' | '+r['status']+' | `'+exp.replace('|','\\|')+'` | '+obs.replace('|','\\|')+'；'+r['reason']+' |')
        lines+=['']
    lines+=['## 必须进行的图像审阅','']
    for m in report['manual_review']:lines.append('- **MANUAL_REVIEW / '+m['id']+'**：'+m['question'])
    lines+=['','人工审阅后另写实际观察、对应文件/位置、严重性和修复建议；不要把此机器报告改写为已完成视觉验收。','']
    (out/'report.md').write_text('\n'.join(lines),encoding='utf-8')

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('inputs',nargs='+',help='Local image files or directories (PNG/GIF/WebP)')
    p.add_argument('--contract',help='JSON audit contract; unspecified rules are NOT_CONFIGURED')
    p.add_argument('--out',required=True,help='Report directory; must not be an input image path')
    p.add_argument('--max-frames',type=int,default=256,help='Maximum measured frames per image; truncation is INCOMPLETE')
    args=p.parse_args(argv);out=Path(args.out).expanduser().resolve()
    if args.max_frames<2:p.error('--max-frames must be at least 2')
    if out.exists() and not out.is_dir():p.error('--out must be a directory')
    out.mkdir(parents=True,exist_ok=True)
    errors=[]
    try:contract=read_contract(args.contract)
    except (OSError,ValueError,TypeError) as ex:
        contract={'schema_version':1,'defaults':{},'roles':{},'assets':[]};errors.append('Contract invalid: '+str(ex))
    files,input_errors=gather(args.inputs,out);errors+=input_errors
    if not files:errors.append('No supported image files found. Empty input is not a passing audit.')
    assets=[];thumbs={}
    if not errors:
        for path,relative,input_root in files:
            rules,matches,roles=effective_rules(contract,relative)
            base={'path':str(path),'relative_path':relative,'input_root':input_root,'roles':roles,'matching_patterns':matches,'rules':rules,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            try:
                measured,images=decode_and_measure(path,rules,args.max_frames);base.update(measured);thumbs[str(path)]=images
            except (OSError,ValueError,EOFError,Image.DecompressionBombError) as ex:
                base.update(machine_status='FAIL',error='Cannot decode/measure image: '+str(ex),checks={})
            assets.append(base)
    statuses=[a['machine_status'] for a in assets]
    status='INCOMPLETE' if errors else ('FAIL' if 'FAIL' in statuses else ('INCOMPLETE' if not statuses or 'INCOMPLETE' in statuses else 'PASS'))
    report={'schema_version':1,'tool':'pixel-game-art-director/audit_assets.py','contract_path':str(Path(args.contract).expanduser().resolve()) if args.contract else None,'machine_status':status,'overall_status':'NEEDS_VISUAL_REVIEW','errors':errors,'assets':assets,'manual_review':[{'id':key,'status':'MANUAL_REVIEW','question':question} for key,question in MANUAL],'contact_sheets':make_sheets(assets,thumbs,out)}
    write_reports(report,out)
    print(json.dumps({'machine_status':status,'overall_status':report['overall_status'],'assets':len(assets),'report':str(out/'report.md'),'json':str(out/'report.json'),'contact_sheets':[str(out/n) for n in report['contact_sheets']],'errors':errors},ensure_ascii=False,indent=2))
    return 1 if status=='FAIL' else (2 if status=='INCOMPLETE' else 0)

if __name__=='__main__':sys.exit(main())
