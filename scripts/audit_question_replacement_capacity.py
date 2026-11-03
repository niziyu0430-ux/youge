"""Measure real same-slot replacement capacity; never creates question content."""
from copy import deepcopy
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from youge import v05
from youge.engine import InputError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='reports/question-replacement-capacity-20261031.json',
                        help='Workspace-relative report path; use a new path to retain a prior audit.')
    args = parser.parse_args()
    path = ROOT / 'config/question-packs.v0.5.0.json'
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    bank = v05.bank()
    rows = []
    failures = []
    for pack in bank['packs']:
        for mode in pack['modes']:
            initial = v05.questions(pack['game_ids'][0], mode_id=mode['id'])
            for index, slot in enumerate(pack['slots']):
                available = [v for v in slot['variants']
                             if not v.get('modes') or mode['id'] in v['modes']]
                form = deepcopy(initial)
                shown = [form['questions'][index]['id']]
                for _ in range(2):
                    current = form['questions'][index]
                    if not current['can_replace']:
                        break
                    form = v05.replace_question(form['response'], current['id'])
                    shown.append(form['questions'][index]['id'])
                checks = {
                    'sixteen_questions': len(form['questions']) == 16,
                    'no_unexperienced_answer_added': form['response']['answers'] == {},
                    'no_extra_answer_added': form['response']['extra_answers'] == [],
                    'shown_ids_never_repeated': len(shown) == len(set(shown)),
                    'same_slot': form['questions'][index]['slot_id'] == slot['id'],
                    'all_options_valid': all(2 <= len(q['options']) <= 4 for q in form['questions']),
                }
                if not all(checks.values()):
                    failures.append({'pack_id': pack['id'], 'mode_id': mode['id'],
                                     'slot_id': slot['id'], 'checks': checks})
                rows.append({'pack_id': pack['id'], 'pack_version': pack['version'],
                             'game_ids': pack['game_ids'], 'mode_id': mode['id'],
                             'slot_id': slot['id'], 'available_variant_count': len(available),
                             'actual_shown_ids': shown,
                             'can_show_a_third_verified_pack_variant': len(shown) == 3,
                             'remaining_after_third': max(0, len(available) - 3),
                             'invariants': checks})
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    shortage = [r for r in rows if not r['can_show_a_third_verified_pack_variant']]
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'bank_sha256': digest,
        'user_policy': 'Continue with other verified game-specific situations; no skip; 16 plus at most2 extras.',
        'qualification': 'Three variants is only the minimum for rejecting the initial and first alternative and continuing once. It is not unlimited capacity or proof every player can finish. This audit checks actual API mechanics and content counts, not independent gameplay/editorial quality.',
        'status': 'incomplete_second_replacement_coverage' if shortage else 'minimum_third_variant_capacity_present',
        'pack_count': len(bank['packs']),
        'game_count': len({g for p in bank['packs'] for g in p['game_ids']}),
        'mode_slot_count': len(rows),
        'mode_slots_with_at_least_three': len(rows) - len(shortage),
        'mode_slots_needing_more_verified_content': len(shortage),
        'games_needing_more_verified_content': sorted({g for r in shortage for g in r['game_ids']}),
        'runtime_invariant_failures': failures,
        'rows': rows,
        'public_content_or_code_modified': False,
    }
    output = ROOT / args.output
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({k: report[k] for k in ('status','game_count','pack_count','mode_slot_count',
        'mode_slots_with_at_least_three','mode_slots_needing_more_verified_content')}, ensure_ascii=False))
    assert not failures, failures[:2]


if __name__ == '__main__':
    main()
