#!/usr/bin/env python3
"""Behavior checks for source-linked UI cases and copy boundaries."""
import json
import tempfile
import unittest
from pathlib import Path
from search import Library
from task_bundle import build

class UICasesTest(unittest.TestCase):
    def test_inventory_shop_finds_relevant_screens(self):
        rows=Library().search('设计背包与商店 UI',kind='case')['results']
        self.assertEqual({r['id'] for r in rows[:2]},{'UI-CASE-003','UI-CASE-006'})
        self.assertTrue(all(r['limitations'] for r in rows))

    def test_dialogue_task_includes_cases_in_all_mode(self):
        rows=Library().search("乡村游戏对话框",kind="all")["results"]
        ids={r["id"] for r in rows if r["kind"]=="case"}
        self.assertIn("UI-CASE-001",ids)
        self.assertIn("UI-CASE-002",ids)

    def test_unsupported_style_does_not_invent_case(self):
        self.assertEqual(Library().search('暗石风格',kind='case',ui_style='dark-stone')['status'],'no_match')
        self.assertEqual(Library().search('量子引力波',kind='case')['status'],'no_match')

    def test_direct_case_has_remote_figures_and_credit(self):
        row=Library().direct('UI-CASE-003')
        self.assertEqual(len(row['figures']),2)
        for f in row['figures']:
            self.assertTrue(f['remote_only'])
            self.assertNotIn('absolute_path',f)
            self.assertTrue(f['source_page'].startswith('https://store.steampowered.com/'))
            self.assertTrue(f['author'])
        self.assertEqual(Library().direct('UI-CASE-003',image_limit=0)['figures'],[])

    def test_ui_brief_copies_teaching_figures_only(self):
        with tempfile.TemporaryDirectory(prefix='pixel-ui-case-test-') as tmp:
            out=Path(tmp)/'brief'
            build('乡村背包与商店UI',out,limit=4,ui_style='wood-paper',copy_figures=True)
            brief=json.loads((out/'task-brief.json').read_text())
            self.assertTrue(brief['ui_case_references'])
            self.assertIn('真实游戏 UI 案例参考',(out/'task-brief.md').read_text())
            copied=json.loads((out/'figure-attributions.json').read_text())
            self.assertTrue(copied)
            self.assertFalse(any('steam' in f['source_url'] for f in copied))
            self.assertEqual(len(list((out/'figures').iterdir())),len(copied))

if __name__=='__main__':unittest.main()
