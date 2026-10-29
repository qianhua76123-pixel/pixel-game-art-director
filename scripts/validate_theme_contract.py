#!/usr/bin/env python3
"""Validate recorded theme inheritance and evidence, never infer visual quality.

Exit 0: complete recorded contract without failures; 1: structural or recorded
hard-gate failure; 2: incomplete decisions/evidence. JSON is always printed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

REVIEW_STATES = {'OBSERVED_PASS', 'OBSERVED_FAIL', 'UNDETERMINED', 'NOT_APPLICABLE'}
DECISION_STATES = REVIEW_STATES | {'DOCUMENTED'}
ASSET_FIELDS = {'file', 'theme_id', 'role_id', 'sha256', 'dimensions', 'exception_ids', 'source_kind'}
CRITICAL_FIELDS = (
    'id', 'revision', 'style_identity', 'color_roles.world_palette',
    'lighting.key_direction', 'projection.world', 'pixel_strategy.logical_grid',
    'pixel_strategy.export_scale', 'typography.font_sources', 'typography.final_screen_checks',
)


def field_value(obj, path):
    current = obj
    for part in path.split('.'):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def unknown(value):
    return value is None or value == '' or value == [] or value == {} or value == 'UNDETERMINED'


def validate(path):
    path = Path(path).expanduser().resolve()
    findings = []
    hard_failures = []

    def note(level, location, message):
        findings.append({'level': level, 'location': location, 'message': message})

    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {'validation_status': 'FAIL', 'structure_status': 'FAIL', 'completion_status': 'INCOMPLETE',
                'findings': [{'level': 'ERROR', 'location': '$', 'message': str(exc)}],
                'boundary': 'No visual or image-pixel analysis is performed.'}, 1
    if not isinstance(data, dict):
        return {'validation_status': 'FAIL', 'structure_status': 'FAIL', 'completion_status': 'INCOMPLETE',
                'findings': [{'level': 'ERROR', 'location': '$', 'message': 'Contract must be a JSON object.'}]}, 1

    def evidence(items, location, require_nonempty=False):
        if not isinstance(items, list) or (require_nonempty and not items):
            note('ERROR', location, 'Evidence must be an explicit list; an override or exception needs at least one source.')
            return
        for i, item in enumerate(items):
            where = f'{location}[{i}]'
            if not isinstance(item, dict) or not any(item.get(k) for k in ('path', 'url', 'description')):
                note('ERROR', where, 'Evidence must identify a file, URL, or concrete observation description.')
                continue
            if item.get('path'):
                value = item['path']
                if not isinstance(value, str) or Path(value).is_absolute():
                    note('ERROR', where, 'Evidence paths must be contract-relative, not personal absolute paths.')
                    continue
                target = (path.parent / value).resolve()
                if not target.is_file():
                    note('INCOMPLETE', where, f'Evidence file missing: {value}')
                elif item.get('sha256') and hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
                    note('INCOMPLETE', where, f'Evidence changed; reassess this observation: {value}')

    theme = data.get('project_theme')
    if not isinstance(theme, dict):
        note('ERROR', 'project_theme', 'Project theme object is required.')
        theme = {}
    if data.get('schema_version') != 1:
        note('ERROR', 'schema_version', 'Only schema_version 1 is supported.')
    for field in CRITICAL_FIELDS:
        exists, value = field_value(theme, field)
        if not exists or unknown(value):
            note('INCOMPLETE', 'project_theme.' + field, 'Critical decision or evidence remains unspecified; not a pass.')
    theme_id = theme.get('id')
    if theme_id is not None and (not isinstance(theme_id, str) or not theme_id.strip()):
        note('ERROR', 'project_theme.id', 'Theme ID must be a nonempty string or null draft value.')

    declared = data.get('declared_roles')
    if not isinstance(declared, list) or not declared or not all(isinstance(x, str) and x for x in declared):
        note('ERROR', 'declared_roles', 'List every allowed role explicitly.')
        declared = []
    elif len(set(declared)) != len(declared):
        note('ERROR', 'declared_roles', 'Role IDs must be unique.')
    roles = data.get('roles', {})
    if not isinstance(roles, dict):
        note('ERROR', 'roles', 'Roles must be an object keyed by declared role ID.')
        roles = {}

    def overrides(rows, location):
        if not isinstance(rows, list):
            note('ERROR', location, 'Overrides must be a list.')
            return
        for i, item in enumerate(rows):
            where = f'{location}[{i}]'
            if not isinstance(item, dict):
                note('ERROR', where, 'Override must be an object.')
                continue
            field = item.get('field')
            if not isinstance(field, str) or not field_value(theme, field)[0]:
                note('ERROR', where, 'Override field must address an existing project_theme field.')
            elif field in {'id', 'revision', 'style_identity', 'ui_content_layer.mechanics_source'}:
                note('ERROR', where, 'Theme identity or game rules require a project revision, not a role/asset override.')
            if 'value' not in item or unknown(item.get('value')):
                note('INCOMPLETE', where, 'Override value is not established.')
            if not isinstance(item.get('reason'), str) or not item['reason'].strip():
                note('ERROR', where, 'Override requires a concrete reason.')
            evidence(item.get('evidence'), where + '.evidence', True)
            if not isinstance(item.get('review_status'), str) or item['review_status'] not in DECISION_STATES:
                note('ERROR', where, 'Override requires an explicit review_status.')
            elif item['review_status'] in {'UNDETERMINED', 'OBSERVED_FAIL'}:
                note('INCOMPLETE', where, 'Override review is pending or has an unresolved failure.')

    for role_id, role in roles.items():
        if role_id not in declared:
            note('ERROR', 'roles.' + role_id, 'Undeclared role cannot introduce a new style branch.')
        if not isinstance(role, dict) or role.get('inherits') != 'project_theme':
            note('ERROR', 'roles.' + role_id, 'Each role must inherit project_theme explicitly.')
            continue
        overrides(role.get('overrides', []), f'roles.{role_id}.overrides')
    for role_id in declared:
        if role_id not in roles:
            note('ERROR', 'roles.' + role_id, 'Declared role is missing its inheritance definition.')

    assets = data.get('assets', [])
    if not isinstance(assets, list):
        note('ERROR', 'assets', 'Assets must be a list.')
        assets = []
    if not assets:
        note('INCOMPLETE', 'assets', 'No actual assets have been bound to the theme.')
    asset_files = {a.get('file') for a in assets if isinstance(a, dict) and isinstance(a.get('file'), str)}
    exceptions = data.get('exceptions', [])
    if not isinstance(exceptions, list):
        note('ERROR', 'exceptions', 'Exceptions must be a list.')
        exceptions = []
    exceptions_by_id = {}
    for i, exception in enumerate(exceptions):
        where = f'exceptions[{i}]'
        if not isinstance(exception, dict) or not isinstance(exception.get('id'), str) or not exception.get('id'):
            note('ERROR', where, 'Each exception needs a nonempty ID.')
            continue
        if exception['id'] in exceptions_by_id:
            note('ERROR', where, 'Duplicate exception ID.')
        exceptions_by_id[exception['id']] = exception
        if not isinstance(exception.get('reason'), str) or not exception['reason'].strip():
            note('ERROR', where, 'An exception needs a concrete reason, not an implicit waiver.')
        evidence(exception.get('evidence'), where + '.evidence', True)
        scope = exception.get('scope', {})
        if not isinstance(scope, dict) or not (scope.get('asset_files') or scope.get('role_ids')):
            note('ERROR', where, 'Exception needs a bounded asset or role scope.')
        elif not all(isinstance(scope.get(k, []), list) and all(isinstance(x, str) for x in scope.get(k, [])) for k in ('asset_files', 'role_ids')):
            note('ERROR', where, 'Exception scope must contain lists of asset paths and role IDs.')
        else:
            if any(x not in asset_files for x in scope.get('asset_files', [])):
                note('ERROR', where, 'Exception names an asset absent from this contract.')
            if any(x not in declared for x in scope.get('role_ids', [])):
                note('ERROR', where, 'Exception names an undeclared role.')
        overrides(exception.get('overrides', []), where + '.overrides')
        if not isinstance(exception.get('review_status'), str) or exception['review_status'] not in DECISION_STATES:
            note('ERROR', where, 'Exception requires an explicit review_status.')
        if not exception.get('production_limit'):
            note('INCOMPLETE', where, 'State the exception limit; it must not waive unrelated production gates.')

    seen_files = set()
    for i, asset in enumerate(assets):
        where = f'assets[{i}]'
        if not isinstance(asset, dict):
            note('ERROR', where, 'Asset entry must be an object.')
            continue
        if set(asset) - ASSET_FIELDS:
            note('ERROR', where, 'Inline asset style/override fields are unsupported; use a scoped exception.')
        filename = asset.get('file')
        if not isinstance(filename, str) or not filename or Path(filename).is_absolute() or '..' in Path(filename).parts:
            note('ERROR', where, 'Asset file must stay inside the contract directory.')
        elif filename in seen_files:
            note('ERROR', where, 'Duplicate asset binding.')
        else:
            seen_files.add(filename)
            evidence([{'path': filename, 'sha256': asset.get('sha256')}], where + '.file')
        if theme_id and asset.get('theme_id') != theme_id:
            note('ERROR', where, 'Asset theme_id differs from the project theme; per-asset reselection is forbidden.')
        elif not theme_id or not asset.get('theme_id'):
            note('INCOMPLETE', where, 'Asset theme binding is unspecified.')
        if asset.get('role_id') not in declared or asset.get('role_id') not in roles:
            note('ERROR', where, 'Asset role must resolve to a declared inherited role.')
        if not isinstance(asset.get('sha256'), str) or not re.fullmatch('[a-f0-9]{64}', asset['sha256']):
            note('INCOMPLETE', where, 'Bind the reviewed source with a SHA-256 hash.')
        ids = asset.get('exception_ids', [])
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
            note('ERROR', where, 'exception_ids must be a list of strings.')
            continue
        for ident in ids:
            exception = exceptions_by_id.get(ident)
            if not exception:
                note('ERROR', where, 'Unresolved asset exception: ' + str(ident))
            else:
                scope = exception.get('scope', {})
                scope = scope if isinstance(scope, dict) else {}
                scoped_assets = scope.get('asset_files') if isinstance(scope.get('asset_files'), list) else []
                scoped_roles = scope.get('role_ids') if isinstance(scope.get('role_ids'), list) else []
                if filename not in scoped_assets and asset.get('role_id') not in scoped_roles:
                    note('ERROR', where, 'Exception does not cover this asset or its role.')

    matrix = data.get('review_matrix', [])
    if not isinstance(matrix, list) or not matrix:
        note('INCOMPLETE', 'review_matrix', 'No review evidence is recorded.')
        matrix = []
    for i, review in enumerate(matrix):
        where = f'review_matrix[{i}]'
        if not isinstance(review, dict):
            note('ERROR', where, 'Review entry must be an object.')
            continue
        for key in ('id', 'category', 'subject', 'method', 'expected', 'observed'):
            if unknown(review.get(key)):
                note('INCOMPLETE', where + '.' + key, 'Review record is unfinished.')
        status = review.get('status')
        if not isinstance(status, str) or status not in REVIEW_STATES:
            note('ERROR', where, 'Review status is invalid.')
        elif status == 'UNDETERMINED':
            note('INCOMPLETE', where, 'Review remains unverified.')
        evidence(review.get('evidence'), where + '.evidence', status in {'OBSERVED_PASS', 'OBSERVED_FAIL'})
        if review.get('exception') and (not isinstance(review['exception'], str) or review['exception'] not in exceptions_by_id):
            note('ERROR', where, 'Review exception reference does not resolve.')
        # An exception records scope; it never erases an explicitly failed gate.
        if status == 'OBSERVED_FAIL' and review.get('category') in {'technical', 'strict-pixel-production'}:
            hard_failures.append({'id': review.get('id'), 'subject': review.get('subject'), 'exception': review.get('exception')})

    overall = data.get('overall', {})
    if not isinstance(overall, dict):
        note('ERROR', 'overall', 'Overall status must be an object.')
        overall = {}
    for field in ('visual_status', 'runtime_status'):
        if not isinstance(overall.get(field), str) or overall[field] not in {'OBSERVED_PASS', 'NOT_APPLICABLE'}:
            note('INCOMPLETE', 'overall.' + field, 'No complete recorded acceptance for this evidence layer.')
    bridge = data.get('technical_audit_bridge', {})
    if not isinstance(bridge, dict):
        note('ERROR', 'technical_audit_bridge', 'Audit bridge must be an object.')
        bridge = {}
    pixel_status = bridge.get('strict_pixel_production_status', 'UNDETERMINED')
    if not isinstance(pixel_status, str) or pixel_status not in REVIEW_STATES:
        note('ERROR', 'technical_audit_bridge.strict_pixel_production_status', 'Invalid recorded production status.')
    if pixel_status == 'UNDETERMINED':
        note('INCOMPLETE', 'technical_audit_bridge.strict_pixel_production_status', 'Pixel production remains unverified.')
    if pixel_status == 'OBSERVED_FAIL' and not hard_failures:
        hard_failures.append({'id': 'declared-production-failure', 'subject': 'strict-pixel-production', 'exception': None})
    structure = 'FAIL' if any(f['level'] == 'ERROR' for f in findings) else 'PASS'
    incomplete = any(f['level'] == 'INCOMPLETE' for f in findings)
    failed = structure == 'FAIL' or bool(hard_failures)
    return {
        'validation_status': 'FAIL' if failed else 'INCOMPLETE' if incomplete else 'PASS',
        'structure_status': structure,
        'completion_status': 'INCOMPLETE' if incomplete else 'COMPLETE',
        'theme_id': theme_id,
        'asset_count': len(assets),
        'recorded_visual_status': overall.get('visual_status', 'UNDETERMINED'),
        'recorded_runtime_status': overall.get('runtime_status', 'UNDETERMINED'),
        'recorded_strict_pixel_production_status': pixel_status,
        'recorded_hard_gate_failures': hard_failures,
        'findings': findings,
        'boundary': 'This validates structure, references, file hashes and recorded states. It does not inspect image pixels, infer style quality or perform runtime/user testing.',
    }, 1 if failed else 2 if incomplete else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract', help='Path to theme-contract.json')
    parser.add_argument('--json', action='store_true', help='JSON is also the default output format')
    args = parser.parse_args()
    report, code = validate(args.contract)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
