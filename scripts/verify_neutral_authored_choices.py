"""Check completed reports for every explicit neutral choice in selected packs."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
from youge import questionnaires, v05
from verify_authored_batch import finish


def verify(names):
    copies = v05.bank()['behavior_copy']
    rows, profiles, bindings = [], [], []
    for name in names:
        assert re.fullmatch(r'question_batch\d{2}(?:_[a-z0-9]+)?', name)
        module = importlib.import_module(name)
        for declared in module.PACKS:
            pack = v05.pack_for(declared['game_ids'][0])
            assert {k: v for k, v in pack.items() if k != 'version'} == declared
            bindings.append({'pack_id': pack['id'], 'pack_version': pack['version']})
            for mode in pack['modes']:
                start = questionnaires.questions(pack['game_ids'][0], mode_id=mode['id'])
                available = lambda v: not v['modes'] or mode['id'] in v['modes']
                for slot in pack['slots']:
                    for variant in filter(available, slot['variants']):
                        for option in variant['options']:
                            if option['signal'] not in copies:
                                continue
                            raw = deepcopy(start['response'])
                            raw['fictional'] = True
                            raw['question_variants'][slot['id']] = variant['id']
                            form = questionnaires.questions(raw=raw)
                            raw['answers'] = {q['id']: 'A' for q in form['questions']}
                            raw['answers'][variant['id']] = option['id']
                            report = finish(raw)
                            state = v05.score(report['response'])
                            assert state['complete']
                            selected = next(s for s in state['selected'] if s[0]['id'] == variant['id'])
                            points, _, anchors = v05._points([selected], Counter())
                            assert sum(points.values()) == 0 and not anchors
                            ref = 'answer:' + variant['id']
                            evidence = report['evidence'][ref]
                            assert evidence['question'] == variant['text']
                            assert evidence['label'] == option['label']
                            assert evidence['signal'] == option['signal']
                            assert evidence['pack_version'] == pack['version']
                            copy = copies[option['signal']]
                            assert any(a['rule_id'] == 'V05_EXPLICIT_BEHAVIOR' and
                                       ref in a['evidence_refs'] and a['text'] == copy['text']
                                       for a in report['advice'])
                            assert any(ref in b['evidence_refs'] and b['text'] == copy['tag']
                                       for b in report['behavior_tags'])
                            rows.append({'pack_id': pack['id'], 'mode': mode['id'],
                                         'variant_id': variant['id'], 'option_id': option['id'],
                                         'signal': option['signal'], 'isolated_anchor_persona_points': 0,
                                         'proper_text_tag_and_exact_evidence': True, 'passed': True})
                raw = deepcopy(start['response'])
                raw['fictional'] = True
                choices = []
                for slot in pack['slots']:
                    variants = [v for v in slot['variants'] if available(v)]
                    variant = next((v for v in variants if v['id'].endswith('.ALT1')), None)
                    option = next((o for o in variant['options'] if o['signal'] in copies), None) if variant else None
                    if option is None:
                        break
                    raw['question_variants'][slot['id']] = variant['id']
                    choices.append({'variant_id': variant['id'], 'option_id': option['id'], 'signal': option['signal']})
                if len(choices) == 12:
                    form = questionnaires.questions(raw=raw)
                    raw['answers'] = {q['id']: 'A' for q in form['questions']}
                    raw['answers'].update({c['variant_id']: c['option_id'] for c in choices})
                    report = finish(raw)
                    assert not report['audit']['anchor_support_count']
                    advice = [a for a in report['advice'] if a['rule_id'] == 'V05_EXPLICIT_BEHAVIOR']
                    assert len(advice) == 12 and 16 <= report['question_count'] <= 18
                    profiles.append({'pack_id': pack['id'], 'mode': mode['id'], 'choices': choices,
                                     'anchor_persona_points': 0, 'behavior_advice_count': 12,
                                     'question_count': report['question_count'], 'passed': True})
    assert rows
    return {'status': 'passed', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
            'modules': names, 'pack_versions': bindings,
            'bank_sha256': hashlib.sha256((ROOT / 'config/question-packs.v0.5.0.json').read_bytes()).hexdigest(),
            'checked_actual_neutral_choices': len(rows),
            'signal_counts': dict(Counter(r['signal'] for r in rows)), 'rows': rows,
            'all12_alternative_neutral_profiles': profiles, 'human_player_trial': False,
            'qualification': 'Synthetic completed reports: exact evidence, neutral copy and zero isolated persona points. Manual review must separately assess whether each choice fits that copy. Not a human trial or psychometric validity.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('modules', nargs='+')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    target = (ROOT / args.output).resolve()
    assert target.is_relative_to((ROOT / 'reports').resolve())
    assert not target.exists(), 'Keep the original completed verification evidence.'
    result = verify(args.modules)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'neutral_choices': result['checked_actual_neutral_choices'],
                      'all12_neutral_profiles': len(result['all12_alternative_neutral_profiles']),
                      'bank_sha256': result['bank_sha256']}))


if __name__ == '__main__':
    main()
