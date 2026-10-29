#!/usr/bin/env python3
"""Meaningful inheritance failures and evidence-bound status tests; no image judgment."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_theme_contract import validate

ROOT = Path(__file__).resolve().parents[1]


class ThemeContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='theme-contract-test-')
        self.root = Path(self.temp.name)
        self.asset = self.root / 'fixture.bin'
        self.asset.write_bytes(b'fixture, not a visual test')
        self.sha = hashlib.sha256(self.asset.read_bytes()).hexdigest()
        self.contract_path = self.root / 'theme-contract.json'
        self.evidence = [{'path': 'fixture.bin', 'sha256': self.sha, 'scope': 'synthetic structure fixture'}]
        self.contract = {
            'schema_version': 1,
            'project_theme': {
                'id': 'rural-shared', 'revision': '1', 'style_identity': 'one shared theme',
                'color_roles': {'world_palette': ['#223322']},
                'lighting': {'key_direction': 'upper-left'},
                'projection': {'world': 'front-top-down'},
                'pixel_strategy': {'logical_grid': [16, 16], 'export_scale': 1},
                'typography': {'font_sources': ['fixture-only'], 'final_screen_checks': ['fixture-only']},
            },
            'declared_roles': ['world', 'UI'],
            'roles': {'world': {'inherits': 'project_theme', 'overrides': []},
                      'UI': {'inherits': 'project_theme', 'overrides': []}},
            'assets': [{'file': 'fixture.bin', 'theme_id': 'rural-shared', 'role_id': 'world',
                        'sha256': self.sha, 'exception_ids': []}],
            'exceptions': [],
            'review_matrix': [{'id': 'fixture', 'category': 'technical', 'subject': 'synthetic file',
                               'method': 'hash match only', 'evidence': self.evidence,
                               'expected': 'matching bytes', 'observed': 'matched bytes',
                               'status': 'OBSERVED_PASS', 'exception': None}],
            'overall': {'visual_status': 'NOT_APPLICABLE', 'runtime_status': 'NOT_APPLICABLE'},
            'technical_audit_bridge': {'strict_pixel_production_status': 'NOT_APPLICABLE'},
        }

    def tearDown(self):
        self.temp.cleanup()

    def run_contract(self):
        self.contract_path.write_text(json.dumps(self.contract), encoding='utf-8')
        return validate(self.contract_path)

    def has_finding(self, report, phrase):
        return any(phrase in f['message'] for f in report['findings'])

    def test_complete_structure_fixture_does_not_claim_visual_analysis(self):
        report, code = self.run_contract()
        self.assertEqual((code, report['structure_status'], report['validation_status']), (0, 'PASS', 'PASS'))
        self.assertIn('does not inspect image pixels', report['boundary'])
        self.assertEqual(report['recorded_visual_status'], 'NOT_APPLICABLE')

    def test_asset_cannot_select_a_different_theme(self):
        self.contract['assets'][0]['theme_id'] = 'unrelated-neon-theme'
        report, code = self.run_contract()
        self.assertEqual(code, 1)
        self.assertEqual(report['structure_status'], 'FAIL')
        self.assertTrue(self.has_finding(report, 'per-asset reselection'))

    def test_undeclared_roles_and_inline_style_overrides_are_rejected(self):
        self.contract['roles']['neon'] = {'inherits': 'project_theme', 'overrides': []}
        self.contract['assets'][0]['role_id'] = 'neon'
        self.contract['assets'][0]['palette'] = ['#ff00ff']
        report, code = self.run_contract()
        self.assertEqual(code, 1)
        self.assertTrue(self.has_finding(report, 'Undeclared role'))
        self.assertTrue(self.has_finding(report, 'Inline asset style'))

    def test_role_override_requires_a_reason_and_actual_evidence(self):
        self.contract['roles']['UI']['overrides'] = [{
            'field': 'projection.world', 'value': 'orthographic-front',
            'reason': '', 'evidence': [], 'review_status': 'DOCUMENTED',
        }]
        report, code = self.run_contract()
        self.assertEqual(code, 1)
        self.assertTrue(self.has_finding(report, 'concrete reason'))
        self.assertTrue(self.has_finding(report, 'at least one source'))
        self.contract['roles']['UI']['overrides'][0].update(
            reason='UI is a reading surface, while world geometry stays unchanged.', evidence=self.evidence)
        report, code = self.run_contract()
        self.assertEqual(code, 0)
        self.assertEqual(report['structure_status'], 'PASS')

    def test_missing_exception_and_out_of_scope_exception_do_not_resolve(self):
        self.contract['assets'][0]['exception_ids'] = ['ex-ui']
        report, code = self.run_contract()
        self.assertEqual(code, 1)
        self.assertTrue(self.has_finding(report, 'Unresolved asset exception'))
        self.contract['exceptions'] = [{
            'id': 'ex-ui', 'scope': {'asset_files': [], 'role_ids': ['UI']},
            'reason': 'Only this UI reading surface may differ.', 'evidence': self.evidence,
            'overrides': [], 'review_status': 'DOCUMENTED', 'production_limit': 'Scope only; no global waiver.',
        }]
        report, code = self.run_contract()
        self.assertEqual(code, 1)
        self.assertTrue(self.has_finding(report, 'does not cover this asset'))

    def test_unknown_grid_and_unreviewed_visuals_remain_incomplete(self):
        self.contract['project_theme']['pixel_strategy']['logical_grid'] = None
        self.contract['overall']['visual_status'] = 'UNDETERMINED'
        report, code = self.run_contract()
        self.assertEqual((code, report['structure_status'], report['validation_status']), (2, 'PASS', 'INCOMPLETE'))

    def test_changed_source_hash_invalidates_old_evidence(self):
        self.asset.write_bytes(b'changed after review')
        report, code = self.run_contract()
        self.assertEqual(code, 2)
        self.assertTrue(self.has_finding(report, 'Evidence changed'))

    def test_exception_never_erases_a_recorded_hard_gate_failure(self):
        self.contract['exceptions'] = [{
            'id': 'demo-source', 'scope': {'asset_files': ['fixture.bin'], 'role_ids': []},
            'reason': 'Source retained for an explicitly limited prototype.', 'evidence': self.evidence,
            'overrides': [], 'review_status': 'DOCUMENTED', 'production_limit': 'Not a production approval.',
        }]
        self.contract['assets'][0]['exception_ids'] = ['demo-source']
        self.contract['review_matrix'][0].update(category='strict-pixel-production',
            expected='binary alpha', observed='recorded partial alpha', status='OBSERVED_FAIL', exception='demo-source')
        self.contract['technical_audit_bridge']['strict_pixel_production_status'] = 'OBSERVED_FAIL'
        report, code = self.run_contract()
        self.assertEqual((code, report['structure_status']), (1, 'PASS'))
        self.assertEqual(report['recorded_hard_gate_failures'][0]['exception'], 'demo-source')

    def test_cli_emits_parseable_layered_json_and_meaningful_exit_status(self):
        self.contract['project_theme']['pixel_strategy']['export_scale'] = None
        self.run_contract()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_theme_contract.py'),
                                 str(self.contract_path), '--json'], capture_output=True, text=True)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report['structure_status'], 'PASS')
        self.assertEqual(report['completion_status'], 'INCOMPLETE')

    def test_invalid_json_returns_a_report_instead_of_a_traceback(self):
        self.contract_path.write_text('{broken', encoding='utf-8')
        report, code = validate(self.contract_path)
        self.assertEqual(code, 1)
        self.assertEqual(report['structure_status'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
