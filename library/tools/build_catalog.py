#!/usr/bin/env python3
"""Assemble existing verified manifests; no network requests."""
from pathlib import Path
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES={'drawing':'像素绘画与场景','animation':'角色与动作动画','asset-production':'素材制作工作流','game-development':'游戏开发与引擎','ui-design':'游戏UI与界面设计'}

def build():
    entries=[]
    for category in CATEGORIES:
        p=ROOT/'manifests'/f'{category}.json'
        if p.exists():
            payload=json.loads(p.read_text())
            if isinstance(payload,dict): payload=payload.get('tutorials',payload.get('entries',[]))
            entries.extend(payload)
    extra=ROOT/'manifests/supplement.json'
    if extra.exists(): entries.extend(json.loads(extra.read_text()))
    entries.sort(key=lambda x:(list(CATEGORIES).index(x['category']),x['id']))
    if len({e['id'] for e in entries})!=len(entries): raise ValueError('Duplicate tutorial IDs')
    if len({e['source_url'] for e in entries})!=len(entries): raise ValueError('Duplicate canonical source URLs')
    for entry in entries:
        entry['image_count']=len(entry.get('images',[]))
        entry['bytes']=(ROOT/entry['path']).stat().st_size
    (ROOT/'catalog.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'catalog.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in entries))
    catalog='# 教程目录\n\n本目录按独立来源计数；同图的不同分辨率、关键帧、导航页均不额外计数。\n\n'
    catalog+='各条目包含本地原图或图文正文、中文导读、来源和许可。游戏开发条目采用明确版本；绘画与动画为原作者图片教程的中文整理，不声称逐字OCR。\n\n'
    for category,label in CATEGORIES.items():
        group=[e for e in entries if e['category']==category]
        catalog+=f'## {label}（{len(group)}篇）\n\n| ID | 教程 | 难度 | 主题 |\n|---|---|---|---|\n'
        for e in group:
            tags=' / '.join(e.get('tags',[])[:5]).replace('|','/')
            catalog+=f'| {e["id"]} | [{e["title"]}]({e["path"]}) | {e.get("level","—")} | {tags} |\n'
        catalog+='\n'
    (ROOT/'CATALOG.md').write_text(catalog)
    stats=dict(tutorials=len(entries),by_category=dict(Counter(e['category'] for e in entries)),image_references=sum(e['image_count'] for e in entries),unique_image_paths=len({i['path'] for e in entries for i in e.get('images',[])}),markdown_bytes=sum(e['bytes'] for e in entries),source_urls=len({e['source_url'] for e in entries}),licenses=dict(Counter(e['license'] for e in entries)))
    (ROOT/'manifests/collection-stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(stats,ensure_ascii=False))
if __name__=='__main__': build()
