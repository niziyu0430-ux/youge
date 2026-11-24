"""Record already completed source, runtime, history and browser acceptance.

This only reconciles evidence; it never authors, registers or builds a pack.
"""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--previous', required=True)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--ui-tag', required=True)
    parser.add_argument('--module', action='append', required=True)
    parser.add_argument('--parent', action='append', required=True)
    parser.add_argument('--neutral-probe')
    args = parser.parse_args()
    assert re.fullmatch(r'[a-z0-9-]+', args.tag)
    assert re.fullmatch(r'[a-z0-9]+', args.ui_tag)
    assert len(args.module) == len(args.parent)
    previous = read(args.previous)
    runtime_path = f'reports/question-through-{args.tag}-runtime-checks.json'
    history_path = f'reports/question-{args.tag}-history-checks.json'
    tests_path = f'reports/question-through-{args.tag}-tests.log'
    ui_path = f'output/playwright/question-{args.ui_tag}-validation.json'
    runtime, history, ui = read(runtime_path), read(history_path), read(ui_path)
    bank = read('config/question-packs.v0.5.0.json')
    bank_sha = hashlib.sha256((ROOT / 'config/question-packs.v0.5.0.json').read_bytes()).hexdigest()
    assert runtime['passed'] and runtime['runtime_sha256'] == bank_sha == ui['bank_sha256']
    assert history['passed'] and not history['changed_pack_ids']
    assert ui['status'] == 'all_browser_paths_and_mobile_visual_review_accepted'
    assert ui['full_authored_path_checks'] and ui['progress']['next'] == len(ui['cases'])
    assert all(r['passed'] for r in ui['progress']['results'])
    tests = (ROOT / tests_path).read_text(encoding='utf-8')
    tested = re.search(r'Ran (\d+) tests in ([\d.]+)s', tests)
    assert tested and tests.rstrip().endswith('OK')
    versions = {p['id']: p['version'] for p in bank['packs']}
    for module_name, parent_path in zip(args.module, args.parent):
        assert re.fullmatch(r'question_batch\d{2,}(?:_[a-z0-9]+)?', module_name)
        module = importlib.import_module(module_name)
        parent = read(parent_path)
        source_sha = hashlib.sha256((ROOT / 'scripts' / (module_name + '.py')).read_bytes()).hexdigest()
        assert parent['source_sha256'] == source_sha
        assert parent['accepted_packs'] == module.PACKS and parent['accepted_sources'] == module.SOURCES
        assert all(any(p['pack_id'] == item['id'] for p in ui['pack_versions']) for item in module.PACKS)
    queue = read('research/question-design-v0.5/rewrite-queue.json')
    counts = {k: queue[k] for k in previous['counts']}
    assert counts['runtime_pack_count'] == runtime['packs'] == len(bank['packs'])
    assert counts['complete_published_count'] == runtime['game_records']
    report = previous.copy()
    reports = previous['browser']['reports'] + [ui_path]
    actual_routes = []
    for path in reports:
        for row in read(path)['progress']['results']:
            assert row['passed'] and row['packVersion'] == versions[row['packId']], (path, row['packId'])
            actual_routes.append(row)
    browser = {
        'new_full_authored_routes_passed': len(ui['progress']['results']),
        'new_dedicated_questions_with_requested_branch_verified': sum(map(len, ui['full_path_targets'])),
        'earlier_current_version_routes_passed': len(actual_routes) - len(ui['progress']['results']),
        'total_targeted_runs': len(actual_routes),
        'distinct_game_mode_pairs': len({(r['gameId'], r['mode']) for r in actual_routes}),
        'all_targeted_pack_versions_match_current_bank': True,
        'reports': reports,
        'new_mobile_visuals': len(ui['mobile_visual_review']['images']),
        'total_mobile_visuals': previous['browser']['total_mobile_visuals'] + len(ui['mobile_visual_review']['images']),
    }
    report.update(
        status=f'released_round_{runtime["game_records"]}_source_runtime_history_and_targeted_browser_verified',
        goal_complete=False, runtime_bank_sha256=bank_sha, counts=counts,
        runtime_verification=runtime_path, actual_current_forms_and_reports=runtime['actual_reports_verified'],
        latest_history={'pairs': history['historical_form_and_report_pairs'], 'report': history_path,
                        'all_previous_current_pack_versions_preserved': True},
        unit_tests={'passed': int(tested[1]), 'seconds': float(tested[2]), 'log': tests_path},
        browser=browser, parent_editorial_acceptance=args.parent,
        qualification=f'All{runtime["game_records"]} authored records passed source/runtime acceptance. New UI paths cover all12 chosen branches. Full library scope remains active; no human trial or psychometric validity established.',
    )
    if args.neutral_probe:
        probe = read(args.neutral_probe)
        assert probe['status'] == 'passed' and probe['bank_sha256'] == bank_sha
        report['new_neutral_behavior_probe'] = args.neutral_probe
    output = f'reports/question-through-{args.tag}-acceptance.json'
    save(output, report)
    active = read('research/question-design-v0.5/active-rewrite-run.json')
    active.update(latest_release=report, latest_acceptance_report=output,
                  latest_runtime_bank_sha256=bank_sha, latest_verified_counts=counts)
    active['parent_accepted_unbuilt_modules'] = [m for m in active['parent_accepted_unbuilt_modules'] if m not in args.module]
    for row in active['new_authoring_assignments']:
        if row['module'] in args.module:
            row['state'] = 'released_editorial_runtime_history_and_browser_verified'
    save('research/question-design-v0.5/active-rewrite-run.json', active)
    print(json.dumps({'counts': counts, 'browser_runs': browser['total_targeted_runs'], 'goal_complete': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
