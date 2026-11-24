"""Route forms and saved responses to their original instrument version."""
from copy import deepcopy
from .engine import InputError
from . import v04,v05


def bootstrap():
    data=v04.bootstrap()
    data['authored_packs']=[v05.descriptor(p) for p in v05.bank()['packs']]
    data['question_release']=v05.bank()['version']
    data['rules']['compatible_versions']=[
        v04.config()['versions']|{'report_rules':v} for v in v04.config()['compatible_report_versions']
    ]+[deepcopy(v05.VERSIONS)]
    return data


def questions(game_id=None,raw=None,instrument=None,mode_id=None):
    if raw is not None:
        if not isinstance(raw,dict):raise InputError('请提供一份有效的答卷。')
        if not isinstance(raw.get('versions'),dict):raise InputError('答卷缺少题库版本。')
        instrument=raw['versions'].get('instrument')
        game_id=raw.get('game_id')
    elif isinstance(game_id,str) and game_id in v04.catalog().get('search_redirects', {}):
        raise InputError('请在作品库搜索并选择你玩过的具体作品。')
    if instrument=='0.5.0' or (instrument is None and v05.pack_for(game_id)):
        return v05.questions(game_id,raw,mode_id)
    if instrument not in (None,'0.4.0'):raise InputError('这份答卷的题库版本暂不支持。')
    response=v04.normalize(raw) if raw is not None else None
    return {'game':v04.find_game(game_id),'questions':[v04.public_question(q) for q in v04.questionnaire(game_id)],
            'versions':deepcopy(v04.config()['versions']),'response':response}


def report(raw):
    if not isinstance(raw,dict) or not isinstance(raw.get('versions'),dict):raise InputError('答卷缺少题库版本。')
    version=raw['versions'].get('instrument')
    if version=='0.4.0':return v04.report(raw)
    if version=='0.5.0':return v05.report(raw)
    raise InputError('这份答卷的题库版本暂不支持。')


def compare(left,right):
    def instrument(raw):
        versions=raw.get('versions') if isinstance(raw,dict) else None
        return versions.get('instrument') if isinstance(versions,dict) else None
    if instrument(left)==instrument(right)=='0.4.0':
        return v04.compare(left,right)
    a,b=report(left),report(right)
    if not a['complete'] or not b['complete']:raise InputError('请先完成两份答卷的补问。')
    a,b=a['report'],b['report'];rows=[]
    la={r['topic']:r for r in a['advice']};ra={r['topic']:r for r in b['advice']}
    for topic in dict.fromkeys([*la,*ra]):
        l,r=la.get(topic),ra.get(topic)
        if l and r:
            def semantic(row,result):
                if 'semantic_key' in row:return row['semantic_key']
                return result['response']['answers'].get('X14') if topic=='coop' else None
            lv,rv=semantic(l,a),semantic(r,b)
            lk=l.get('comparability_key','shared:X14:v04' if topic=='coop' else None)
            rk=r.get('comparability_key','shared:X14:v04' if topic=='coop' else None)
            status=('已有共同选择' if lv is not None and lv==rv else '需要协调') if lk is not None and lk==rk else '先聊一聊'
        else:status='先聊一聊'
        title=(l or r)['title']
        empty={'text':'这份题包没有问到同一情境，可以先聊聊各自的实际习惯。'}
        rows.append({'topic':topic,'title':title,'status':status,'left':l or empty,'right':r or empty})
    same=a['game']['id']==b['game']['id']
    return {'versions':deepcopy(v05.VERSIONS),'contains_fictional':a['fictional'] or b['fictional'],
            'left':a,'right':b,'same_game':same,'common_game':a['game'] if same else None,
            'coordination':rows,'note':'只对照实际回答的情境；没有对应问题时先交流，不推断一致或冲突，也不换算契合度。'}
