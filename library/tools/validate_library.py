#!/usr/bin/env python3
"""Validate catalog, metadata, local links, image decoding and source fingerprints."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote,urlparse
import hashlib,json,re,sys
import yaml
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[];warnings=[];counts=Counter();decoded=set();checked_links=set()
    items=json.loads((ROOT/'catalog.json').read_text())
    required=['id','title','category','path','source_url','author','license','license_url','retrieved_at','level','tags','summary','images','content_mode','version']
    for e in items:
        tid=e.get('id','unknown')
        for key in required:
            if key not in e or e[key] in ['',None]: errors.append(f'{tid}: missing manifest field {key}')
        path=ROOT/e['path']
        if not path.is_file(): errors.append(f'{tid}: missing Markdown {path}');continue
        body=path.read_text()
        if not body.startswith('---\n'): errors.append(f'{tid}: missing YAML frontmatter')
        else:
            try:
                fm=yaml.safe_load(body.split('---\n',2)[1])
                if fm.get('id')!=tid: errors.append(f'{tid}: frontmatter id mismatch')
            except Exception as ex: errors.append(f'{tid}: invalid frontmatter {ex}')
        if len(body)<1000: warnings.append(f'{tid}: short document {len(body)} characters')
        if not e.get('images'): errors.append(f'{tid}: no registered local image')
        if e['source_url'] not in body: errors.append(f'{tid}: source URL missing from document')
        # Markdown and optional HTML media links. Exclude fenced code before checking.
        links_text=re.sub(r'```.*?```','',body,flags=re.S)
        urls=re.findall(r'!?\[[^\]]*\]\(([^\s]+?)(?:\s+"[^"]*")?\)',links_text)
        urls+=re.findall(r'<(?:img|source)[^>]+src=["\']([^"\']+)',links_text)
        for url in urls:
            url=url.strip('<>'); parsed=urlparse(url)
            if parsed.scheme or url.startswith('#') or url.startswith('//'): continue
            clean=unquote(parsed.path)
            if not clean: continue
            target=(path.parent/clean).resolve();checked_links.add(str(target))
            if not target.exists(): errors.append(f'{tid}: broken local link {url}')
        for img in e.get('images',[]):
            p=ROOT/img['path']
            if not p.is_file(): errors.append(f'{tid}: missing image {img["path"]}');continue
            if p.suffix.lower()=='.svg':
                if '<svg' not in p.read_text(errors='replace'): errors.append(f'{tid}: invalid SVG {p.name}')
            elif str(p) not in decoded:
                try:
                    with Image.open(p) as im:
                        w,h=im.size;im.verify()
                        if min(w,h)<2: warnings.append(f'{tid}: tiny image {p.name} {w}x{h}')
                except Exception as ex: errors.append(f'{tid}: image decode failed {p.name}: {ex}')
            decoded.add(str(p))
            expected=img.get('sha256')
            if expected and hashlib.sha256(p.read_bytes()).hexdigest()!=expected: errors.append(f'{tid}: image hash mismatch {p.name}')
        counts[e['category']]+=1
    # Include hand-authored entry points in the local-link check as well.
    for path in ROOT.glob('*.md'):
        if path.name.startswith('._'): continue
        body=path.read_text();body=re.sub(r'```.*?```','',body,flags=re.S)
        for url in re.findall(r'!?\[[^\]]*\]\(([^\s]+?)(?:\s+"[^"]*")?\)',body):
            url=url.strip('<>');parsed=urlparse(url)
            if parsed.scheme or url.startswith('#') or url.startswith('//'): continue
            clean=unquote(parsed.path)
            if clean and not (path.parent/clean).exists(): errors.append(f'{path.name}: broken local link {url}')
    report=dict(status='PASS' if not errors else 'FAIL',retrieved_at='2026-10-29',tutorial_count=len(items),unique_source_count=len({x['source_url'] for x in items}),by_category=dict(counts),decoded_image_files=len(decoded),checked_local_targets=len(checked_links),errors=errors,warnings=warnings,limitations=['Local structural checks do not execute Godot or Krita projects.','Remote site availability is recorded at collection time, not guaranteed in future.','Image interpretation is a manual reading, not a claim of exhaustive OCR.'])
    q=ROOT/'qa';q.mkdir(exist_ok=True)
    (q/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    text='# 教程库验证报告\n\n'+f'状态：**{report["status"]}**。教程 {len(items)} 篇；独立来源 {report["unique_source_count"]}；可解码图像 {len(decoded)} 个；检查本地链接目标 {len(checked_links)} 个。\n\n'
    text+='## 错误\n\n'+('\n'.join('- '+x for x in errors) if errors else '无。')+'\n\n'
    text+='## 提醒\n\n'+('\n'.join('- '+x for x in warnings) if warnings else '无。')+'\n\n'
    text+='## 验证范围\n\n检查了清单字段、YAML、Markdown来源链接、本地引用、图片可解码性和已记录SHA-256。未将这些教程中的游戏或绘画工程逐一运行；教程示例不等于本地已执行结果。原文文档按获取时的页面转存，外部参考链接仍需联网。\n'
    (q/'VALIDATION.md').write_text(text)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not errors else 1
if __name__=='__main__':sys.exit(main())
