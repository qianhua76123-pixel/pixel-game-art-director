#!/usr/bin/env python3
"""Build paragraph/code-block-aware JSONL retrieval chunks, no network needed."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
TARGET=2200

def split_blocks(body):
    lines=body.splitlines(keepends=True);blocks=[];current=[];fence=None
    for line in lines:
        marker=re.match(r'^\s*(`{3,}|~{3,})',line)
        if marker:
            if fence is None: fence=marker.group(1)[0]
            elif marker.group(1)[0]==fence: fence=None
        current.append(line)
        if not fence and not line.strip():
            blocks.append(''.join(current));current=[]
    if current:blocks.append(''.join(current))
    return blocks

def main():
    entries=json.loads((ROOT/'catalog.json').read_text());rows=[]
    for e in entries:
        doc=(ROOT/e['path']).read_text()
        if doc.startswith('---\n'):doc=doc.split('---\n',2)[2].lstrip()
        pieces=[];current='';heading=e['title'];chunk_heading=heading
        for block in split_blocks(doc):
            match=re.match(r'^(#{1,6})\s+(.+)',block)
            if match: heading=match.group(2).strip()
            if current and len(current)+len(block)>TARGET:
                pieces.append((chunk_heading,current));current=''
            if not current:chunk_heading=heading
            current+=block
        if current: pieces.append((chunk_heading,current))
        for i,(heading,body) in enumerate(pieces,1):
            rows.append(dict(chunk_id=f'{e["id"]}-{i:03}',tutorial_id=e['id'],title=e['title'],heading=heading,category=e['category'],document_path=e['path'],relative_link_base=str(Path(e['path']).parent),source_url=e['source_url'],author=e['author'],license=e['license'],version=e['version'],retrieved_at=e['retrieved_at'],text=body.strip()))
    (ROOT/'chunks.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    report={'chunks':len(rows),'tutorials':len(entries),'target_characters':TARGET,'max_chunk_characters':max((len(x['text']) for x in rows),default=0),'note':'Long code blocks/tables remain intact and can exceed target length.'}
    (ROOT/'qa/chunk-stats.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
