#!/usr/bin/env python3
"""Validate the collected local files and build a visual-review contact sheet."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import hashlib,json,re,io
from PIL import Image, ImageDraw, ImageFont
import yaml
R=Path(__file__).resolve().parents[1]
records=json.loads((R/'manifests/asset-production.json').read_text())
errors=[];checks=[];previews=[]
for rec in records:
 p=R/rec['path'];text=p.read_text();meta=yaml.safe_load(text.split('---',2)[1])
 if meta['id']!=rec['id']:errors.append('id mismatch '+rec['id'])
 if len(rec['author'])==0:errors.append('missing author '+rec['id'])
 if not rec['images']:errors.append('no images '+rec['id'])
 for im in rec['images']:
  ip=R/im['path'];dat=ip.read_bytes()
  if hashlib.sha256(dat).hexdigest()!=im['sha256']:errors.append('image hash '+im['path'])
  if ip.suffix!='.svg':
   with Image.open(io.BytesIO(dat)) as obj:obj.verify()
 for local in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
  if urlparse(local).scheme:errors.append('remote image '+local)
  elif not (p.parent/unquote(local)).exists():errors.append('missing image '+local)
 for href in re.findall(r'\]\(([^)]+)\)',text):
  if href.startswith('#') and f'id="{href[1:]}"' not in text:errors.append('anchor '+rec['id']+' '+href)
  if not urlparse(href).scheme and not href.startswith('#') and not (p.parent/unquote(href.split('#')[0])).exists():errors.append('broken local link '+rec['id']+' '+href)
 original=(R/rec['source_rst_path']).read_text()
 if 'free documentation license' not in original.lower():errors.append('license '+rec['id'])
 choices=[x for x in rec['images'] if not x['path'].endswith('.svg')]
 if rec['id']=='MAKE-001':choice=next(x for x in choices if 'Kiki-pixel' in x['path'])
 else:choice=choices[0]
 with Image.open(R/choice['path']) as im:
  im=im.convert('RGBA');im.thumbnail((380,240));previews.append((rec['id'],choice['path'],im.copy()))
 checks.append({'id':rec['id'],'md_bytes':p.stat().st_size,'source_characters':len(original),'local_images':len(rec['images'])})
canvas=Image.new('RGB',(1600,300*((len(previews)+3)//4)),(238,241,244));d=ImageDraw.Draw(canvas)
for i,(ident,path,im) in enumerate(previews):
 x=(i%4)*400;y=(i//4)*300;d.text((x+10,y+8),ident,fill=(15,20,30));d.text((x+10,y+25),Path(path).name[:48],fill=(40,40,40))
 canvas.paste(im,(x+10,y+50),im)
log=R/'logs/asset-production';log.mkdir(parents=True,exist_ok=True);canvas.save(log/'contact-sheet.png')
report={'tutorials':len(records),'unique_source_urls':len({r['source_url'] for r in records}),'images':sum(len(x['images']) for x in records),'unique_image_hashes':len({i['sha256'] for r in records for i in r['images']}),'image_bytes':sum(i['bytes'] for r in records for i in r['images']),'errors':errors,'files':checks,'visual_review':'contact sheet generated; viewing must be recorded separately'}
(log/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
