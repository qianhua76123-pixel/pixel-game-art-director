#!/usr/bin/env python3
"""Observable regression fixtures for audit_assets.py. Never uses user artwork."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
from PIL import Image
AUDITOR=Path(__file__).with_name('audit_assets.py')
ROOT=Path(tempfile.mkdtemp(prefix='pixel-skill-audit-test-'))

def save(path,size=(8,8),color=(220,100,40,255),partial=False):
    im=Image.new('RGBA',size,(0,0,0,0))
    for y in range(2,min(6,size[1])):
        for x in range(2,min(6,size[0])):im.putpixel((x,y),color)
    if partial:im.putpixel((3,3),(220,100,40,120))
    im.save(path)

def run(name,inputs,contract=None,*flags):
    out=ROOT/name
    cmd=[sys.executable,str(AUDITOR),*[str(x) for x in inputs],'--out',str(out),*flags]
    if contract is not None:
        cp=ROOT/(name+'-contract.json');cp.write_text(json.dumps(contract));cmd+=['--contract',str(cp)]
    proc=subprocess.run(cmd,capture_output=True,text=True)
    if not (out/'report.json').exists():raise AssertionError(proc.stderr or proc.stdout)
    return proc.returncode,json.loads((out/'report.json').read_text()),out

inputs=ROOT/'inputs';inputs.mkdir(exist_ok=True)
good=inputs/'good.png';save(good)
bad_size=inputs/'bad-size.png';save(bad_size,(10,8))
bad_palette=inputs/'bad-palette.png';save(bad_palette,color=(0,255,255,255))
bad_alpha=inputs/'bad-alpha.png';save(bad_alpha,partial=True)
bad_grid=inputs/'bad-grid.png';save(bad_grid)
im=Image.open(bad_grid);im.putpixel((3,2),(0,0,0,0));im.save(bad_grid)
alt=inputs/'large-tree.png';save(alt,(12,12))
contract={'schema_version':1,'defaults':{'canvas_size':[8,8],'size_multiple':[2,2],'grid_scale':2,'alpha_policy':'binary','palette':{'colors':['#DC6428'],'max_distance':0},'max_colors':1,'margins':{'min':[2,2,2,2],'max':[2,2,2,2]},'bottom_anchor':{'padding':2,'tolerance':0},'animation_canvas_consistency':True}}
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.glob('*.png')}
results=[]
rc,r,out=run('good',[good],contract);assert rc==0 and r['machine_status']=='PASS';assert r['overall_status']=='NEEDS_VISUAL_REVIEW';assert (out/'contact-sheet.png').is_file();results.append(['valid fixture',rc,r['machine_status']])
for name,path,check in [('wrong-canvas',bad_size,'canvas_size'),('outside-palette',bad_palette,'palette'),('partial-alpha',bad_alpha,'alpha_policy'),('broken-grid',bad_grid,'grid_scale')]:
    rc,r,_=run(name,[path],contract);assert rc==1 and r['assets'][0]['checks'][check]['status']=='FAIL';results.append([name,rc,r['machine_status']])
rc,r,_=run('not-configured',[good]);assert rc==2 and r['machine_status']=='INCOMPLETE';assert all(x['status']=='NOT_CONFIGURED' for x in r['assets'][0]['checks'].values());results.append(['no contract',rc,r['machine_status']])
empty=ROOT/'empty';empty.mkdir(exist_ok=True)
rc,r,_=run('empty-input',[empty],contract);assert rc==2 and len(r['assets'])==0;results.append(['empty input',rc,r['machine_status']])
rc,r,_=run('invalid-contract',[good],{'schema_version':1,'defaults':{'max_colour':2}});assert rc==2 and r['errors'];results.append(['unknown contract key',rc,r['machine_status']])
# A distinct role can override canvas/margins/anchor without weakening all character checks.
role_contract=json.loads(json.dumps(contract));role_contract.update(roles={'tree':{'canvas_size':[12,12],'margins':None,'bottom_anchor':None}},assets=[{'pattern':'large-tree.png','role':'tree'}])
rc,r,_=run('role-overrides',[good,alt],role_contract);assert rc==0;assert r['assets'][1]['checks']['margins']['status']=='NOT_CONFIGURED';results.append(['per-role canvas override',rc,r['machine_status']])
# A three-frame GIF has stable canvases but the visible bottom moves: anchor, not canvas, must fail.
frames=[]
for dy in [0,1,0]:
    im=Image.new('RGBA',(8,8),(0,0,0,0))
    for y in range(2+dy,6+dy):
        for x in range(2,6):im.putpixel((x,y),(220,100,40,255))
    frames.append(im)
gif=inputs/'moving-anchor.gif';frames[0].save(gif,save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=2)
anim_contract={'schema_version':1,'defaults':{'canvas_size':[8,8],'bottom_anchor':{'padding':2,'tolerance':0},'animation_canvas_consistency':True}}
rc,r,_=run('moving-anchor',[gif],anim_contract);assert rc==1;checks=r['assets'][0]['checks'];assert checks['bottom_anchor']['status']=='FAIL' and checks['animation_canvas_consistency']['status']=='PASS';results.append(['animation anchor drift',rc,r['machine_status']])
rc,r,_=run('sampled-animation',[gif],{'schema_version':1,'defaults':{'canvas_size':[8,8]}},'--max-frames','2');assert rc==2 and not r['assets'][0]['coverage']['complete'];results.append(['sampled animation incomplete',rc,r['machine_status']])
# One report containing mixed fixtures makes the visual output easy to inspect.
rc,r,out=run('mixed-demo',[good,bad_size,bad_palette,bad_alpha,bad_grid],contract);assert rc==1;results.append(['mixed visual report',rc,r['machine_status']])
after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.glob('*.png')};assert before==after
report={'status':'PASS','checks':results,'input_png_hashes_unchanged':True,'demo_report':str(out/'report.md'),'demo_contact_sheet':str(out/'contact-sheet.png')}
(ROOT/'test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
