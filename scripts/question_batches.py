"""Load only batches explicitly reviewed and registered for the release build."""
import importlib
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
        if not re.fullmatch(r'question_batch\d{2}(?:_[a-z0-9]+)?',name) or name in seen:
            raise ValueError('题包批次名称无效或重复：'+str(name))
        seen.add(name)
        module=importlib.import_module(name)
        result.append({'module':name,'name':entry['name'],'packs':module.PACKS,'sources':module.SOURCES})
    return result


def additions():
    batches=load_batches()
    return ([p for b in batches for p in b['packs']],
            [s for b in batches for s in b['sources']])
