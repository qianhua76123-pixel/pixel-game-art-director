#!/usr/bin/env python3
"""Validate downloaded tutorial links, media hashes and retained code blocks."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import hashlib
import io
import json
import re
from bs4 import BeautifulSoup
from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'manifests/game-development.json').read_text())
failures = []
rows = []
for item in records:
    path = ROOT / item['path']
    text = path.read_text()
    frontmatter = yaml.safe_load(text.split('---', 2)[1])
    local_errors = []
    if frontmatter['id'] != item['id']:
        local_errors.append('Frontmatter ID mismatch')
    if hashlib.sha256(text.encode()).hexdigest() != item['markdown_sha256']:
        local_errors.append('Markdown hash mismatch')
    for destination in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
        if destination.startswith(('http:', 'https:', '#', 'mailto:')):
            continue
        target = (path.parent / unquote(destination.split('#')[0])).resolve()
        if not target.exists():
            local_errors.append('Missing local link: ' + destination)
    for media in item['images']:
        content = (ROOT / media['path']).read_bytes()
        if hashlib.sha256(content).hexdigest() != media['sha256']:
            local_errors.append('Media hash mismatch: ' + media['path'])
        try:
            with Image.open(io.BytesIO(content)) as im:
                im.verify()
        except Exception as exc:
            local_errors.append('Invalid image: ' + str(exc))
    for media in item['embedded_videos']:
        if media['status'] != 'downloaded-with-extracted-stills':
            local_errors.append('Video not archived with keyframes: ' + media['source_url'])
        elif hashlib.sha256((ROOT / media['path']).read_bytes()).hexdigest() != media['sha256']:
            local_errors.append('Video hash mismatch: ' + media['path'])
    source = BeautifulSoup((ROOT / item['source_snapshot']).read_text(), 'html.parser')
    code_blocks = source.find_all('pre')
    missed_code = [p.get_text().strip()[:60] for p in code_blocks if p.get_text().strip() not in text]
    if missed_code:
        local_errors.append('Original code blocks missing or altered: ' + repr(missed_code))
    if 'User-contributed notes' in text or 'Built with Sphinx' in text:
        local_errors.append('Navigation/comment boilerplate remains')
    if re.search(r'!\[[^\]]*\]\(https?://', text):
        local_errors.append('Remote image embed remains')
    for heading in ['中文操作路线','动手练习','验收清单','来源、配图与授权']:
        if heading not in text:
            local_errors.append('Missing guide section: ' + heading)
    rows.append({'id':item['id'],'images':len(item['images']),'source_code_blocks':len(code_blocks),'markdown_bytes':len(text.encode()),'failures':local_errors})
    failures.extend(item['id'] + ': ' + e for e in local_errors)
if len(records) != 24 or len({r['source_url'] for r in records}) != 24:
    failures.append('Expected exactly 24 unique source tutorial pages')
result = {'validated_at':'2026-10-29','tutorials':len(records),'unique_source_pages':len({r['source_url'] for r in records}),'local_images':sum(len(r['images']) for r in records),'original_videos':sum(len(r['embedded_videos']) for r in records),'extracted_video_stills':sum(1 for r in records for im in r['images'] if 'timestamp_seconds' in im),'source_code_blocks':sum(r['source_code_blocks'] for r in rows),'failures':failures,'checks':['YAML metadata','relative file links','local image embeds','image decode and SHA-256','original video SHA-256','original code block preservation','boilerplate removal','distinct source URLs'],'visual_review':'Representative images from all 24 tutorials viewed in two contact sheets; source screenshots, sprite GIFs, diagrams and video stills confirmed. This is document QA, not execution of all Godot exercises.','items':rows}
out=ROOT/'reports/game-development-validation.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='items'},ensure_ascii=False,indent=2))
raise SystemExit(bool(failures))
