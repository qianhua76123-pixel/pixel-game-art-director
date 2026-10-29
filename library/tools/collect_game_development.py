#!/usr/bin/env python3
"""Collect 24 selected CC BY 3.0 Godot 4.5 tutorials, with local images.

Requires requests, beautifulsoup4, markdownify, pillow, pyyaml.
The guide data lives in game_development_guides.json; reruns reuse image files.
No whole-site crawling, authentication, payment, or media generation is used.
"""
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
import os
import re
import subprocess
import time
import warnings
import requests
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify
from PIL import Image

warnings.filterwarnings('ignore', category=Warning, module='urllib3')
ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://docs.godotengine.org/en/4.5/'
DATE = '2026-10-29'
AUTHOR = 'Juan Linietsky, Ariel Manzur and the Godot community'
LICENSE = 'CC-BY-3.0'
LICENSE_URL = 'https://creativecommons.org/licenses/by/3.0/'
LICENSE_EVIDENCE = 'https://github.com/godotengine/godot-docs/blob/4.5/README.md#license'
CACHE = Path(os.environ.get('PIXEL_GODOT_HTML_CACHE', '/tmp/pixel-godot-html'))
GUIDES = json.loads((ROOT / 'tools/game_development_guides.json').read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url):
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=(15, 60), headers={'User-Agent': 'PixelTutorialLibrary/1.0 (local educational archive; bounded requests)'})
            response.raise_for_status()
            if len(response.content) > 24 * 1024 * 1024:
                raise ValueError('Resource exceeds 24 MiB size guard: ' + url)
            return response
        except (requests.RequestException, ValueError):
            if attempt == 2:
                raise
            time.sleep(1.0 + attempt)


def code_language(el):
    for parent in [el] + list(el.parents)[:4]:
        for cls in parent.get('class', []):
            if cls.startswith('highlight-'):
                language = cls[len('highlight-'):]
                return {'csharp': 'csharp', 'gdscript': 'gdscript', 'text': 'text'}.get(language, language)
    return ''


def clean_inline(text):
    return re.sub(r'\s+', ' ', text).strip().replace('|', '\\|')


