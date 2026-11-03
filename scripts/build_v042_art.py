"""Copy generated files intact; build the art-edition manifests, never edit pixels."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design/v0.4.2'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = read(DESIGN / 'v1-baseline.json')
    for original in baseline['assets']:
        assert digest(ROOT / original['path']) == original['sha256'], original['id']
    records = read(DESIGN / 'generation-sources.json')['assets']
    for record in records:
        source, target = Path(record['source']), ROOT / record['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert digest(target) == digest(source), f'Refusing to replace {target}'
        else:
            shutil.copyfile(source, target)
        record['sha256'] = digest(target)
    active = {}
    for record in records:
        if record['revision'] >= active.get(record['id'], {}).get('revision', 0):
            active[record['id']] = record
    assert len(active) == 16
    plan = read(DESIGN / 'wardrobe-plan.json')
    plan.update(version='wardrobe-0.4.2', status='generated_for_review')
    plan['rollback']['default_site_art'] = 'v2_with_v1_toggle'
    plan['rollback']['note'] = 'V1原文件完整保留；图鉴和结果页可切换新装V2与原版V1，选择独立于答卷。'
    for persona in plan['assets']:
        persona['status'] = 'generated_for_review'
        if persona['id'] == 'style_director':
            persona['footwear'] = '黑色男式平底便士乐福鞋'
            persona['prop_palette_note'] = '布样扇、手持布料与人台披布统一为紫灰色；保留原道具形状。'
        if persona['id'] == 'practice_seeker':
            persona['detail_note'] = '新增绗缝肩部、护腕、练习珠串、领口织边、补缝与鞋头缝线。'
    save(DESIGN / 'wardrobe-plan.json', plan)
    save(DESIGN / 'portraits-manifest.json', {
        'version': 'wardrobe-0.4.2', 'status': 'complete', 'mode': 'builtin_image_gen',
        'assets': [active[p['id']] for p in plan['assets']],
        'prior_variants': [r for r in records if r is not active[r['id']]],
        'v1_baseline': 'design/v0.4.2/v1-baseline.json',
    })
    save(ROOT / 'web/assets/personas-v2/preview.json', {
        'version': 'wardrobe-0.4.2', 'status': 'complete', 'default_site_art': 'v2',
        'focus_ids': ['story_keeper', 'practice_seeker', 'growth_keeper', 'style_director'],
        'note': '16位V2造型已生成；V1全套原图完整保留。',
        'assets': [dict(p, sample=True, v1=f"/assets/personas/{p['id']}.png", v2='/' + active[p['id']]['path'].removeprefix('web/')) for p in plan['assets']],
    })
    print(f'Art V2: {len(active)} active portraits, {len(records)-len(active)} prior variants; V1 hashes unchanged')


if __name__ == '__main__':
    main()
