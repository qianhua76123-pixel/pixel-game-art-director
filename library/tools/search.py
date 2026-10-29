#!/usr/bin/env python3
"""Offline ranked metadata/fulltext search for agents. Python standard library only."""
from pathlib import Path
import argparse, json, re
ROOT=Path(__file__).resolve().parents[1]
ALIASES={'俯视':['top-down','top down','topdown'],'地图':['tilemap','tileset','tiles','terrain'],'动画':['animation','cycle','timeline'],'像素':['pixel'],'行走':['walk'],'跑步':['run'],'光影':['shading','light','shadow'],'房屋':['houses','house','indoors'],'树木':['vegetation','trees','tree'],'调色':['palette','color'],'导出':['export','sprite sheet'],'保存':['saving','save'],'缩放':['scale','scaling','resizing','resolution'],'碰撞':['collision','physics'],'透明':['alpha','transparency']}
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('query',nargs='?',default='')
p.add_argument('--category',choices=['drawing','animation','asset-production','game-development','ui-design'])
p.add_argument('--top',type=int,default=10)
p.add_argument('--fulltext',action='store_true',help='Also rank matches inside tutorial Markdown')
p.add_argument('--json',action='store_true',help='Emit compact JSON for agents')
a=p.parse_args()
entries=json.loads((ROOT/'catalog.json').read_text())
terms=[x.lower() for x in re.split(r'\s+',a.query.strip()) if x]
groups=[]
for term in terms:
 group=[term]
 for key,aliases in ALIASES.items():
  if key in term: group.extend(aliases)
 groups.append(group)
rows=[]
for e in entries:
 if a.category and e['category']!=a.category: continue
 title=(e['title']+' '+e['id']).lower()
 meta=' '.join([e.get('summary',''),' '.join(e.get('tags',[])),' '.join(e.get('learning_objectives',[])),e.get('category','')]).lower()
 body=(ROOT/e['path']).read_text().lower() if a.fulltext else ''
 score=0;matched=[]
 for term,group in zip(terms,groups):
  weight=max((10*(t in title)+4*(t in meta)+min(body.count(t),3) for t in group),default=0)
  score+=weight
  if weight: matched.append(term)
 if groups and not matched: continue
 score+=5*len(matched)
 rows.append({'id':e['id'],'title':e['title'],'category':e['category'],'score':score,'matched_terms':matched,'path':e['path'],'absolute_path':str(ROOT/e['path']),'summary':e.get('summary',''),'source_url':e['source_url']})
rows.sort(key=lambda x:(-x['score'],x['id']))
rows=rows[:a.top]
if a.json: print(json.dumps(rows,ensure_ascii=False,indent=2))
else:
 for e in rows:
  print(f'{e["id"]} | {e["title"]} | score={e["score"]}\n  {e["path"]}\n  {e["summary"]}')
 if not rows: print('No match. Try shorter terms, spaces between concepts, or --fulltext.')
