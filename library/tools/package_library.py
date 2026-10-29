#!/usr/bin/env python3
"""Package the completed library and verify archive members and CRCs."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
def allowed(p):
 return p.is_file() and not any(x.startswith('._') or x in ['.DS_Store','.venv','__pycache__'] for x in p.relative_to(R).parts)
entries=json.loads((R/'catalog.json').read_text())
validation=json.loads((R/'qa/validation.json').read_text())
if validation['status']!='PASS' or validation['tutorial_count']!=len(entries): raise RuntimeError('Run current validation before packaging')
files=sorted(p for p in R.rglob('*') if allowed(p) and p.name!='MANIFEST.sha256')
(R/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in files))
files.append(R/'MANIFEST.sha256')
archive=R.parent/'pixel-tutorial-library-2026-10-29.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,arcname='pixel-tutorial-library/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(archive) as z:
 bad=z.testzip()
 if bad:raise RuntimeError('Archive CRC error: '+bad)
 names=set(z.namelist())
 for e in entries:
  if 'pixel-tutorial-library/'+e['path'] not in names:raise RuntimeError('Missing tutorial '+e['id'])
  for im in e['images']:
   if 'pixel-tutorial-library/'+im['path'] not in names:raise RuntimeError('Missing image '+im['path'])
 if any('/._' in n for n in names):raise RuntimeError('AppleDouble leaked into archive')
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(digest+'  '+archive.name+'\n')
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'files':len(files),'tutorials':len(entries),'sha256':digest,'verification':'ZIP CRC and all catalog/image members verified'},ensure_ascii=False,indent=2))
