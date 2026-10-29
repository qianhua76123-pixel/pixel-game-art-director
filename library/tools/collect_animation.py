#!/usr/bin/env python3
"""Build Chinese annotated tutorials from pinned, CC-BY-4.0 Saint11 GIFs.
The lesson text was manually interpreted from the original figures; this is not OCR.
Run with the requirements.txt environment. Never overwrite unrelated files.
"""
from pathlib import Path
import argparse, hashlib, json, os, time
from urllib.parse import quote
import requests, yaml
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
COMMIT='ce1393eb2c46441d917134a9fd52e15575ee10a7'
BASE=f'https://raw.githubusercontent.com/saint11/Saint11Tutorials/{COMMIT}/'
FILES=['Walk.gif','RunCycleSimple.gif','TopDownWalkCycle.gif','TopDownRun.gif','TopDownAttack.gif','characterIdle.gif','Jump.gif','Easings.gif','loop.gif','Squash.gif','Subpixel.gif','MotionBlur.gif']

def fetch(url,target):
    if target.exists(): return target.read_bytes()
    for attempt in range(3):
        try:
            r=requests.get(url,timeout=45);r.raise_for_status()
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(r.content);return r.content
        except requests.RequestException:
            if attempt==2: raise
            time.sleep(1+attempt)

def main():
    lessons=json.loads((ROOT/'tools/animation_lessons.json').read_text())
    entries=[]
    for lesson,filename in zip(lessons,FILES):
        tid=lesson['id']; folder=ROOT/'assets/animation'/tid;folder.mkdir(parents=True,exist_ok=True)
        url=BASE+quote(filename); target=folder/filename
        data=fetch(url,target); digest=hashlib.sha256(data).hexdigest()
        im=Image.open(target); n=im.n_frames; durations=[]
        for f in range(n): im.seek(f);durations.append(im.info.get('duration',100))
        image_rows=[dict(path=target.relative_to(ROOT).as_posix(),source_url=url,caption='Saint11 原始动画教程图；包含文字与多个动画示例。',sha256=digest,kind='original-gif',width=im.width,height=im.height,frames=n)]
        for f in sorted(set([0,n//4,n//2,3*n//4])):
            im.seek(f); p=folder/f'frame-{f:03}.png';im.convert('RGBA').save(p)
            image_rows.append(dict(path=p.relative_to(ROOT).as_posix(),source_url=url,caption=f'原GIF第{f}帧（从0计），时间约{sum(durations[:f])} ms；帧截取，未重绘。',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),kind='extracted-frame',frame=f,time_ms=sum(durations[:f])))
        rel=f'tutorials/animation/{tid}-{lesson["slug"]}.md'; doc=ROOT/rel; doc.parent.mkdir(parents=True,exist_ok=True)
        source_page=f'https://github.com/saint11/Saint11Tutorials/blob/{COMMIT}/{quote(filename)}'
        entry=dict(id=tid,title=lesson['title'],category='animation',path=rel,source_url=source_page,source_title=filename,author='Pedro Medeiros (Saint11)',license='CC-BY-4.0',license_url='https://creativecommons.org/licenses/by/4.0/',license_evidence=f'https://github.com/saint11/Saint11Tutorials/blob/{COMMIT}/README.md',retrieved_at='2026-10-29',language='zh-CN',source_language='en',level=lesson['level'],tags=lesson['tags'],summary=lesson['summary'],images=image_rows,content_mode='translated-image-tutorial',version=f'Saint11Tutorials@{COMMIT}',prerequisites=lesson['prerequisites'],learning_objectives=lesson['concepts'],original_duration_ms=sum(durations),verification='original-image-visually-read; no engine execution')
        fm={k:v for k,v in entry.items() if k not in ['images','learning_objectives']}
        fm['image_count']=len(image_rows)
        def img(row):
            return f'![{row["caption"]}]({os.path.relpath(ROOT/row["path"],doc.parent)})'
        txt='---\n'+yaml.safe_dump(fm,allow_unicode=True,sort_keys=False)+'---\n\n'
        txt+=f'# {lesson["title"]}\n\n{lesson["summary"]}\n\n'
        txt+='## 用途与前提\n\n适合制作像素角色动画、评审动作稿，或为引擎动画状态准备资产。先具备：'+ '；'.join(lesson['prerequisites'])+'。\n\n'
        txt+='## 原作者教程图（本地原始 GIF）\n\n'+img(image_rows[0])+'\n\n'
        txt+=f'图源：[Pedro Medeiros / {filename}]({source_page})，CC BY 4.0。原文件 {im.width}×{im.height}，{n}个合成GIF帧，总时长约{sum(durations)} ms。**这是整个教程图的GIF容器帧数，不是每个角色示例的推荐动画帧数。**\n\n'
        txt+='## 关键概念（原图中文整理）\n\n'+''.join('- '+s+'\n' for s in lesson['concepts'])+'\n'
        txt+='## 操作步骤（根据原图重述）\n\n'+''.join(f'{i}. {s}\n' for i,s in enumerate(lesson['steps'],1))+'\n'
        txt+='## 如何读图\n\n'+lesson['read_image']+'\n\n'
        txt+='### 静态关键帧\n\n以下按GIF总帧序列的四个位置抽取，方便不支持动画的阅读器。它们不是动作逐帧全集；完整时序以原始GIF为准。\n\n'
        for row in image_rows[1:]: txt+=img(row)+'\n\n'+row['caption']+'\n\n'
        txt+='## 实作练习（整理者补充）\n\n'+lesson['exercise']+'\n\n'
        txt+='## 验收清单（整理者补充）\n\n'+''.join('- [ ] '+s+'\n' for s in lesson['checks'])+'\n'
        txt+='## 常见问题（整理者补充）\n\n'+''.join('- '+s+'\n' for s in lesson['pitfalls'])+'\n'
        txt+='## 给读取本文的 agent\n\n先使用文字中的概念和步骤，再按需要打开本地GIF/关键帧。不要仅凭图片文件名推断动作规则；不要把画法示例解释为固定帧率、固定碰撞箱或已经在某个引擎中测试。导出时记录画布尺寸、脚底锚点、方向、帧时长及状态标签。\n\n'
        txt+=f'## 来源、许可与整理说明\n\n- 原作者：Pedro Medeiros（Saint11）。\n- 固定版本来源：[{filename}]({source_page})。\n- 授权证据：[仓库 README]({entry["license_evidence"]})；许可证：[Creative Commons Attribution 4.0 International]({entry["license_url"]})。\n- 本地获取日期：2026-10-29。原始GIF SHA-256：`{digest}`。\n- 变更：原GIF原样保存；额外PNG由GIF帧截取；中文概念和步骤为依据原图的人工整理，未声称逐字全文OCR。练习、验收、常见问题与agent操作建议是整理者补充。中文改编也按CC BY 4.0提供，署名原作者并标注整理者为本教程库。\n- 未运行游戏工程；效果示例属于作者原图。原图中的风格偏好不作为所有项目的硬性规则。\n'
        doc.write_text(txt,encoding='utf-8');entries.append(entry)
    (ROOT/'manifests/animation.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'tutorials':len(entries),'images':sum(len(x['images']) for x in entries)},ensure_ascii=False))
if __name__=='__main__': main()
