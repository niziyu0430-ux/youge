"""Load only batches explicitly reviewed and registered for the release build."""
import importlib
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))


def load_batches():
    manifest=json.loads((ROOT/'config/question-authoring-batches.json').read_text(encoding='utf-8'))
    seen=set();result=[]
    for entry in manifest['batches']:
        name=entry['module']
        if not re.fullmatch(r'question_batch\d{2,}(?:_[a-z0-9]+)?',name) or name in seen:
            raise ValueError('题包批次名称无效或重复：'+str(name))
        seen.add(name)
        module=importlib.import_module(name)
        result.append({'module':name,'name':entry['name'],'packs':module.PACKS,'sources':module.SOURCES})
    return result


def additions():
    batches=load_batches()
    return ([p for b in batches for p in b['packs']],
            [s for b in batches for s in b['sources']])


def pack_version(pack):
    data = json.dumps(pack, ensure_ascii=False, sort_keys=True).encode()
    return '0.5.0+' + hashlib.sha256(data).hexdigest()[:12]


def apply_replacement_expansions(packs, sources, *, allow_missing=False):
    """Apply registered, version-bound additions to the authored source data."""
    manifest = json.loads((ROOT / 'config/question-authoring-batches.json').read_text(encoding='utf-8'))
    filenames = manifest.get('replacement_expansions', [])
    if len(filenames) != len(set(filenames)):
        raise ValueError('替换题追加文件重复')
    by_id = {pack['id']: pack for pack in packs}
    known_sources = {source['id'] for source in sources}
    known_questions = {v['id'] for pack in packs for slot in pack['slots'] for v in slot['variants']}
    for name in filenames:
        if not re.fullmatch(r'question_[a-z0-9_]+_extra_v05\.json', name):
            raise ValueError(f'无效的替换题追加文件：{name}')
        expansion = json.loads((ROOT / 'scripts' / name).read_text(encoding='utf-8'))
        pack = by_id.get(expansion['pack_id'])
        # The verifier can be invoked for a single batch that excludes this pack.
        if pack is None:
            if allow_missing:
                continue
            raise ValueError(f'找不到替换题追加文件所对应的题包：{name}')
        if pack_version(pack) != expansion['base_pack_version']:
            raise ValueError(f'替换题追加文件的基础版本已变化：{name}')
        for source in expansion['SOURCES']:
            if source['id'] in known_sources:
                raise ValueError(f"重复的替换题来源编号：{source['id']}")
            sources.append(source)
            known_sources.add(source['id'])
        slots = {slot['id']: slot for slot in pack['slots']}
        for record in expansion['additions']:
            variant = record['append_variant']
            if variant['id'] in known_questions or not set(variant['source_ids']) <= known_sources:
                raise ValueError(f"替换题编号重复或来源缺失：{variant['id']}")
            slots[record['slot_id']]['variants'].append(variant)
            known_questions.add(variant['id'])
        modes = {mode['id'] for mode in pack['modes']}
        for mode in expansion.get('append_modes', []):
            if mode['id'] in modes:
                raise ValueError(f"重复的玩法编号：{mode['id']}")
            for slot_id, slot in slots.items():
                eligible = {variant['id'] for variant in slot['variants'] if mode['id'] in variant.get('modes', [])}
                if len(eligible) < 3 or mode['initial_variants'].get(slot_id) not in eligible:
                    raise ValueError(f"新玩法缺少首题或替代题：{mode['id']} / {slot_id}")
            pack['modes'].append(mode)
            modes.add(mode['id'])
