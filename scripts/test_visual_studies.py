#!/usr/bin/env python3
"""Offline behavior checks for visual-study retrieval and theme inheritance briefs."""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from search import Library, ROOT, main as search_main
from task_bundle import build


class VisualStudiesBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = Library()

    def test_direct_id_and_cli_list_stay_separate_from_tutorials_and_ui(self):
        row = self.lib.direct('ART-CASE-001')
        self.assertEqual((row['kind'], row['game']), ('visual-case', 'Hyper Light Drifter'))
        self.assertEqual(self.lib.direct('ART-CASE-001', image_limit=0)['figures'], [])
        self.assertNotIn(row['id'], self.lib.by_id)
        self.assertNotIn(row['id'], {case['id'] for case in self.lib.ui_cases})
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = search_main(['--list', 'visual-cases', '--json'])
        self.assertEqual(code, 0)
        rows = json.loads(output.getvalue())['results']
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r['kind'] == 'visual-case' and r['figures'] == [] for r in rows))
        self.assertEqual(sum(len(c['images']) for c in self.lib.visual_cases), 8)

    def test_game_and_metadata_search_are_specific_and_no_match_is_honest(self):
        result = self.lib.search('DAVE THE DIVER', kind='visual-case')
        self.assertEqual([r['id'] for r in result['results']], ['ART-CASE-004'])
        self.assertEqual(self.lib.search('几何母题', kind='visual-case')['results'][0]['id'], 'ART-CASE-001')
        self.assertEqual(self.lib.search('纹理', kind='visual-case')['results'][0]['id'], 'ART-CASE-002')
        for query in ('量子星港纠错电路', '像素游戏案例'):
            result = self.lib.search(query, kind='visual-case')
            self.assertEqual((result['status'], result['results']), ('no_match', []))
        with tempfile.TemporaryDirectory(prefix='pixel-visual-optional-') as tmp:
            root = Path(tmp)
            (root / 'library').mkdir()
            (root / 'references').mkdir()
            shutil.copyfile(ROOT / 'library/catalog.json', root / 'library/catalog.json')
            shutil.copyfile(ROOT / 'references/task-routing.json', root / 'references/task-routing.json')
            optional = Library(root)
            self.assertEqual(optional.visual_cases, [])
            self.assertEqual(optional.search('DAVE THE DIVER', kind='visual-case')['status'], 'no_match')

    def test_all_mode_requires_explicit_research_intent(self):
        for query in ('制作像素角色行走动画', '俯视农舍地图素材制作', '制作拟物餐厅图标',
                      'Hyper Light Drifter', '不要案例，制作俯视房屋'):
            rows = self.lib.search(query, kind='all')['results']
            self.assertFalse(any(r['kind'] == 'visual-case' for r in rows), query)
        for intent in ('案例', '拆解', '画面分析', '风格参考', '一致性研究'):
            rows = self.lib.search('Hyper Light Drifter ' + intent, kind='all')['results']
            self.assertEqual([r['id'] for r in rows if r['kind'] == 'visual-case'], ['ART-CASE-001'])

    def test_copy_figures_exports_teaching_images_never_commercial_references(self):
        with tempfile.TemporaryDirectory(prefix='pixel-visual-bundle-') as tmp:
            result = build('Hyper Light Drifter 案例与俯视农舍教程', tmp, limit=3, copy_figures=True)
            out = Path(tmp)
            brief = json.loads((out / 'task-brief.json').read_text())
            attrs = json.loads((out / 'figure-attributions.json').read_text())
            refs = brief['visual_game_references']
            self.assertTrue(refs)
            self.assertEqual(result['visual_game_references'], len(refs))
            self.assertEqual(result['tutorials'], len(brief['tutorials']))
            self.assertTrue(attrs)
            self.assertEqual(len(list((out / 'figures').iterdir())), len(attrs))
            for figure in attrs:
                self.assertTrue(figure['path'].startswith('library/'))
                self.assertNotIn('steam', figure['source_url'])
                self.assertFalse(figure.get('remote_only'))
            md = (out / 'task-brief.md').read_text()
            for case in refs:
                for figure in case['figures']:
                    self.assertTrue(figure['remote_only'])
                    self.assertNotIn('bundle_path', figure)
                    self.assertNotIn('absolute_path', figure)
                    self.assertTrue(figure['rights']['restrictions'])
                    self.assertIn(figure['url'], md)
                    self.assertNotIn(figure['sha256'], {f['sha256'] for f in attrs})

    def test_compact_records_preserve_evidence_layers_and_promotional_exception(self):
        source = next(c for c in self.lib.visual_cases if c['id'] == 'ART-CASE-002')
        row = self.lib.direct(source['id'])
        for field in ('observed', 'design_inferences', 'cohesion_rules', 'exceptions_and_limits',
                      'viewpoint', 'rights', 'evidence_status'):
            self.assertEqual(row[field], source[field], field)
        self.assertTrue(Path(row['absolute_path']).is_file())
        self.assertEqual(row['registry_path'], 'references/visual-game-studies.json')
        self.assertTrue(Path(row['absolute_registry_path']).is_file())
        for figure, original in zip(row['figures'], source['images']):
            self.assertEqual(figure['evidence_type'], original['evidence_type'])
            self.assertEqual(figure['observations'], original['observations'])
            self.assertEqual(figure['source_page'], original['source_url'])
            self.assertTrue(figure['license'])
        self.assertEqual(row['figures'][1]['evidence_type'], 'official-store-screenshot-with-promotional-overlay')

    def test_theme_contract_entry_precedes_style_candidates_without_claiming_review(self):
        with tempfile.TemporaryDirectory(prefix='pixel-theme-entry-') as tmp:
            build('制作乡村木质按钮', tmp, style='cozy-rural')
            out = Path(tmp)
            brief = json.loads((out / 'task-brief.json').read_text())
            self.assertEqual(brief['visual_game_references'], [])
            theme = brief['theme_cohesion']
            self.assertEqual(theme['project_contract_status'], 'NOT_LOADED')
            self.assertTrue(Path(theme['absolute_reference_path']).is_file())
            self.assertTrue(Path(theme['absolute_template_path']).is_file())
            self.assertIn('先加载项目已有主题合同', theme['application_order'][0])
            self.assertIn('role', theme['application_order'][1])
            self.assertIn('例外', theme['application_order'][2])
            self.assertIn('最后', theme['application_order'][3])
            self.assertIn('reason', theme['role_override_fields'])
            self.assertIn('evidence', theme['exception_requirements'])
            self.assertIn('validate_theme_contract.py', theme['validation_command'])
            self.assertIn('不自动鉴定', theme['validation_boundary'])
            md = (out / 'task-brief.md').read_text()
            self.assertLess(md.index('## 项目主题继承入口'), md.index('## 风格约定'))
            self.assertIn('已有项目不为每个 asset 重新选择主题', md)
            self.assertIn('NOT_LOADED', md)


if __name__ == '__main__':
    unittest.main(verbosity=2)
