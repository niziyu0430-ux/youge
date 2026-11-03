"""Keep every unfinished record visible; a queue entry never counts as authored."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from youge import v05
from question_batches import load_batches
from check_game_question_coverage import input_hashes


def build():
    directory=ROOT/'research/question-design-v0.5'
    audit=json.loads((directory/'per-game-question-audit.json').read_text(encoding='utf-8'))
    assert audit['inputs_sha256']==input_hashes(),'先重新运行逐游戏检查，不能发布过时进度'
    published=[{'game_id':g['game_id'],'title':g['title'],'state':g['status'],
                'scope':'published','current_pack':g['actual_pack'],'next_step':'核对玩法资料并逐款编写12题与替代情境'}
               for g in audit['games'] if not g['has_complete_dedicated_form']]
    candidates=[{'game_id':g['game_id'],'title':g['title'],'state':'candidate_not_authored',
                 'scope':'candidate','current_pack':None,
                 'next_step':'核实中文名或中文社区知名度与收录条件，再核对玩法并编写题包'}
                for g in audit['candidates'] if not g['has_declared_dedicated_pack']]
    queue=published+candidates
    for n,g in enumerate(queue,1):g['order']=n
    batches=[]
    for batch in load_batches():
        name,packs=batch['name'],batch['packs']
        batches.append({'name':name,'pack_ids':[p['id'] for p in packs],
                        'game_ids':[g for p in packs for g in p['game_ids']],
                        'titles':[p['title'] for p in packs],
                        'base_slots':sum(len(p['slots']) for p in packs),
                        'scenes':sum(len(s['variants']) for p in packs for s in p['slots'])})
    bank=v05.bank()
    result={'checked_at':audit['checked_at'],'scope':'all published and candidate records',
            'catalogue_count':audit['published_count'],'complete_published_count':audit['published_count']-len(published),
            'pending_published_count':len(published),'pending_candidate_count':len(candidates),
            'pending_total':len(queue),'runtime_pack_count':len(bank['packs']),
            'runtime_base_slots':sum(len(p['slots']) for p in bank['packs']),
            'runtime_scenes':sum(len(s['variants']) for p in bank['packs'] for s in p['slots']),
            'batches':batches,'queue':queue,
            'limits':'Only runtime non-template authored forms count as complete. Candidate queue entries do not publish games. Player trials remain pending.'}
    (directory/'rewrite-queue.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 游格专属题重写进度','',f'更新日期：{result["checked_at"]}。正式库和候选库的全部未完成记录均列入待办，先完成正式展示的作品。','',
           f'当前正式库{result["catalogue_count"]:,}条中，{result["complete_published_count"]}条接入完整专属题，{len(published):,}条仍待逐款编写。候选库另有{len(candidates):,}条待核实及编写，不因排入待办自动展示。','',
           f'运行库共有{result["runtime_pack_count"]}套作品题包、{result["runtime_base_slots"]}个基础专属题位，含模式与替代题共{result["runtime_scenes"]}个情境。每次仍是12道专属题＋4道跨游戏题，最多2道补问。','',
           '## 本轮已接入','']
    for batch in batches:
        lines.extend(['### '+batch['name'],'',
                      f'{len(batch["pack_ids"])}套作品题包，覆盖{len(batch["game_ids"])}条游戏记录；{batch["base_slots"]}个基础题位，含模式与换题共{batch["scenes"]}个情境。','',
                      '、'.join(batch['titles'])+'。',''])
    lines.extend(['《死亡搁浅》原版与导演剪辑版只共享两版本共同的配送机制题；《骑马与砍杀2》战役和纯战斗分别有12道初始题与12道替代题。《怪物猎人：世界》的单人替代情境不把随从NPC当作真人社交。','',
                  '## 剩余待办与验收','',
                  '- [全部未完成记录及顺序](../research/question-design-v0.5/rewrite-queue.json)。',
                  '- [逐游戏检查清单](游格-逐游戏专属题检查清单.md)。',
                  '- [当前运行的全部题目、选项、设计目的与机制资料](游格-已重写游戏题库.md)。','',
                  '每款先核对真实活动与版本模式，再逐题编写情境、四种可行行动、拟区分动机和解释边界。替代情境也单独写作，不从模板替换游戏名。旧答卷按旧版本保留。题数、版本、换题和计分链路通过后，再更新实际覆盖状态；玩法资料不能证明人格解释或测量效果，真人试测尚未完成。','',
                  '队列只是待办。未编写的作品仍明确标记为通用模板，候选记录仍保留原来的展示门槛。全库待办未归零之前，批次进度不表示任务结束。',''])
    (ROOT/'exports/游格-专属题重写进度.md').write_text('\n'.join(lines),encoding='utf-8')
    refresh_overviews(result,audit)
    print(json.dumps({k:v for k,v in result.items() if k not in ('queue','batches','limits')},ensure_ascii=False))


def refresh_overviews(result,audit):
    """Keep current counts in entry documents distinct from historical test records."""
    complete=result['complete_published_count'];pending=result['pending_published_count']
    candidates=result['pending_candidate_count'];packs=result['runtime_pack_count']
    slots=result['runtime_base_slots'];scenes=result['runtime_scenes']
    changes={
      'README.md':[
        ('当前完整专属题已覆盖',f'当前完整专属题已覆盖{complete}条游戏记录，共{packs}套作品题包、{slots}个基础题位，含模式与替代题{scenes}个情境。每次12道专属题＋4道跨游戏题，最多2道补问；旧答卷按原版本读取。[当前全部题目](exports/游格-已重写游戏题库.md) · [使用与版本说明](docs/18-game-specific-questionnaires.md) · [全库重写进度](exports/游格-专属题重写进度.md)。正式库另{pending:,}条仍待逐款重写，候选库{candidates:,}条待核实与编写。'),
        ('本轮重写后已',f'{result["checked_at"]}本轮重写后已逐条核对实际取题内容：{audit["published_count"]:,}条正式记录中，{complete}条完整专属、{pending:,}条未达完整标准；候选库另行记录。[逐游戏检查清单](exports/游格-逐游戏专属题检查清单.md) · [全部剩余待办](research/question-design-v0.5/rewrite-queue.json)。只替换游戏名或打乱选项顺序不算专属题。')],
      'docs/18-game-specific-questionnaires.md':[
        ('更新日期：',f'更新日期：{result["checked_at"]}。完整专属题当前接入{complete}条游戏记录，{packs}套作品题包、{slots}个基础题位，含模式与替代题{scenes}个情境。正式库另{pending:,}条仍待逐款重写；候选库{candidates:,}条列入核实与编写待办。'),
        ('[本轮新增作品与完整待办]',f'[本轮新增作品与完整待办](../exports/游格-专属题重写进度.md)。当前覆盖{complete}条游戏记录；完整批次、范围与待办状态以进度文件和实际取题检查为准。')],
      'research/question-design-v0.5/README.md':[
        ('当前共',f'当前共{complete}条游戏记录接入完整专属题，{packs}套题包、{slots}个基础题位、{scenes}个模式与替代情境。正式库剩余{pending:,}条待逐款编写；另{candidates:,}条候选列入核实与编写待办，不自动发布。'),
        ('本轮最初检查时',f'本轮最初检查时6条完整、9条部分定制、2,163条通用模板；现在{complete}条完整、{pending:,}条待完成。旧题包、未复核稿与待办记录不自动算作完成。运行题库保留不可覆盖的历史快照，旧答卷按原题义读取。')]
    }
    for name,replacements in changes.items():
        path=ROOT/name;content=path.read_text(encoding='utf-8').splitlines()
        for prefix,replacement in replacements:
            indices=[i for i,line in enumerate(content) if (len(line)>=10 and line[10:].startswith(prefix) if prefix=='本轮重写后已' else line.startswith(prefix))]
            assert len(indices)==1,(name,prefix,indices)
            content[indices[0]]=replacement
        path.write_text('\n'.join(content)+'\n',encoding='utf-8')


if __name__=='__main__':build()
