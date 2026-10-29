#!/usr/bin/env python3
"""Behavioral retrieval checks using the actual bundled knowledge and relocation."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,unittest
from search import Library,ROOT
from task_bundle import build

class RetrievalBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.lib=Library()

    def test_natural_language_tasks_reach_distinct_sources(self):
        cases=[
            ('做南方乡村俯视像素游戏，需要农舍、树木和草地地图',{'ART-008','ART-011','ART-012'}),
            ('给村民做四方向行走和待机动画',{'ANIM-003','ANIM-006'}),
            ('设计暗黑奇幻背包UI，九宫格面板和手柄焦点',{'UI-001','UI-002'}),
            ('检查草木石的光源是否一致，并生成美术一致性检查清单',{'ART-003','ART-011','ART-015'})]
        rankings=[]
        for task,needed in cases:
            with self.subTest(task=task):
                rows=self.lib.search(task,limit=8)['results'];ids={x['id'] for x in rows};rankings.append(tuple(x['id'] for x in rows))
                self.assertTrue(needed<=ids,(needed,ids))
                for row in rows:
                    self.assertTrue(Path(row['absolute_path']).is_file())
                    self.assertLessEqual(len(row['figures']),2)
                    self.assertTrue(row['reasons'])
                    for image in row['figures']:
                        self.assertTrue(Path(image['absolute_path']).is_file());self.assertTrue(image['source_url']);self.assertTrue(image['license'])
        self.assertEqual(len(set(rankings)),4)

    def test_direct_id_is_exact_and_empty_query_is_honest(self):
        row=self.lib.direct('ART-008');self.assertEqual(row['id'],'ART-008')
        self.assertIn('Top-Down-Houses',row['figures'][0]['absolute_path'])
        result=self.lib.search('量子纠缠纠错电路求解器')
        self.assertEqual(result['status'],'no_match');self.assertEqual(result['results'],[])
        with self.assertRaises(ValueError):self.lib.validate_profile('style','totally-unknown-style')

    def test_selected_profiles_and_negative_hint(self):
        p=self.lib.search('暗黑背包UI',kind='all',style='dark-gothic',ui_style='dark-stone')['results']
        self.assertIn('dark-gothic',[x['id'] for x in p]);self.assertIn('dark-stone',[x['id'] for x in p])
        rejected=self.lib.profile_search('style','不要暗黑，采用科幻霓虹风格',limit=8)
        self.assertNotIn('dark-gothic',[x['id'] for x in rejected])
        self.assertIn('neon-scifi',[x['id'] for x in rejected])

    def test_bundle_contains_copy_and_attribution_without_changing_source(self):
        source=Path(self.lib.direct('ART-008')['figures'][0]['absolute_path'])
        before=hashlib.sha256(source.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix='pixel-task-bundle-') as tmp:
            result=build('俯视农舍和村庄树木',tmp,limit=4,copy_figures=True)
            self.assertEqual(result['status'],'ok')
            payload=json.loads((Path(tmp)/'task-brief.json').read_text())
            attrs=json.loads((Path(tmp)/'figure-attributions.json').read_text())
            self.assertTrue(payload['workflow']);self.assertGreater(len(attrs),0)
            for im in attrs:
                p=Path(tmp)/im['bundle_path'];self.assertTrue(p.is_file())
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),im['sha256'])
                self.assertTrue(im['author']);self.assertTrue(im['license']);self.assertTrue(im['source_url'])
                if im.get('bundle_license_file'):self.assertTrue((Path(tmp)/im['bundle_license_file']).is_file())
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),before)

    def test_relocated_skill_uses_new_root(self):
        with tempfile.TemporaryDirectory(prefix='pixel-relocation-') as tmp:
            dest=Path(tmp)/'renamed skill';(dest/'scripts').mkdir(parents=True);(dest/'references').mkdir()
            for name in ['search.py','task_bundle.py']:shutil.copyfile(ROOT/'scripts'/name,dest/'scripts'/name)
            for name in ['task-routing.json','style-profiles.json','ui-profiles.json','style-design.md','ui-design.md']:
                shutil.copyfile(ROOT/'references'/name,dest/'references'/name)
            shutil.copytree(ROOT/'library',dest/'library',ignore=shutil.ignore_patterns('._*','.DS_Store','__pycache__'))
            proc=subprocess.run([sys.executable,str(dest/'scripts/search.py'),'--task','俯视农舍','--json','--limit','3'],cwd=tmp,capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr);payload=json.loads(proc.stdout)
            self.assertEqual(payload['skill_root'],str(dest.resolve()))
            self.assertEqual(payload['status'],'ok')
            for row in payload['results']:
                self.assertTrue(row['absolute_path'].startswith(str(dest.resolve())))
                self.assertTrue(Path(row['absolute_path']).is_file())
                for im in row['figures']:self.assertTrue(im['absolute_path'].startswith(str(dest.resolve())))
            self.assertNotIn('/Volumes/',proc.stdout);self.assertNotIn(str(ROOT),proc.stdout)

if __name__=='__main__':unittest.main(verbosity=2)