def collect(guide):
    ident = guide['id']
    url = BASE + guide['source_path']
    md_path = ROOT / 'tutorials/game-development' / (ident + '-' + guide['slug'] + '.md')
    asset_dir = ROOT / 'assets/game-development' / ident
    snapshot_path = ROOT / 'sources/game-development' / (ident + '.article.html')
    for directory in [md_path.parent, asset_dir, snapshot_path.parent]:
        directory.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / guide['source_path'].replace('/', '__')
    if snapshot_path.exists():
        source_html = snapshot_path.read_text()
    elif cache_path.exists():
        source_html = cache_path.read_text()
    else:
        response = fetch(url)
        source_soup = BeautifulSoup(response.content, 'html.parser')
        main = source_soup.select_one('[itemprop=articleBody]')
        if main is None:
            raise ValueError('No article content: ' + url)
        source_html = str(main)
    snapshot_path.write_text(source_html)
    soup = BeautifulSoup(source_html, 'html.parser')
    article = soup.select_one('[itemprop=articleBody]') or soup
    original_title = article.h1.get_text(' ', strip=True).replace('', '').strip()
    for item in article.select('.headerlink, .rst-footer-buttons, .admonition-grid, script, style, footer, .sphinx-tabs-tab'):
        item.decompose()
    for heading in article.find_all(['h2', 'h3']):
        if heading.get_text(' ', strip=True).strip() == 'User-contributed notes':
            node = heading.find_parent('section')
            if node:
                node.decompose()
            else:
                for sibling in list(heading.next_siblings):
                    sibling.extract()
                heading.decompose()
    image_records = []
    image_by_url = {}
    image_replacements = {}
    errors = []
    image_elements = list(article.find_all('img'))
    for element in image_elements:
        src = element.get('src') or element.get('data-src')
        if not src:
            continue
        remote = urljoin(url, src)
        basename = unquote(Path(urlparse(remote).path).name)
        alt = element.get('alt', '').strip()
        if basename in ('good.png', 'bad.png', 'regular.png') and alt in ('good', 'bad', 'regular'):
            element.replace_with('[' + alt + ']')
            continue
        if remote not in image_by_url:
            name = re.sub(r'[^a-zA-Z0-9._-]+', '-', basename)
            if not name:
                name = sha(remote.encode())[:12] + '.img'
            target = asset_dir / name
            try:
                if not target.exists():
                    target.write_bytes(fetch(remote).content)
                raw = target.read_bytes()
                with Image.open(io.BytesIO(raw)) as im:
                    im.verify()
                with Image.open(io.BytesIO(raw)) as im:
                    width, height = im.size
                    frames = getattr(im, 'n_frames', 1)
                header = element.find_previous(['h2', 'h3', 'h4'])
                section = header.get_text(' ', strip=True).replace('', '').strip() if header else original_title
                useful_alt = alt if alt and not alt.startswith('../') and not alt.endswith(('.webp', '.png', '.jpg', '.gif')) else basename
                caption = '原教程图示：' + section + ' — ' + useful_alt
                record = {'path': str(target.relative_to(ROOT)), 'source_url': remote, 'caption': caption, 'sha256': sha(raw), 'width': width, 'height': height, 'frames': frames, 'author': AUTHOR, 'license': LICENSE, 'license_url': LICENSE_URL}
                image_records.append(record)
                image_by_url[remote] = record
            except Exception as exc:
                errors.append({'url': remote, 'error': str(exc)})
                raise RuntimeError('Failed image in ' + ident + ': ' + remote) from exc
        record = image_by_url[remote]
        relative = os.path.relpath(ROOT / record['path'], md_path.parent)
        image_replacements[remote] = relative
        element['src'] = relative
        element['alt'] = record['caption']
        for attr in ('srcset', 'loading', 'width', 'height', 'class'):
            if attr in element.attrs:
                del element[attr]
    video_records = []
    for video in list(article.find_all('video')):
        sources = [s.get('src') for s in video.find_all('source') if s.get('src')]
        if video.get('src'):
            sources.insert(0, video['src'])
        if not sources:
            video.decompose()
            continue
        remote = urljoin(url, sources[0])
        label = video.get_text(' ', strip=True) or '原教程动态演示'
        container = soup.new_tag('div')
        paragraph = soup.new_tag('p')
        link = soup.new_tag('a', href=remote)
        paragraph.append(link)
        container.append(paragraph)
        video_record = {'source_url': remote, 'label': label, 'status': 'linked-not-transcribed'}
        try:
            import imageio_ffmpeg
            movie = asset_dir / Path(urlparse(remote).path).name
            if not movie.exists():
                movie.write_bytes(fetch(remote).content)
            video_record.update({'path': str(movie.relative_to(ROOT)), 'sha256': sha(movie.read_bytes()), 'status': 'downloaded-with-extracted-stills', 'keyframes': []})
            image_replacements[remote] = os.path.relpath(movie, md_path.parent)
            executable = imageio_ffmpeg.get_ffmpeg_exe()
            probe = subprocess.run([executable, '-hide_banner', '-i', str(movie)], capture_output=True, text=True, timeout=20)
            match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe.stderr)
            if not match:
                raise ValueError('Cannot detect media duration')
            duration = float(match[1]) * 3600 + float(match[2]) * 60 + float(match[3])
            for position, fraction in enumerate((0.1, 0.5, 0.9), 1):
                stamp = round(duration * fraction, 3)
                target = asset_dir / (movie.stem + '-keyframe-' + str(position) + '.png')
                if not target.exists():
                    subprocess.run([executable, '-hide_banner', '-loglevel', 'error', '-ss', str(stamp), '-i', str(movie), '-frames:v', '1', '-y', str(target)], check=True, capture_output=True, timeout=30)
                raw = target.read_bytes()
                with Image.open(io.BytesIO(raw)) as im:
                    width, height = im.size
                    im.verify()
                caption = label + '：原视频抽帧 ' + str(stamp) + ' 秒（静态观察，不是视频转录）'
                record = {'path': str(target.relative_to(ROOT)), 'source_url': remote, 'caption': caption, 'sha256': sha(raw), 'width': width, 'height': height, 'frames': 1, 'author': AUTHOR, 'license': LICENSE, 'license_url': LICENSE_URL, 'derived_from': str(movie.relative_to(ROOT)), 'transformation': 'ffmpeg single-frame extraction', 'timestamp_seconds': stamp}
                image_records.append(record)
                video_record['keyframes'].append(record['path'])
                frame = soup.new_tag('img', src=os.path.relpath(target, md_path.parent), alt=caption)
                frame_paragraph = soup.new_tag('p')
                frame_paragraph.append(frame)
                container.append(frame_paragraph)
            link.string = label + '（本地原视频；下方为10%、50%、90%位置静态抽帧，未转录视频内容）'
        except Exception as exc:
            link.string = label + '（原文动态演示，在线链接；未逐帧转录）'
            video_record['status'] = 'linked-not-transcribed'
            video_record['extraction_error'] = str(exc)
        video.replace_with(container)
        video_records.append(video_record)
    for anchor in article.find_all('a', href=True):
        absolute = urljoin(url, anchor['href'])
        anchor['href'] = image_replacements.get(absolute, absolute)
    for h in article.find_all(re.compile('^h[1-6]$')):
        h.name = 'h' + str(min(int(h.name[1]) + 2, 6))
    body = markdownify(str(article), heading_style='ATX', bullets='-', code_language_callback=code_language, escape_underscores=False, strip=['button'])
    body = re.sub(r'\n{4,}', '\n\n\n', body).strip()
    if not image_records:
        raise ValueError('Expected illustrated source but found no image: ' + ident)
    metadata = {'id': ident, 'title': guide['title'], 'category': 'game-development', 'path': str(md_path.relative_to(ROOT)), 'source_url': url, 'source_title': original_title, 'author': AUTHOR, 'license': LICENSE, 'license_url': LICENSE_URL, 'license_evidence_url': LICENSE_EVIDENCE, 'retrieved_at': DATE, 'language': 'zh-CN+en', 'source_language': 'en', 'level': guide['level'], 'tags': guide['tags'], 'summary': guide['summary'], 'images': image_records, 'content_mode': 'licensed-fulltext-with-chinese-guide', 'version': 'Godot 4.5 documentation branch', 'prerequisites': guide['prerequisites'], 'learning_objectives': guide['steps'], 'source_snapshot': str(snapshot_path.relative_to(ROOT)), 'source_snapshot_sha256': sha(source_html.encode()), 'embedded_videos': video_records, 'image_download_errors': errors}
    front = {k: metadata[k] for k in ('id','title','category','source_url','source_title','author','license','license_url','retrieved_at','language','source_language','level','tags','content_mode','version','prerequisites')}
    text = '---\n' + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + '---\n\n'
    text += '# ' + guide['title'] + '\n\n'
    text += '> 本文由 Godot 官方 4.5 版文档转换。下方中文导读、练习和验收是整理者的教学编排，英文正文是原教程主内容；不是官方中文逐句译文，也未声称已在引擎中执行全部练习。\n\n'
    text += '## 适用任务\n\n' + guide['summary'] + '\n\n'
    text += '## 前提\n\n' + '\n'.join('- ' + p for p in guide['prerequisites']) + '\n\n'
    text += '## 中文操作路线\n\n' + '\n'.join(str(i+1) + '. ' + s for i,s in enumerate(guide['steps'])) + '\n\n'
    text += '## 图示怎么读\n\n先沿英文正文的步骤阅读对应截图；截图来自同一版本页面，局部操作顺序以紧邻图片的文字为准。图片下载到本地，可离线打开并放大检查。截图中的示例美术用于说明引擎操作，不代表本库要求采用该画风。\n\n'
    text += '## 动手练习\n\n' + guide['exercise'] + '\n\n'
    text += '## 验收清单\n\n' + '\n'.join('- [ ] ' + s for s in guide['checks']) + '\n\n'
    text += '## 版本与边界\n\n' + guide['caution'] + '\n\n本次来源固定为 Godot 4.5 文档分支，抓取日期为 2026-10-29；它不是“当前最新版本”的声明。升级引擎时应重新核对节点名、属性名和 API。\n\n'
    text += '## 原教程正文（英文，Markdown 转换）\n\n' + body + '\n\n'
    text += '## 来源、配图与授权\n\n'
    text += '- 原文：[' + original_title + '](' + url + ')。\n'
    text += '- 作者与署名：' + AUTHOR + '。\n'
    text += '- 文档许可：[CC BY 3.0](' + LICENSE_URL + ')；[官方仓库许可声明](' + LICENSE_EVIDENCE + ')。\n'
    text += '- 许可全文：[godot-docs-4.5-LICENSE.txt](../../licenses/godot-docs-4.5-LICENSE.txt)。\n'
    text += '- 本地原文主内容快照：[' + ident + '.article.html](../../' + metadata['source_snapshot'] + ')。\n'
    text += '- 变更：去除导航和用户评论入口，HTML 转 Markdown，图片改为相对路径，重复评级图标转成同义文字，新增中文导读、练习及验收。正文中的示例素材署名予以保留。\n'
    text += '- 本整理稿的新增中文内容同样按 CC BY 3.0 提供，署名“Pixel Tutorial Library 整理者（Codex）”；不暗示原作者认可本整理稿。\n'
    if video_records:
        if all(v['status'] == 'downloaded-with-extracted-stills' for v in video_records):
            text += '- 嵌入动态演示保存原始 webm，并按时长的10%、50%、90%提取静态帧辅助离线阅读；这是画面抽帧，不是语音、字幕或完整动作转录。\n'
        else:
            text += '- 部分嵌入视频只保留原地址，具体下载/抽帧结果见清单 embedded_videos 字段；不得将链接或抽帧当作完整视频转录。\n'
    text += '\n| 本地图像 | 原图来源 | 图示语境 |\n| --- | --- | --- |\n'
    for record in image_records:
        local = os.path.relpath(ROOT / record['path'], md_path.parent)
        text += '| [' + Path(record['path']).name + '](' + local + ') | [原图](' + record['source_url'] + ') | ' + clean_inline(record['caption']) + ' |\n'
    md_path.write_text(text)
    metadata['markdown_sha256'] = sha(text.encode())
    metadata['markdown_bytes'] = len(text.encode())
    print(json.dumps({'id':ident,'images':len(image_records),'bytes':metadata['markdown_bytes'],'videos_linked':len(video_records)},ensure_ascii=False), flush=True)
    return metadata


def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(collect, GUIDES))
    results.sort(key=lambda item: item['id'])
    out = ROOT / 'manifests/game-development.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'tutorials':len(results),'images':sum(len(t['images']) for t in results),'manifest':str(out)},ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
