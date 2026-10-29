#!/usr/bin/env python3
"""Offline task-aware tutorial, style and figure retrieval. Standard library only."""
from pathlib import Path
import argparse, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
PROFILE_HINTS = {
    'cozy-rural': ['乡村','村庄','农舍','田园','温馨','cozy','rural'],
    'limited-handheld': ['掌机','限色','handheld'],
    'one-bit': ['单色','1-bit','1bit','one-bit'],
    'vivid-arcade': ['街机','明快','鲜艳','arcade'],
    'muted-fantasy': ['低饱和','柔和','奇幻','fantasy'],
    'dark-gothic': ['暗黑','哥特','黑暗','gothic','dark'],
    'isometric-diorama': ['等距','等轴','微缩','isometric'],
    'neon-scifi': ['科幻','霓虹','未来','neon','scifi','sci-fi'],
    'wood-paper': ['木纸','木质','纸张','农舍','乡村','田园','cozy'],
    'compact-handheld': ['掌机','紧凑','小屏','handheld'],
    'bold-arcade': ['街机','粗边','醒目','arcade'],
    'ornate-fantasy': ['奇幻','华丽','卷轴','fantasy'],
    'dark-stone': ['暗黑','哥特','黑暗','石质','gothic','dark'],
    'holo-terminal': ['科幻','全息','终端','霓虹','scifi','sci-fi','neon']
}

def flat(value):
    if isinstance(value, dict): return ' '.join(flat(v) for v in value.values())
    if isinstance(value, (list,tuple)): return ' '.join(flat(v) for v in value)
    return str(value or '')

def contains(text, term):
    text=text.casefold();term=str(term).casefold()
    if not term:return False
    if re.search(r'[a-z0-9]',term) and not re.search(r'[\u3400-\u9fff]',term):
        return re.search(r'(?<![a-z0-9_])'+re.escape(term)+r'(?![a-z0-9_])',text) is not None
    return term in text

def is_negated(text, term):
    return re.search(r'(?:不要|不想要|不采用|避免|排除)\s*'+re.escape(term),text,re.I) is not None

def safe_path(root, relative):
    p=(root/relative).resolve()
    if p!=root and root not in p.parents:raise ValueError('Path escapes skill folder: '+str(relative))
    return p

