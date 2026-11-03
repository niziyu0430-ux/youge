"""Find dedicated scenes whose choices cannot contribute persona points."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def audit():
    bank_path = ROOT / 'config/question-packs.v0.5.0.json'
    bank = read(bank_path)
    personas = {p['id'] for p in read(ROOT / 'config/youge.v0.4.0.json')['personas']}
    rows = []
    for pack in bank['packs']:
        for mode in pack['modes']:
            for slot in pack['slots']:
                variants = [v for v in slot['variants']
                            if not v.get('modes') or mode['id'] in v['modes']]
                if not variants:
                    raise ValueError(f"No scene: {pack['id']} / {mode['id']} / {slot['id']}")
                initial = mode.get('initial_variants', {}).get(slot['id'], variants[0]['id'])
                if initial not in {v['id'] for v in variants}:
                    raise ValueError(f'Invalid initial scene: {initial}')
                unscored = [v['id'] for v in variants
                            if not any(o.get('signal') in personas for o in v['options'])]
                if unscored:
                    rows.append({'pack_id': pack['id'], 'mode': mode['id'], 'slot': slot['id'],
                                 'initial_unscored': initial in unscored,
                                 'unscored_scenes': unscored,
                                 'all_scenes_unscored': len(unscored) == len(variants)})
    return {'at_utc': datetime.now(timezone.utc).isoformat(),
            'bank_sha256': hashlib.sha256(bank_path.read_bytes()).hexdigest(),
            'definition': 'No option contributes persona points; behavior observations can still appear in reports. Structural presence does not establish the validity of a signal.',
            'mode_slots_with_any_unscored_scene': len(rows),
            'mode_slots_with_unscored_initial': sum(r['initial_unscored'] for r in rows),
            'mode_slots_all_scenes_unscored': sum(r['all_scenes_unscored'] for r in rows),
            'affected_packs': len({r['pack_id'] for r in rows}), 'rows': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to((ROOT / 'reports').resolve()):
        raise ValueError('Output must be inside reports')
    result = audit()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, ensure_ascii=False))
