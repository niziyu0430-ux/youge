"""Inventory authored question progress separately from searchable catalogue size."""
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
RESEARCH = ROOT / 'research/question-design-v0.5'


def fingerprint(items, title):
    visible = [{'text':q['text'].replace(title,'{game}'),
                'options':[o['label'].replace(title,'{game}') for o in q['options']]}
               for q in items if q['scope']=='anchor']
    return hashlib.sha256(json.dumps(visible,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def audit():
    from youge import v04,v05
    draft_path = ROOT / 'config/question-packs.v0.5.draft.json'
    draft = json.loads(draft_path.read_text(encoding='utf-8')) if draft_path.exists() else {'packs':[]}
    drafts = {g:pack for pack in draft['packs'] for g in pack['game_ids']}
    active_path=ROOT/'config/question-packs.v0.5.0.json'
    active=json.loads(active_path.read_text(encoding='utf-8')) if active_path.exists() else {'packs':[]}
    released={g:p for p in active['packs'] for g in p['game_ids']}
    rows = []
    for game in v04.catalog()['games']:
        pack = drafts.get(game['id'])
        live=released.get(game['id'])
        has_pack = game.get('question_pack') in v04.config()['packs']
        rows.append({'game_id':game['id'],'title':game['title'],
                     'live_basis':'authored_game_pack' if live else 'partly_custom_legacy_pack' if has_pack else 'generic_mechanic_template',
                     'live_mechanic_family':None if live else game['mechanic_family'],
                     'live_question_pack':live['id'] if live else game.get('question_pack'),
                     'legacy_mechanic_family':game['mechanic_family'],
                     'legacy_question_pack':game.get('question_pack'),
                     'live_anchor_fingerprint':fingerprint(v05.questions(game['id'])['questions'] if live else v04.questionnaire(game['id']),game['title']),
                     'new_design_status':live['status'] if live else pack['status'] if pack else 'not_authored',
                     'new_pack_id':live['id'] if live else pack['id'] if pack else None,
                     'new_dedicated_item_count':len(live['slots']) if live else len(pack['questions']) if pack else 0,
                     'player_review':live['player_trial'] if live else 'pending','released':bool(live),
                     'active_pack_version':live['version'] if live else None})
    persona_ids={p['id'] for p in v04.config()['personas']}
    shared={p for q in draft.get('shared_questions',[]) for o in q['options'] for p in o['weights']}
    draft_reviews=[]
    for pack in draft['packs']:
        exposure=Counter(o['proposed_signal'] for q in pack['questions'] for o in q['options'] if o['proposed_signal'] in persona_ids)
        gated=[q for q in pack['questions'] if q['requires_experience']]
        draft_reviews.append({'pack_id':pack['id'],'title':pack['title'],
                              'item_count':len(pack['questions']),
                              'proposed_persona_option_opportunities':dict(exposure),
                              'persona_ids_supported_only_by_shared_questions':sorted(shared-set(exposure)),
                              'experience_gated_items':len(gated),
                              'items_missing_alternative':[q['id'] for q in gated if not q['alternatives']],
                              'written_alternative_count':sum(len(q['alternatives']) for q in pack['questions']),
                              'release_blockers':[] if pack['game_ids'][0] in released else ['unreviewed_question_meanings_and_scoring',
                                                 'incomplete_mode_or_progress_replacement_paths',
                                                 'new_report_contract_and_answer_version_not_implemented'],
                              'quality_status':'released_exploratory_player_trial_pending' if pack['game_ids'][0] in released else 'needs_review_not_proven_by_schema_tests'})
    return {'checked_at':datetime.now(timezone(timedelta(hours=8))).date().isoformat(),'catalogue_version':v04.catalog()['version'],
            'catalogue_count':len(rows),'target_dedicated_questions_per_game':12,
            'shared_question_count':4,'max_extra':2,
            'live_basis_counts':dict(Counter(r['live_basis'] for r in rows)),
            'new_status_counts':dict(Counter(r['new_design_status'] for r in rows)),
            'new_draft_item_count':sum(len(p['questions']) for p in draft['packs']),
            'released_new_game_count':len(released),
            'released_pack_count':len(active['packs']),
            'released_base_slot_count':sum(len(p['slots']) for p in active['packs']),
            'released_scene_count':sum(len(s['variants']) for p in active['packs'] for s in p['slots']),
            'draft_reviews':draft_reviews,'games':rows}


def main():
    result = audit()
    RESEARCH.mkdir(exist_ok=True,parents=True)
    (RESEARCH/'coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('games','draft_reviews')},ensure_ascii=False))


if __name__=='__main__':
    main()