class Library:
    def __init__(self,root=ROOT):
        self.root=Path(root).resolve();self.library=self.root/'library'
        catalog=self.library/'catalog.json'
        if not catalog.is_file():raise ValueError('Bundled library/catalog.json is missing. Install/extract the whole skill folder.')
        self.entries=json.loads(catalog.read_text(encoding='utf-8'))
        self.by_id={x['id']:x for x in self.entries}
        case_file=self.root/'references/ui-case-studies.json'
        self.ui_cases=json.loads(case_file.read_text(encoding='utf-8')).get('cases',[]) if case_file.is_file() else []
        routing=json.loads((self.root/'references/task-routing.json').read_text(encoding='utf-8'))
        self.concepts=routing['concepts'];self.routes=routing['routes'];self.profiles={}
        for kind,name in [('style','style-profiles.json'),('ui','ui-profiles.json')]:
            p=self.root/'references'/name
            self.profiles[kind]=json.loads(p.read_text()).get('profiles',[]) if p.is_file() else []

    def validate_profile(self,kind,pid):
        if not pid:return None
        for p in self.profiles[kind]:
            if p['id']==pid:return p
        ids=', '.join(p['id'] for p in self.profiles[kind]) or '(profile file missing or empty)'
        raise ValueError(f'Unknown {kind} profile {pid!r}. Available: {ids}')

    def match_routes(self,task):
        result=[]
        for r in self.routes:
            hits=[k for k in r['keywords'] if contains(task,k) and not is_negated(task,k)]
            if hits:
                score=r.get('priority',10)+min(len(hits),4)*8
                result.append(dict(r,score=score,matched_keywords=hits))
        return sorted(result,key=lambda r:(-r['score'],r['id']))

    def active_concepts(self,task):
        return {name:aliases for name,aliases in self.concepts.items() if any(contains(task,a) and not is_negated(task,a) for a in aliases)}

    def figures(self,entry,limit=2):
        images=entry.get('images',[])
        def key(im):
            role=im.get('role',im.get('kind',''))
            if role in ['original','original-gif'] or im.get('derived') is False:return 0
            if role in ['keyframes','extracted-frame']:return 1
            if role=='preview':return 3
            return 2
        images=sorted(enumerate(images),key=lambda pair:(key(pair[1]),pair[0]))
        chosen=[]
        for _,im in images:
            rel='library/'+im['path'];p=safe_path(self.root,rel)
            if not p.is_file():continue
            chosen.append({'path':rel,'absolute_path':str(p),'caption':im.get('caption',''),
                'source_url':im.get('source_url',entry.get('source_url','')),
                'author':im.get('author',entry.get('author','')),'license':im.get('license',entry.get('license','')),
                'license_url':im.get('license_url',entry.get('license_url','')),
                'role':im.get('role',im.get('kind','source-figure')),
                'usage':'教学配图；用于理解方法，不代表可直接作为游戏成品素材。'})
            if len(chosen)>=limit:break
        return chosen if limit>0 else []

    def compact_tutorial(self,e,score=0,reasons=None,image_limit=2):
        rel='library/'+e['path'];p=safe_path(self.root,rel)
        return {'kind':'tutorial','id':e['id'],'title':e['title'],'category':e['category'],
            'summary':e.get('summary',''),'score':round(score,2),'reasons':reasons or ['按ID直接读取'],
            'path':rel,'absolute_path':str(p),'document_exists':p.is_file(),
            'source_url':e['source_url'],'author':e.get('author',''),'license':e.get('license',''),
            'license_url':e.get('license_url',''),'version':e.get('version',''),
            'content_mode':e.get('content_mode',''),'figures':self.figures(e,image_limit),
            'figure_count_total':len(e.get('images',[]))}

    def tutorial_search(self,task,limit=6,image_limit=2,style=None,ui_style=None,fulltext=False):
        routes=self.match_routes(task);concepts=self.active_concepts(task)
        explicit=[p for p in [self.validate_profile('style',style),self.validate_profile('ui',ui_style)] if p]
        tokens=[t for t in re.findall(r'[A-Za-z][A-Za-z0-9_.-]{2,}',task) if t.lower() not in ['the','and','with','for','make','create','pixel','game']]
        rows=[]
        for e in self.entries:
            title=flat([e['id'],e['title']]);tags=flat(e.get('tags',[]));meta=flat([e.get('summary',''),e.get('learning_objectives',[])])
            score=0;reasons=[]
            for concept,aliases in concepts.items():
                t=any(contains(title,a) for a in aliases);g=any(contains(tags,a) for a in aliases);m=any(contains(meta,a) for a in aliases)
                weight=8*t+6*g+2*m
                if weight:score+=weight;reasons.append('主题匹配：'+concept)
            for tok in tokens:
                if contains(title,tok) or contains(tags,tok):score+=10;reasons.append('术语匹配：'+tok)
            route_boosts=[]
            for r in routes:
                if e['id'] in r['tutorial_ids']:
                    rank=r['tutorial_ids'].index(e['id']);route_boosts.append(max(5,24-rank*1.5)+r['score']*.35)
                    reasons.append('任务路线：'+r['name'])
            if route_boosts:
                route_boosts.sort(reverse=True)
                score+=route_boosts[0]+min(sum(route_boosts[1:])*.2,5)
            for profile in explicit:
                if e['id'] in profile.get('tutorial_ids',[]):score+=18;reasons.append('所选风格参考：'+profile['id'])
            if fulltext and concepts:
                p=safe_path(self.root,'library/'+e['path'])
                if p.is_file():
                    body=p.read_text().casefold();body_hits=[c for c,aliases in concepts.items() if any(contains(body,a) for a in aliases)]
                    if body_hits:score+=min(len(body_hits)*1.2,6)
            if contains(task,e['id']):score+=100;reasons.insert(0,'任务中明确引用ID')
            if score>0:rows.append(self.compact_tutorial(e,score,list(dict.fromkeys(reasons))[:6],image_limit))
        rows.sort(key=lambda x:(-x['score'],x['id']))
        return rows[:limit]

    def compact_profile(self,profile,kind,score,reasons,image_limit=2,details=False):
        ref='references/'+('style-design.md' if kind=='style' else 'ui-design.md')
        figures=[]
        for im in profile.get('figures',[]):
            relative=im.get('path','');p=safe_path(self.root,relative)
            if not p.is_file():continue
            figures.append(dict(im,absolute_path=str(p),usage=im.get('scope','教程图仅展示方法，不是此风格的完整成品样例。')))
            if len(figures)>=image_limit:break
        row={'kind':kind,'id':profile['id'],'title':profile.get('name',profile['id']),
             'summary':profile.get('summary',''),'score':round(score,2),'reasons':reasons,
             'path':ref,'absolute_path':str(self.root/ref),'profile_file':'references/'+('style-profiles.json' if kind=='style' else 'ui-profiles.json'),
             'tutorial_ids':profile.get('tutorial_ids',[]),'palette':profile.get('palette',[]),
             'figures':figures if image_limit>0 else [],'editorial_notice':'整理者提供的可调整配方，项目既有规范和用户要求优先；图示不等于完整风格样张。'}
        if details:
            for key in ['tasks','parameters','avoid_mixing','visual_checks','ui_profile_ids','art_profile_ids']:
                if key in profile:row[key]=profile[key]
        return row

    def profile_search(self,kind,task,limit=2,image_limit=2,selected=None,details=False):
        if selected:
            p=self.validate_profile(kind,selected)
            return [self.compact_profile(p,kind,100,['本次调用参数指定；不代表用户已批准全部风格参数'],image_limit,details)]
        routes=self.match_routes(task);rows=[]
        for profile in self.profiles[kind]:
            pid=profile['id'];score=0;reasons=[]
            hints=PROFILE_HINTS.get(pid,[])
            if any(is_negated(task,h) for h in hints):continue
            hits=[h for h in hints if contains(task,h)]
            if hits:score+=40+10*len(hits);reasons.append('风格线索：'+'、'.join(hits))
            key='style_ids' if kind=='style' else 'ui_style_ids'
            for route in routes:
                if pid in route.get(key,[]):
                    score+=12+route['score']*.1;reasons.append('任务候选：'+route['name'])
            if score>0:rows.append(self.compact_profile(profile,kind,score,reasons,image_limit,details))
        rows.sort(key=lambda p:(-p['score'],p['id']))
        return rows[:limit]

    def direct(self,ident,image_limit=2,details=False):
        if ident in self.by_id:return self.compact_tutorial(self.by_id[ident],100,['按ID直接读取'],image_limit)
        for c in self.ui_cases:
            if c['id']==ident:return self.compact_case(c,100,['按ID直接读取'],image_limit)
        for kind,profiles in self.profiles.items():
            for p in profiles:
                if p['id']==ident:return self.compact_profile(p,kind,100,['按ID直接读取'],image_limit,details)
        raise ValueError('Unknown tutorial/style/UI/case ID: '+ident)

    def compact_case(self,c,score,reasons,image_limit=2):
        relative='references/ui-case-studies.md'
        return {'kind':'case','id':c['id'],'title':c['game']+' · '+c['title'],
            'summary':c['application_note'],'score':score,'reasons':reasons,
            'path':relative,'absolute_path':str(self.root/relative),'source_url':c['source_url'],
            'tutorial_ids':c['tutorial_ids'],'ui_style_ids':c['style_ids'],
            'observed':c['observed'],'strengths':c['strengths'],'limitations':c['limitations'],
            'rights':c['rights'],'evidence_status':c['evidence_status'],
            'figures':[dict(im,source_url=im['url'],source_page=im['source_url'],remote_only=True,
                            author=c['creator'],license=c['rights']['license'],
                            usage='官方截图参考链接，不随资料包复制，不授予游戏素材复用许可。')
                       for im in c['images'][:image_limit]],
            'editorial_notice':'基于静态官方截图的原创分析；风格关联只表示某些规律可借鉴，不等于完整同款或交互验证。'}

    def case_search(self,task,limit=6,image_limit=2,style=None,ui_style=None):
        groups=[['背包','物品整理','库存','inventory'],['商店','交易','出售','shop'],
                ['对话','对白','dialogue'],['战斗','血条','hud','battle'],
                ['装备','equipment','loadout'],['科幻','机甲','tactical','mech'],
                ['幻想','奇幻','rpg'],['升级','level-up']]
        active=[g for g in groups if any(contains(task,t) and not is_negated(task,t) for t in g)]
        rows=[]
        for c in self.ui_cases:
            reasons=[];score=0;tags=flat(c['tags'])
            for g in active:
                if any(contains(tags,t) for t in g):score+=20;reasons.append('界面任务：'+g[0])
            for tag in c['tags']:
                if contains(task,tag) and not is_negated(task,tag):score+=5;reasons.append('案例关键词：'+tag)
            if contains(task,c['game']) or contains(task,c['id']):score+=100;reasons.append('明确指定案例')
            for pid,field in [(style,'art_style_ids'),(ui_style,'style_ids')]:
                if pid and pid in c.get(field,[]):score+=12;reasons.append('可借鉴关联：'+pid)
            if score:rows.append(self.compact_case(c,score,list(dict.fromkeys(reasons))[:6],image_limit))
        return sorted(rows,key=lambda c:(-c['score'],c['id']))[:limit]

    def search(self,task,kind='tutorial',limit=6,image_limit=2,style=None,ui_style=None,fulltext=False,details=False):
        self.validate_profile('style',style);self.validate_profile('ui',ui_style)
        results=[]
        if kind in ['tutorial','all']:results+=self.tutorial_search(task,limit,image_limit,style,ui_style,fulltext)
        if kind in ['style','all']:results+=self.profile_search('style',task,min(limit,2) if kind=='all' else limit,image_limit,style,details)
        if kind in ['ui','all']:results+=self.profile_search('ui',task,min(limit,2) if kind=='all' else limit,image_limit,ui_style,details)
        ui_request=ui_style or any(r['id']=='game-ui' for r in self.match_routes(task))
        if kind=='case' or (kind=='all' and ui_request):
            results+=self.case_search(task,min(limit,3) if kind=='all' else limit,image_limit,style,ui_style)
        return {'status':'ok' if results else 'no_match','task':task,'kind':kind,
                'skill_root':str(self.root),'results':results,
                'matched_routes':[{'id':r['id'],'name':r['name'],'matched_keywords':r['matched_keywords']} for r in self.match_routes(task)[:3]],
                'note':'基于本地主题词、任务路线和元数据排序；不是向量模型，也不表示已执行教程或审美检验。' if results else '没有与本地知识库匹配的教程或风格；请缩小任务或补充来源。'}

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='');p.add_argument('--task')
    p.add_argument('--kind',choices=['tutorial','style','ui','case','all'],default='tutorial')
    p.add_argument('--style');p.add_argument('--ui-style');p.add_argument('--id')
    p.add_argument('--list',choices=['styles','ui-styles','cases','routes'],help='List available profiles/cases/routes without retrieving figures')
    p.add_argument('--limit',type=int,default=6);p.add_argument('--images',type=int,default=2)
    p.add_argument('--fulltext',action='store_true');p.add_argument('--details',action='store_true');p.add_argument('--json',action='store_true')
    return p

