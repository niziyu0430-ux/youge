"""Small serializer for explicitly written scenes; never creates prose from game titles."""
from collections import Counter

SIGNALS=dict(zip('w s r p t k f b y g c a i o q h'.split(),[
    'wanderer','story_keeper','role_player','puzzle_breaker','practice_seeker','rank_worker',
    'feedback_engine','build_alchemist','systems_builder','growth_keeper','collector',
    'style_director','play_inventor','social_spark','quest_board','cozy_resident']))


def question(number,scene,text,labels,signals,purpose,sources,alternative,boundary=''):
    """Both scenes and all eight choices must be written by the editor."""
    labels=labels.split('|');signals=[SIGNALS.get(s,s) for s in signals.split()]
    alt_text,alt_labels=alternative[:2];alt_labels=alt_labels.split('|')
    alt_signals=[SIGNALS.get(s,s) for s in alternative[2].split()] if len(alternative)==3 else signals
    assert 2 <= len(labels) <= 4 and len(labels)==len(signals)
    assert 2 <= len(alt_labels) <= 4 and len(alt_labels)==len(alt_signals)
    assert len(set(labels))==len(labels) and len(set(alt_labels))==len(alt_labels)
    def variant(key,title,words,scene_name,assigned):
        pairs=list(zip(words,assigned))
        # Rotate authored pairs together so a recurring motive is not always A.
        offset=(number-1)%len(pairs)
        pairs=pairs[offset:]+pairs[:offset]
        return {'key':key,'text':title,'scene':scene_name,
                'question_type':'situational_action' if number<=8 else 'experience_reflection',
                'source_ids':sources.split(),'modes':[],
                'options':[{'id':chr(65+i),'label':label,'signal':signal}
                           for i,(label,signal) in enumerate(pairs)],
                'design_purpose':purpose,
                'interpretation_boundary':boundary or '只解释这次情境的偏好；不由效率、胜负或未体验推断能力与现实人格。'}
    return {'number':number,'scene':scene,'variants':[
        variant('V1',text,labels,scene,signals),variant('ALT1',alt_text,alt_labels,scene+'的另一情境',alt_signals)]}


def pack(identifier,title,game_ids,scope,questions,notes=()):
    assert len(questions)==12 and [q['number'] for q in questions]==list(range(1,13))
    slots=[]
    for q in questions:
        slot_id=identifier.upper()+f'{q["number"]:02d}'
        variants=[]
        for v in q['variants']:
            variants.append({k:value for k,value in v.items() if k!='key'}|{'id':slot_id+'.'+v['key']})
        slots.append({'id':slot_id,'number':q['number'],'variants':variants})
    return {'id':identifier,'title':title,'game_ids':game_ids,'scope':scope,
            'author_review':'source_checked_and_editorially_revised','player_trial':'not_performed',
            'status':'released_exploratory','editorial_notes':list(notes),
            'modes':[{'id':'default','label':scope,'initial_variants':{}}],'slots':slots}


def source(identifier,title,url,kind,supports,limits='不用于证明人格信号；不采用易变价格、伤害或数量。'):
    return {'id':identifier,'title':title,'url':url,'kind':kind,'checked_at':'2026-10-30',
            'supports':supports.split('|'),'limits':limits}


def validate(packs,sources,known_signals):
    source_ids=[s['id'] for s in sources]
    assert len(set(source_ids))==len(source_ids),'重复资料ID'
    ids=[];games=[]
    for p in packs:
        games+=p['game_ids'];ids.append(p['id'])
        assert len(p['slots'])==12
        for slot in p['slots']:
            assert len(slot['variants'])>=2
            for v in slot['variants']:
                ids.append(v['id'])
                assert v['source_ids'] and set(v['source_ids'])<=set(source_ids)
                assert all(o['signal'] in known_signals for o in v['options'])
                assert 2 <= len(v['options']) <= 4
                assert [o['id'] for o in v['options']]==list('ABCD'[:len(v['options'])])
                assert len({o['label'] for o in v['options']})==len(v['options'])
                assert v['text'] and '{game}' not in v['text']
                assert v['design_purpose'] and v['interpretation_boundary']
    assert len(set(ids))==len(ids),'重复题包或题目ID'
    assert not [g for g,n in Counter(games).items() if n>1],'同一作品重复发布'
