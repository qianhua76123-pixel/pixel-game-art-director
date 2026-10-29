#!/usr/bin/env python3
"""Build a standalone UI research atlas. Public mode links images; local mode can copy an explicit image map."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def build(out, image_map=None, root=ROOT):
    root=Path(root).resolve();out=Path(out).expanduser().resolve()
    if image_map and (out==root or root in out.parents):
        raise ValueError('Local commercial reference images must stay outside the public skill folder.')
    def read(name):return json.loads((root/'references'/name).read_text(encoding='utf-8'))
    cases=read('ui-case-studies.json')['cases']
    axes=read('ui-taxonomy.json')['axes']
    patterns=read('ui-system-patterns.json')['patterns']
    sources=[]
    for name in ['ui-foundation-sources.json','ui-system-sources.json','ui-evaluation-sources.json']:
        sources+=read(name)['sources']
    out.mkdir(parents=True,exist_ok=True)
    mapping=json.loads(Path(image_map).read_text()) if image_map else {}
    for c in cases:
        for im in c['images']:
            im['display_url']=im['url']
            if im['sha256'] in mapping:
                src=Path(mapping[im['sha256']])
                if hashlib.sha256(src.read_bytes()).hexdigest()!=im['sha256']:
                    raise ValueError('Reference image hash mismatch: '+src.name)
                dest=out/'images'/(im['sha256'][:16]+src.suffix.lower())
                dest.parent.mkdir(exist_ok=True);shutil.copyfile(src,dest)
                im['display_url']=dest.relative_to(out).as_posix()
    data={'cases':cases,'axes':axes,'patterns':patterns,'sources':sources,
          'local_review':bool(image_map),'unique_source_count':len({s['url'] for s in sources})}
    template=(root/'assets/ui-atlas.html').read_text(encoding='utf-8')
    payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    html=template.replace('__ATLAS_DATA__',payload)
    (out/'index.html').write_text(html,encoding='utf-8')
    return {'html':str(out/'index.html'),'cases':len(cases),'images':sum(len(c['images']) for c in cases),
            'axes':len(axes),'systems':len(patterns),'unique_method_sources':data['unique_source_count'],
            'local_reference_images':sum(im['display_url']!=im['url'] for c in cases for im in c['images'])}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--image-map')
    a=p.parse_args()
    try:print(json.dumps(build(a.out,a.image_map),ensure_ascii=False,indent=2))
    except (ValueError,OSError,json.JSONDecodeError) as e:p.exit(2,str(e)+'\n')