def main(argv=None):
    p=parser();a=p.parse_args(argv);task=a.task if a.task is not None else a.query
    if not 1<=a.limit<=30:p.error('--limit must be between 1 and 30')
    if not 0<=a.images<=5:p.error('--images must be between 0 and 5')
    if not task.strip() and not a.id and not a.list:p.error('Provide a task/query, --id, or --list')
    try:
        lib=Library()
        if a.list:
            if a.list=='cases':
                rows=[lib.compact_case(c,0,['可用真实游戏案例'],0) for c in lib.ui_cases]
            elif a.list=='routes':
                rows=[{'kind':'route','id':r['id'],'title':r['name'],'summary':'、'.join(r['keywords'][:6]),'score':0,'reasons':['可用任务路线'],'absolute_path':str(lib.root/'references/task-routing.json'),'tutorial_ids':[tid for tid in r['tutorial_ids'] if tid in lib.by_id]} for r in lib.routes]
            else:
                k='style' if a.list=='styles' else 'ui'
                rows=[lib.compact_profile(q,k,0,['可用风格配方'],0,a.details) for q in lib.profiles[k]]
            result={'status':'ok' if rows else 'no_match','list':a.list,'results':rows,'note':'可用项目列表；未表示已为当前项目选择风格。'}
        else:
            result={'status':'ok','results':[lib.direct(a.id,a.images,a.details)]} if a.id else lib.search(task,a.kind,a.limit,a.images,a.style,a.ui_style,a.fulltext,a.details)
    except (ValueError,OSError,json.JSONDecodeError) as ex:
        if a.json: print(json.dumps({'status':'error','error':str(ex)},ensure_ascii=False))
        else:print('Error: '+str(ex),file=sys.stderr)
        return 2
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('status: '+result['status'])
        for row in result['results']:
            print(f'\n{row["id"]} | {row["title"]} | {row["kind"]} | score={row["score"]}')
            print('  '+str(row['absolute_path']))
            print('  '+str(row.get('summary','')))
            print('  理由：'+'；'.join(row['reasons']))
            for image in row.get('figures',[]):
                print('  图：'+image.get('absolute_path',image.get('url',image.get('source_url',''))));print('     '+image.get('caption',image.get('title','')))
        if result['status']=='no_match':print(result['note'])
    return 0
if __name__=='__main__':sys.exit(main())
