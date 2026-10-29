#!/usr/bin/env python3
"""Behavior checks for task-first UI research, evidence links, and public exports.

Uses the bundled knowledge, not source-text snapshots. All generated artifacts live
in temporary directories; no network access or commercial image download occurs.
"""
import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlparse

from search import Library, ROOT
from task_bundle import build as build_bundle
from build_ui_atlas import build as build_atlas


class UIDesignBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = Library()
        cls.source_rows = []
        for name in (
            'ui-foundation-sources.json',
            'ui-system-sources.json',
            'ui-evaluation-sources.json',
        ):
            cls.source_rows.extend(
                json.loads((ROOT / 'references' / name).read_text(encoding='utf-8'))['sources']
            )
        cls.sources = {row['id']: row for row in cls.source_rows}

    def assert_web_reference(self, value):
        parsed = urlparse(value)
        self.assertIn(parsed.scheme, ('http', 'https'), value)
        self.assertTrue(parsed.netloc, value)

    def system_results(self, query):
        result = self.lib.search(query, kind='system', details=True)
        self.assertEqual(result['status'], 'ok', query)
        self.assertTrue(result['results'], query)
        return result['results']

    def test_building_placement_retrieves_decision_and_recovery(self):
        row = self.system_results('农舍建造放置界面')[0]
        self.assertEqual(row['id'], 'building-placement')
        for key in ('required_content', 'states', 'input_flow', 'failures_and_recovery'):
            self.assertTrue(row[key], key)
        self.assertTrue(row['source_ids'])

    def test_shop_query_retrieves_trade_not_generic_inventory(self):
        row = self.system_results('商店买卖价格确认')[0]
        self.assertEqual(row['id'], 'shop-trade')
        self.assertTrue(row['required_content'])
        self.assertTrue(row['acceptance_checks'])
        self.assertTrue(row['source_ids'])

    def test_recipe_query_retrieves_crafting_constraints(self):
        row = self.system_results('配方材料不足如何制作')[0]
        self.assertEqual(row['id'], 'crafting')
        for key in ('information_structure', 'states', 'failures_and_recovery'):
            self.assertTrue(row[key], key)

    def test_general_pixel_asset_tasks_do_not_imply_ui_work(self):
        ui_kinds = {'ui', 'system', 'axis', 'case'}
        for task in (
            '制作像素角色行走动画',
            '绘制树木草地素材',
            '俯视农舍地图素材制作',
        ):
            with self.subTest(task=task):
                rows = self.lib.search(task, kind='all')['results']
                self.assertTrue(any(row['kind'] == 'tutorial' for row in rows))
                unintended = [(row['kind'], row['id']) for row in rows if row['kind'] in ui_kinds]
                self.assertEqual(unintended, [], f'Asset-only task implied UI work: {unintended}')

    def test_skeuomorphism_does_not_select_world_relation(self):
        visual = self.lib.search('拟物化界面', kind='axis')['results']
        self.assertIn('visual-treatment', {row['id'] for row in visual})
        self.assertNotIn('fiction-relation', {row['id'] for row in visual})
        world = self.lib.search('世界内界面', kind='axis')['results']
        self.assertIn('fiction-relation', {row['id'] for row in world})
        # The two questions must remain independently addressable, with their
        # own value sets rather than a single selected "style" answer.
        visual_values = {v['id'] for v in self.lib.direct('visual-treatment')['values']}
        world_values = {v['id'] for v in self.lib.direct('fiction-relation')['values']}
        self.assertTrue(visual_values)
        self.assertTrue(world_values)
        self.assertFalse(visual_values & world_values)

    def test_direct_ids_return_exact_system_axis_and_case(self):
        for ident, kind in (
            ('building-placement', 'system'),
            ('fiction-relation', 'axis'),
            ('UI-CASE-014', 'case'),
        ):
            with self.subTest(ident=ident):
                row = self.lib.direct(ident, details=True)
                self.assertEqual((row['id'], row['kind']), (ident, kind))
                self.assertTrue(Path(row['absolute_path']).is_file())
        case = self.lib.direct('UI-CASE-014', image_limit=0)
        self.assertEqual(case['figures'], [])
        with self.assertRaises(ValueError):
            self.lib.direct('UI-CASE-NOT-A-REAL-ID')

    def test_task_bundle_contains_system_fields_and_traceable_sources(self):
        with tempfile.TemporaryDirectory(prefix='pixel-ui-design-bundle-') as tmp:
            out = Path(tmp) / 'brief'
            build_bundle('设计商店交易 UI，拟物化界面', out, limit=4)
            bundle = json.loads((out / 'task-brief.json').read_text(encoding='utf-8'))
            md = (out / 'task-brief.md').read_text(encoding='utf-8')
            patterns = {row['id']: row for row in bundle['ui_system_patterns']}
            self.assertIn('shop-trade', patterns)
            row = patterns['shop-trade']
            for key in ('required_content', 'information_structure', 'states',
                        'input_flow', 'failures_and_recovery', 'acceptance_checks'):
                self.assertTrue(row[key], key)
            for source_id in row['source_ids']:
                self.assertIn(source_id, self.sources)
                self.assertIn(source_id, md)
            self.assertIn('visual-treatment', {a['id'] for a in bundle['ui_design_axes']})
            self.assertTrue(bundle['ui_case_references'])
            for case in bundle['ui_case_references']:
                self.assert_web_reference(case['source_url'])
                for figure in case['figures']:
                    self.assertTrue(figure['remote_only'])
                    self.assertNotIn('bundle_path', figure)
            self.assertEqual(bundle['copied_figure_count'], 0)
            self.assertFalse((out / 'figures').exists())

    def test_references_and_per_image_evidence_resolve(self):
        self.assertEqual(len(self.sources), len(self.source_rows), 'Duplicate source IDs')
        for source in self.source_rows:
            self.assert_web_reference(source['url'])
        cases = {case['id']: case for case in self.lib.ui_cases}
        self.assertEqual(len(cases), 14)
        self.assertEqual(len(cases), len(self.lib.ui_cases), 'Duplicate case IDs')
        self.assertEqual(sum(len(c['images']) for c in cases.values()), 28)
        for row in self.lib.ui_axes + self.lib.ui_systems:
            with self.subTest(reference=row['id']):
                self.assertTrue(row['source_ids'])
                self.assertTrue(set(row['source_ids']) <= self.sources.keys())
                for case_id in row.get('related_case_ids', []):
                    self.assertIn(case_id, cases)
                for tutorial_id in row.get('related_tutorial_ids', []):
                    self.assertIn(tutorial_id, self.lib.by_id)
        evidence_types = {'official-game-screenshot', 'developer-design-mockup', 'official-settings-guide'}
        system_ids = {row['id'] for row in self.lib.ui_systems}
        for case in cases.values():
            with self.subTest(case=case['id']):
                self.assert_web_reference(case['source_url'])
                self.assertTrue(case['rights'])
                self.assertTrue(case['classification'])
                self.assertTrue(set(case['classification']['systems']) <= system_ids)
                for tutorial_id in case['tutorial_ids']:
                    self.assertIn(tutorial_id, self.lib.by_id)
                for image in case['images']:
                    self.assertIn(image['evidence_type'], evidence_types)
                    self.assert_web_reference(image['url'])
                    self.assert_web_reference(image['source_url'])
                    self.assertTrue(image['observations'])
                    self.assertRegex(image['sha256'], r'^[0-9a-f]{64}$')
                    self.assertGreater(image['width'], 0)
                    self.assertGreater(image['height'], 0)
                    self.assertNotIn('local_path', image)

    def test_public_atlas_contains_remote_references_and_no_local_paths(self):
        with tempfile.TemporaryDirectory(prefix='pixel-ui-design-atlas-') as tmp:
            out = Path(tmp) / 'public'
            result = build_atlas(out)
            self.assertEqual((result['cases'], result['images']), (14, 28))
            self.assertEqual(result['local_reference_images'], 0)
            html = (out / 'index.html').read_text(encoding='utf-8')
            for forbidden in ('/Volumes/', '/Users/', 'file://', str(ROOT), str(out)):
                self.assertNotIn(forbidden, html)
            marker = 'const DATA='
            self.assertIn(marker, html)
            payload, _ = json.JSONDecoder().raw_decode(html.split(marker, 1)[1])
            self.assertFalse(payload['local_review'])
            for case in payload['cases']:
                for image in case['images']:
                    self.assertEqual(image['display_url'], image['url'])
                    self.assert_web_reference(image['display_url'])
            # Public export may contain HTML/data only; commercial binaries must
            # not appear incidentally merely because references have URLs.
            written = {p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
            self.assertEqual(written, {'index.html'})

    def test_local_atlas_cannot_copy_commercial_images_into_skill_tree(self):
        with tempfile.TemporaryDirectory(prefix='pixel-ui-design-boundary-') as tmp:
            fake_root = Path(tmp) / 'skill'
            fake_root.mkdir()
            image_map = Path(tmp) / 'local-map.json'
            image_map.write_text('{}', encoding='utf-8')
            for target in (fake_root, fake_root / 'public-review'):
                with self.subTest(target=target), self.assertRaises(ValueError):
                    build_atlas(target, image_map=image_map, root=fake_root)
            self.assertEqual(list(fake_root.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
