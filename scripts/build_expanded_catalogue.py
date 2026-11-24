"""Build the expanded, source-backed offline catalogue without category quotas."""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from difflib import SequenceMatcher
import ctypes
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/catalogue-v0.5'
HAN = re.compile(r'[\u3400-\u9fff]')
AS_OF = '2026-10-28'
EXTRA_CATEGORIES = [
    ('moba', '多人在线战术竞技（MOBA）', 'strategy'),
    ('mmorpg', '大型多人在线角色扮演（MMORPG）', 'adventure'),
    ('online_rpg', '在线角色扮演', 'adventure'),
    ('battle_royale', '大逃杀', 'shooter'),
    ('extraction_shooter', '撤离射击', 'shooter'),
    ('party_multiplayer', '派对与多人合作', 'action'),
    ('social_deduction', '社交推理', 'strategy'),
    ('auto_battler', '自走棋', 'strategy'),
    ('vr', '虚拟现实（VR）', 'action'),
    ('action', '动作', 'action'),
    ('adventure', '冒险', 'adventure'),
    ('simulation', '模拟', 'management'),
]
FAMILY = {
    'fps':'shooter','third_person_shooter':'shooter','hack_and_slash':'action',
    'fighting_martial_arts':'action','arcade_rhythm':'rhythm','platformer_runner':'action',
    'shmup':'action','hidden_object':'hidden','metroidvania':'action','puzzle':'puzzle',
    'adventure_rpg':'adventure','visual_novel':'story','story_rich':'story',
    'action_rpg':'adventure','strategy_tactical_rpg':'strategy','jrpg':'adventure',
    'roguelike_roguelite':'rogue','turn_based_rpg':'strategy','party_based_rpg':'adventure',
    'building_automation':'management','hobby_job_sim':'management','dating_sim':'story',
    'farming_crafting':'life','space_flight_sim':'flight','life_immersive_sim':'life',
    'sandbox_physics':'creative','turn_based_strategy':'strategy','rts':'strategy',
    'tower_defense':'strategy','card_board':'cards','city_settlement':'management',
    'grand_strategy_4x':'strategy','military_strategy':'strategy','sports_sim_management':'management',
    'racing':'racing','racing_sim':'racing','team_sports':'sports','individual_sports':'sports','sports':'sports',
    'horror':'adventure','scifi_cyberpunk':'adventure','space':'flight','open_world':'adventure',
    'anime':'adventure','survival':'creative','mystery_detective':'puzzle',
    **{key: family for key, _, family in EXTRA_CATEGORIES},
}
TAG_CATEGORIES = {
    '第一人称射击':['fps'], '第三人称射击':['third_person_shooter'], '砍杀':['hack_and_slash'],
    '节奏':['arcade_rhythm'], '音乐节奏':['arcade_rhythm'], '平台游戏':['platformer_runner'],
    '精确平台':['platformer_runner'], '清版射击':['shmup'], '弹幕射击':['shmup'],
    '格斗':['fighting_martial_arts'], '2D 格斗':['fighting_martial_arts'], '3D 格斗':['fighting_martial_arts'],
    '隐藏物体':['hidden_object'], '休闲':['casual'], '类银河战士恶魔城':['metroidvania'],
    '解谜':['puzzle'], '视觉小说':['visual_novel'], '剧情丰富':['story_rich'],
    '动作角色扮演':['action_rpg'], '策略角色扮演':['strategy_tactical_rpg'], '日系角色扮演':['jrpg'],
    '战术角色扮演':['strategy_tactical_rpg'],
    '类 Rogue':['roguelike_roguelite'], '轻度 Rogue':['roguelike_roguelite'],
    '回合制战斗':['turn_based_rpg'], '团队角色扮演':['party_based_rpg'],
    '回合战略':['turn_based_strategy'], '回合制战术':['turn_based_strategy'],
    '自动化':['building_automation'], '恋爱模拟':['dating_sim'], '农场模拟':['farming_crafting'],
    '飞行':['space_flight_sim'], '沉浸式模拟':['life_immersive_sim'], '生活模拟':['life_immersive_sim'],
    '物理':['sandbox_physics'], '回合制策略':['turn_based_strategy'], '即时战略':['rts'],
    '塔防':['tower_defense'], '卡牌游戏':['card_board'], '卡牌战斗':['card_board'], '桌上游戏':['card_board'],
    '牌组构建':['card_board'], '牌组构建式类 Rogue':['card_board','roguelike_roguelite'],
    '城市营造':['city_settlement'], '殖民模拟':['city_settlement'], '大战略':['grand_strategy_4x'],
    '4X':['grand_strategy_4x'], '体育管理':['sports_sim_management'], '竞速':['racing'],
    '竞速模拟':['racing_sim'], '足球':['team_sports'], '篮球':['team_sports'], '棒球':['team_sports'],
    '网球':['individual_sports'], '高尔夫球':['individual_sports'], '体育':['sports'],
    '恐怖':['horror'], '赛博朋克':['scifi_cyberpunk'], '太空':['space'], '开放世界':['open_world'],
    '动漫':['anime'], '生存':['survival'], '推理':['mystery_detective'],
    '多人在线战术竞技':['moba'], '大型多人在线角色扮演':['mmorpg'], '大逃杀':['battle_royale'],
    '撤离射击':['extraction_shooter'], '派对游戏':['party_multiplayer'], '社交推理':['social_deduction'],
    '自走棋':['auto_battler'], '虚拟现实':['vr'], '动作':['action'], '冒险':['adventure'], '模拟':['simulation'],
}
NICKNAMES = {
    'minecraft':['MC','我的世界'],
    'steam-10':['CS1.6','CS 1.6','CS16','反恐精英1.6'],
    'steam-730':['CS2','反恐精英二'], 'steam-570':['DOTA2','刀塔2','刀塔','刀塔二'],
    'steam-4465480':['CSGO','CS:GO','反恐精英全球攻势','全球攻势'],
    'steam-216150':['冒险岛','枫之谷','楓之谷'],
    'steam-578080':['绝地求生','PUBG','吃鸡'], 'steam-1172470':['Apex英雄','APEX','顶点英雄'],
    'steam-2357570':['守望先锋','守望先锋2','OW','OW2'], 'steam-359550':['彩虹六号围攻','彩六','R6','R6S'],
    'steam-1203220':['永劫无间','NARAKA'], 'steam-2507950':['三角洲行动','三角洲'],
    'steam-440':['军团要塞2','TF2'], 'steam-238960':['流放之路','POE'],
    'steam-2694490':['流放之路2','POE2'], 'steam-2344520':['暗黑破坏神4','暗黑4','大菠萝4'],
    'steam-72850':['老滚5','上古卷轴5原版','天际原版'],
    'steam-489830':['老滚5','上古卷轴5','天际特别版','Skyrim SE','上古卷轴5周年纪念版'],
    'steam-22330':['老滚4','上古卷轴4原版','湮灭原版'], 'steam-22320':['老滚3','上古卷轴3','晨风'],
    'steam-271590':['GTA5','GTA V','给他爱5','侠盗猎车手5','GTA5旧版','GTA5传承版'],
    'steam-12100':['GTA3','侠盗猎车手3'], 'steam-12210':['GTA4','侠盗猎车手4'],
    'steam-12110':['GTAVC','GTA VC','罪恶都市'], 'steam-12120':['GTASA','GTA SA','圣安地列斯'],
    'steam-3240220':['GTA5','GTA V','给他爱5','侠盗猎车手5','GTA5增强版'],
    'steam-1174180':['大表哥2','RDR2','荒野大镖客2','荒野大镖客救赎2'],
    'steam-2668510':['大表哥1','RDR1','荒野大镖客1','荒野大镖客救赎'],
    'steam-1245620':['老头环','法环','艾尔登法环','ELDEN RING'],
    'steam-814380':['只狼','SEKIRO'], 'steam-374320':['黑魂3','魂3','黑暗之魂3'],
    'steam-570940':['黑魂1重制','黑暗之魂重制版'], 'steam-236430':['黑魂2原版','黑暗之魂2原版'],
    'steam-335300':['黑魂2原罪学者','原罪学者'], 'steam-1091500':['2077','CP2077','赛博朋克2077'],
    'steam-289070':['文明6','文明六','CIV6','CIV VI'], 'steam-8930':['文明5','文明五','CIV5'],
    'steam-3900':['文明4','文明四','CIV4'], 'steam-1295660':['文明7','文明七','CIV7'],
    'steam-261550':['骑砍2','骑砍二','骑马与砍杀2','骑马与砍杀2霸主','MB2'],
    'steam-48700':['骑砍战团','骑马与砍杀战团'], 'steam-1086940':['博德3','BG3','博德之门3'],
    'steam-435150':['神界原罪2','DOS2'], 'steam-1085660':['命运2','Destiny2'],
    'steam-413150':['星露谷','星露谷物语','SDV'], 'steam-105600':['泰拉瑞亚','泰拉'],
    'steam-4000':['GMod','盖瑞模组','盖瑞'], 'steam-646570':['杀戮尖塔','杀戮尖塔1','STS'],
    'steam-2868840':['杀戮尖塔2','STS2'], 'steam-2379780':['小丑牌','Balatro'],
    'steam-1623730':['幻兽帕鲁','帕鲁'], 'steam-294100':['环世界','边缘世界','RimWorld'],
    'steam-1938090':['使命召唤','COD','Call of Duty'], 'steam-254700':['生化危机4原版','生化危机4 2005','RE4原版'],
    'steam-2050650':['生化危机4重制版','RE4重制','RE4R'], 'steam-17470':['死亡空间原版','死亡空间2008'],
    'steam-1693980':['死亡空间重制版','死亡空间2023'], 'steam-7670':['生化奇兵原版','生化奇兵1原版'],
    'steam-409710':['生化奇兵重制版','生化奇兵1重制版'], 'steam-620':['传送门2','Portal2'],
}


def read(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def key(text):
    text=re.sub(r'[™®©]', '', str(text))
    return ''.join(char for char in unicodedata.normalize('NFKC', text).casefold() if char.isalnum())


def chinese_variant(text, traditional=False):
    if sys.platform != 'win32' or not HAN.search(text):
        return text
    flags = 0x04000000 if traditional else 0x02000000
    size = ctypes.windll.kernel32.LCMapStringEx('zh-CN', flags, text, len(text), None, 0, None, None, 0)
    if size <= 0:
        return text
    output = ctypes.create_unicode_buffer(size)
    ctypes.windll.kernel32.LCMapStringEx('zh-CN', flags, text, len(text), output, size, None, None, 0)
    result=output.value
    if traditional:
        for source,target in [('西游','西遊'),('游侠','遊俠'),('游乐','遊樂'),('游戏','遊戲')]:
            result=result.replace(source,target)
    return result


def clean_title(text):
    return re.sub(r'\s+', ' ', text.replace('™', '').replace('®', '').strip('《》 ')).strip()


def label_evidence(english, references):
    target = key(english)
    allowed_suffixes = {'', 'remastered', 'enhancededition', 'definitiveedition', 'ultimateedition',
                        'directorscut', 'englishEdition'.lower(), 'anniversaryedition', 'hdremaster',
                        'ver122474487139', 'ver122474487139', 'legionrising', 'xmikadoremix', 'connected'}
    matches = []
    for entry in references:
        source_key = key(entry['english_query'])
        position = target.find(source_key)
        if position < 0:
            continue
        tail = target[position + len(source_key):]
        if tail in allowed_suffixes or (source_key == key('NieR Replicant') and tail.startswith('ver1')):
            matches.append(entry)
    return max(matches, key=lambda entry: len(key(entry['english_query'])), default=None)


def classify(tags, seed_categories=None):
    categories = []
    for tag in tags:
        categories.extend(TAG_CATEGORIES.get(tag, []))
    # Exact tags avoid interpreting the shooter tag "快节奏" as a music game.
    if '角色扮演' in tags and not any(cat in categories for cat in ['action_rpg','jrpg','mmorpg','turn_based_rpg']):
        categories.append('adventure_rpg')
    if '大型多人在线' in tags and '角色扮演' in tags:
        categories.append('mmorpg')
    if '军事' in tags and ('策略' in tags or '即时战略' in tags):
        categories.append('military_strategy')
    if seed_categories:
        categories = [({'management':'hobby_job_sim','strategy':'turn_based_strategy'}.get(cat,cat))
                      for cat in seed_categories] + categories
    return list(dict.fromkeys(cat for cat in categories if cat in FAMILY or cat == 'casual')) or ['adventure']


def family_for(categories):
    priority = ['moba','mmorpg','extraction_shooter','fps','third_person_shooter','card_board',
                'arcade_rhythm','racing_sim','racing','hidden_object','visual_novel','dating_sim',
                'building_automation','farming_crafting','grand_strategy_4x','rts','turn_based_strategy',
                'tower_defense','strategy_tactical_rpg','roguelike_roguelite','metroidvania',
                'fighting_martial_arts','hack_and_slash','space_flight_sim','city_settlement',
                'sports_sim_management','team_sports','individual_sports','puzzle','action_rpg',
                'jrpg','turn_based_rpg','story_rich','sandbox_physics','life_immersive_sim']
    return next((FAMILY[cat] for cat in priority if cat in categories), 'adventure')


def seed_matches(seed, product):
    actual = key(product.get('english_name') or '')
    expected = key(seed['expected_title'])
    local = key(product['data'].get('name') or '')
    if local == key(seed['proposed_title']):
        return True
    if not actual:
        return False
    return actual == expected or (expected and actual.startswith(expected) and
        (actual[len(expected):] in ['remastered','remaster','enhancededition','definitiveedition',
                                   'ultimateedition','legacy','thecompleteedition','completeedition',
                                   'n7digitaldeluxeedition2012','aeternum'] or
         re.fullmatch(r'20\d\dedition',actual[len(expected):])))


def edition_details(english):
    for token, kind, label in [('Remake','remake','重制版'),('Remastered','remaster','高清重制版'),
                              ('Remaster','remaster','高清重制版'),('Definitive Edition','definitive','决定版'),
                              ('Special Edition','special','特别版'),('Enhanced Edition','enhanced','增强版'),
                              ('Ultimate Edition','ultimate','终极版'),('GOTY','goty','年度版'),
                              ('Game of the Year','goty','年度版'),('Collection','collection','合集'),
                              ('Legacy','legacy','传承版')]:
        if token.casefold() in english.casefold():
            return kind, label
    return 'standard', '标准版'


def series_aliases(game):
    """Editorial search terms derived from the identified work, never official-name claims."""
    aliases=[]
    patterns=[
        (r'^FINAL FANTASY\s+([IVX]+|\d+)', '最终幻想','FF'),
        (r'^Romance of the Three Kingdoms\s*([IVX]+|\d+)', '三国志','三国志'),
        (r'^DRAGON QUEST\s+([IVX]+|\d+)', '勇者斗恶龙','DQ'),
        (r'^Ys\s*([IVX]+|\d+)', '伊苏','伊苏'),
        (r'^Age of Empires\s+([IVX]+|\d+)', '帝国时代','AOE'),
        (r'^THE KING OF FIGHTERS\s*[\'’]?([IVX]+|\d+)', '拳皇','KOF'),
        (r'^Sid Meier.s Civilization\s+([IVX]+|\d+)', '文明','CIV'),
        (r'^Persona\s*(\d+)', '女神异闻录','P'),
        (r'^Resident Evil\s*(\d+)', '生化危机','RE'),
        (r'^Battlefield\s*([IVX]+|\d+)', '战地','BF'),
        (r'^DARK SOULS\s*([IVX]+|\d+)', '黑暗之魂','黑魂'),
    ]
    roman={'I':1,'V':5,'X':10}
    for pattern, chinese, short in patterns:
        match=re.search(pattern,clean_title(game['original_title']),re.I)
        if match:
            number=match[1].upper()
            if not number.isdigit():
                number=str(sum(-roman[c] if i+1<len(number) and roman[c]<roman[number[i+1]] else roman[c]
                               for i,c in enumerate(number)))
            aliases += [chinese+number,short+number]
    names=[game['title']]+game.get('aliases',[])
    numerals={'一':'1','二':'2','三':'3','四':'4','五':'5','六':'6','七':'7','八':'8','九':'9','十':'10',
              '壹':'1','贰':'2','叁':'3','肆':'4','伍':'5','陆':'6','柒':'7','捌':'8','玖':'9'}
    for name in names:
        for stem, short in [('仙剑奇侠传','仙剑'),('古剑奇谭','古剑'),('轩辕剑','轩辕剑'),
                            ('三国群英传','三国群英传'),('最终幻想','FF'),('女神异闻录','P')]:
            match=re.search(re.escape(stem)+r'\s*([一二三四五六七八九十壹贰叁肆伍陆柒捌玖]|\d+)',name)
            if match:
                number=numerals.get(match[1],match[1])
                aliases += [stem+number,short+number,short+match[1]]
        if name=='仙剑奇侠传':
            aliases += ['仙剑1','仙剑一','仙剑奇侠传1','仙剑奇侠传一']
    return list(dict.fromkeys(aliases))


def finalize_names(game):
    derived=series_aliases(game)
    game.setdefault('alias_evidence',[]).extend({'value':alias,'kind':'derived_series_search_term',
                                               'derived_from':game['original_title']} for alias in derived)
    aliases = list(dict.fromkeys(clean_title(alias) for alias in
                    [game['title'], game['original_title']] + game.get('aliases', []) + derived if alias))
    records = game.setdefault('alias_evidence', [])
    for alias in list(aliases):
        for variant in (chinese_variant(alias), chinese_variant(alias, True)):
            if variant and variant not in aliases:
                aliases.append(variant)
                records.append({'value': variant, 'kind': 'script_variant', 'derived_from': alias})
        # A Chinese numeral variant helps users who type "文明六" instead of "文明6".
        if HAN.search(alias):
            numerals = '零一二三四五六七八九'
            variant = re.sub(r'(?<=[\u3400-\u9fff])([1-9])(?!\d)', lambda match: numerals[int(match[1])], alias)
            if variant not in aliases:
                aliases.append(variant)
                records.append({'value': variant, 'kind': 'number_variant', 'derived_from': alias})
    game['aliases'] = aliases


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    legacy = read(ROOT/'config/games.v0.4.0.json')
    manifest = read(BASE/'manifest.json')
    references = [entry for path in BASE.glob('name-evidence*.json') for entry in read(path)['names']]
    search_aliases = read(BASE/'search-alias-evidence.json', {'aliases':[]})['aliases']
    references = [entry for entry in references if not any(host in entry['source_url'] for host in
                  ['dict.cn','eol.cn','nos.netease.com','357.com','game1319.com','bkso.baidu.com'])]
    tag_definitions = read(BASE/'tag-definitions.json', {}).get('response', {}).get('tags', [])
    tag_names = {tag['tagid']: tag['name'] for tag in tag_definitions}
    products = {int(path.stem): read(path) for path in (BASE/'products').glob('*.json')}
    seed_by_id = defaultdict(list)
    for seed in manifest['steam_seeds']:
        seed_by_id[seed['appid']].append(seed)
    legacy_by_id = {game['id']: game for game in legacy['games']}
    games = deepcopy(legacy_by_id)
    excluded = []
    identity_issues = []
    for appid, product in products.items():
        identifier = f'steam-{appid}'
        data = product['data']
        if identifier not in games:
            if not product['success'] or data.get('type') != 'game':
                excluded.append({'id': identifier, 'title': data.get('name'), 'reason': 'not_verified_as_game'})
                continue
            if not any(data.get('platforms', {}).get(os) for os in ('windows','mac','steamos_linux')):
                excluded.append({'id': identifier, 'title': data.get('name'), 'reason': 'native_pc_not_verified'})
                continue
            if data.get('release_date', {}).get('coming_soon'):
                excluded.append({'id': identifier, 'title': data.get('name'), 'reason': 'not_released'})
                continue
            matches = [seed for seed in seed_by_id[appid] if seed_matches(seed, product)]
            for seed in seed_by_id[appid]:
                if seed not in matches:
                    identity_issues.append({'appid': appid, 'expected': seed['expected_title'],
                                            'observed': product.get('english_name'), 'action': 'proposed_names_not_applied'})
            tags = [tag_names[tagid] for tagid in data.get('tagids', []) if tagid in tag_names]
            categories = classify(tags, [cat for seed in matches for cat in seed['category_ids']])
            games[identifier] = {'id': identifier, 'title': clean_title(data['name']),
                'original_title': clean_title(product.get('english_name') or data['name']),
                'aliases': [], 'category_ids': categories, 'mechanic_family': family_for(categories),
                'question_pack': None, 'platforms': ['PC'], 'source_url': f'https://store.steampowered.com/app/{appid}/',
                'source_status': 'verified_steam_product', 'review_snapshot': None,
                'award_evidence': [], 'store_tags': tags,
                'inclusion_rationale': '补充真实PC作品与系列历史；中文名称或中文受众证据分别核对，奖项不是必备门槛。'}
        game = games[identifier]
        game['identity_checked_at'] = product.get('checked_at')
        game['identity_source_url'] = product.get('source_url')
        if product['success'] and data.get('type') == 'game':
            game['store_tags'] = [tag_names[tagid] for tagid in data.get('tagids', []) if tagid in tag_names]
            game['pc_operating_systems'] = [name for flag, name in [('windows','Windows'),('mac','macOS'),('steamos_linux','Linux')]
                                            if data.get('platforms', {}).get(flag)]
            game['release_evidence'] = data.get('release_date')
            game['steam_franchises'] = data.get('franchises', [])
            localized = clean_title(data.get('name') or '')
            if HAN.search(localized):
                if not HAN.search(game['title']):
                    game['title'] = localized
                game['aliases'].append(localized)
                game.setdefault('name_evidence', []).append({'kind':'official_store_localized_name',
                    'value': localized, 'source_url': product['source_url'], 'checked_at': product['checked_at']})
            summaries = data.get('review_summaries', {})
            summary = summaries.get('summary_filtered')
            if summary:
                game['review_snapshot'] = {'total_reviews':summary.get('review_count',0),
                    'positive_percent':summary.get('percent_positive'), 'language_scope':'all',
                    'purchase_scope':'steam_purchases', 'offtopic_filtered':True,
                    'source_url':product['source_url']}
                game['review_checked_at'] = product['checked_at']
    # Existing name identities remain stable except a documented, cross-year mismatch.
    if 'steam-4045750' in games:
        game = games['steam-4045750']
        game['original_title'] = 'Out of the Park Baseball 27'
        game['aliases'] = [name for name in game['aliases'] if not re.search(r'Baseball\s*25', name)]
        game['identity_correction'] = '旧配置把27代的商店ID与25代原文名混在一起；已按商店身份纠正，不把不同年份当别名。'
    for game in games.values():
        game.setdefault('name_evidence', [])
        reference = label_evidence(game['original_title'], references)
        if reference:
            name = reference['chinese_name']
            game['aliases'].append(name)
            game['name_evidence'].append(deepcopy(reference))
            if not HAN.search(game['title']):
                game['title'] = name
        game['aliases'] += NICKNAMES.get(game['id'], [])
        if not HAN.search(game['title']):
            audience=read(BASE/'chinese-reviews'/f'{game["id"][6:]}.json',{}) if game['id'].startswith('steam-') else {}
            known_name=next((name for name in NICKNAMES.get(game['id'],[]) if HAN.search(name)),None)
            if known_name and audience.get('total_reviews',0)>=manifest['chinese_review_minimum']:
                game['title']=known_name
                game['name_status']='editorial_common_name_with_audience_evidence'
                game['name_evidence'].append({'kind':'editorial_common_name','value':known_name,
                    'identity_source_url':game['source_url'],'audience_source_url':audience['source_url'],
                    'note':'编辑整理的常见名称，不冒充商店官方译名；中文受众证据另列。'})
        # CSGO is a historical work and must not be an exact alias for Counter-Strike 2.
        if game['id'] == 'steam-730':
            game['aliases'] = [alias for alias in game['aliases'] if key(alias) not in {'csgo','counterstrikeglobaloffensive'}]
        game['catalogue_origin'] = 'legacy_v0.4' if game['id'] in legacy_by_id else 'expanded_v0.5'
    native_manifest = read(BASE/'native-seeds.json')
    native_manual=read(BASE/'manual-native-evidence.json',{})
    for seed in native_manifest['games']:
        check = read(BASE/'publishers'/f'{seed["id"]}.json', {})
        check.update(native_manual.get(seed['id'],{}))
        game = {'id':seed['id'], 'title':seed['title'], 'original_title':seed['original_title'],
                'aliases':seed['aliases'], 'category_ids':seed['categories'], 'mechanic_family':seed['family'],
                'question_pack':None, 'platforms':['PC'], 'pc_operating_systems':['Windows'],
                'source_url':seed['url'], 'source_status':check.get('status','publisher_fetch_pending'),
                'identity_checked_at':check.get('checked_at'), 'review_snapshot':None, 'award_evidence':[],
                'name_evidence':[{'kind':'publisher_name_check','source_url':check.get('verification_source_url',seed['url']),
                    'observed_page_title':check.get('page_title'), 'matched_names':check.get('matched_names',[])}],
                'pc_evidence_url':seed.get('pc_evidence_url',seed['url']),
                'catalogue_origin':'native_pc_supplement', 'inclusion_rationale':'中文PC端游、独立客户端或历史常玩作品补充；不包含手机专属产品。'}
        if check.get('status') not in ['publisher_identity_observed','verified_historical_reference']:
            game['candidate_reason'] = '发行方来源或作品名称仍需核对'
        # Global store and Chinese service pages can describe the same PC work.
        # Only exact original-name matches merge; similarly named sequels never do.
        equivalent=next((existing for existing in games.values() if
                        existing['id'].startswith('steam-') and
                        key(existing['original_title'])==key(game['original_title'])),None)
        if equivalent:
            if not game.get('candidate_reason'):
                equivalent['aliases'] += [game['title'],game['original_title']]+game['aliases']
                equivalent.setdefault('additional_sources',[]).append(game['source_url'])
                equivalent['category_ids']=list(dict.fromkeys(game['category_ids']+equivalent['category_ids']))
                equivalent['name_evidence']+=game['name_evidence']
                if equivalent['id'] not in legacy_by_id:
                    equivalent['mechanic_family']=game['mechanic_family']
                if not HAN.search(equivalent['title']):
                    equivalent['title']=game['title']
            else:
                equivalent.setdefault('pending_secondary_sources',[]).append({
                    'source_url':game['source_url'],'status':check.get('status'),
                    'proposed_chinese_name':game['title']})
            continue
        games[game['id']] = game
    apply_relationships(games)
    categories = deepcopy(legacy['categories'])
    for identifier, name, family in EXTRA_CATEGORIES:
        categories.append({'id':identifier,'name':name,'kind':'genre','game_ids':[],'image_positions':[]})
    category_names = {category['id']:category['name'] for category in categories}
    published, candidates = [], []
    for game in games.values():
        if game['id'] == 'steam-1506980':
            # The developer describes 葬花 as a visual novel. Ignore the FPS user tag.
            game['category_ids'] = [category for category in game['category_ids'] if category != 'fps']
            game['mechanic_family'] = 'story'
        game.setdefault('version_type', edition_details(game['original_title'])[0])
        game.setdefault('version_label', edition_details(game['original_title'])[1])
        game.setdefault('work_id',game['id'])
        game.setdefault('related_games',[])
        game['chinese_review_evidence'] = read(BASE/'chinese-reviews'/f'{game["id"][6:]}.json') if game['id'].startswith('steam-') else None
        if not HAN.search(game['title']):
            evidence = game.get('chinese_review_evidence') or {}
            if evidence.get('total_reviews',0) >= manifest['chinese_review_minimum']:
                game['name_status'] = 'original_brand_with_chinese_context'
                category = category_names.get(game['category_ids'][0], '游戏')
                game['title'] = f'{clean_title(game["title"])}（{category}）'
                game['chinese_context'] = category
                game['name_evidence'].append({'kind':'chinese_audience_verified',
                    'source_url':evidence['source_url'],'chinese_review_count':evidence['total_reviews']})
            else:
                game['candidate_reason'] = '尚无可核实中文名，中文评测未达到本轮受众证据阈值或数据待核对'
        else:
            game.setdefault('name_status', 'chinese_name_available')
        finalize_names(game)
        # Search aliases are added after eligibility and display-name decisions.
        # A translation found in a description must not silently rename a saved
        # report or make a candidate meet the publication threshold. These exact
        # reviewed spellings already include the intended script variants.
        for alias_evidence in search_aliases:
            if alias_evidence['game_id'] == game['id']:
                game['aliases'] = list(dict.fromkeys(game['aliases'] + alias_evidence['aliases']))
                game['name_evidence'].append({'kind':'reviewed_search_alias', **deepcopy(alias_evidence)})
        if game.get('candidate_reason'):
            game['visibility']='candidate'
            candidates.append(game)
        else:
            game['visibility']='published'
            published.append(game)
    for category in categories:
        category['game_ids'] = [game['id'] for game in published if category['id'] in game['category_ids']]
    output = {'version':'0.5.0','checked_at':AS_OF,'category_count':len(categories),
              'category_assignment_count':sum(len(category['game_ids']) for category in categories),
              'game_count':len(published),'candidate_count':len(candidates),
              'selection_policy':'native PC first; notable console games retained; unlimited category sizes; Chinese names or audience evidence required',
              'categories':categories,'games':published,'candidates':candidates,'featured':legacy['featured'],
              'legacy_game_ids':list(legacy_by_id),'provenance':deepcopy(legacy['provenance']) | {
                  'chinese_audience_threshold':manifest['chinese_review_minimum'],
                  'threshold_meaning':'仅作有中文玩家受众的工程筛选证据，不等于总体知名度或97%覆盖率',
                  'sources_frozen':True,'build_offline':True,'data_release_separate_from_instrument':True}}
    from identity_policy import apply_catalogue, archive_cod_launcher
    apply_catalogue(output)
    # Reviewed community names remain searchable across catalogue rebuilds.
    overrides = read(BASE/'reviewed-name-overrides.json', {})
    for game in output['games']:
        override = overrides.get(game['id'])
        if not override:
            continue
        apply_name_override(game, override)
    archive_cod_launcher(output)
    write(ROOT/'config/games.v0.5.0.json',output)
    write(BASE/'identity-issues.json',identity_issues)
    write(BASE/'excluded-products.json',excluded)
    write_exports(output)
    print(json.dumps({key:output[key] for key in ['game_count','candidate_count','category_count','category_assignment_count']},ensure_ascii=False))


def apply_name_override(game, override):
    game['display_title'] = override['display_title']
    if 'name_status' in override:
        game['name_status'] = override['name_status']
    if 'display_original_title' in override:
        game['display_original_title'] = override['display_original_title']
    removed = set(override.get('remove_aliases', ()))
    aliases = [alias for alias in game['aliases'] if alias not in removed]
    game['aliases'] = list(dict.fromkeys([*aliases, override['display_title'], *override['aliases']]))
    evidence = override['name_evidence']
    if evidence not in game.setdefault('name_evidence', []):
        game['name_evidence'].append(evidence)


def apply_relationships(games):
    """Explicit reviewed relationships; names alone never merge sequels or remakes."""
    relation_file = read(BASE/'relationships.json', {'works':[]})
    for work in relation_file['works']:
        members = [member for member in work['members'] if member['id'] in games]
        for member in members:
            game = games[member['id']]
            game['work_id']=work['id']
            game['work_title']=work['title']
            game['version_type']=member['type']
            game['version_label']=member['label']
            game['related_games']=[{'id':other['id'],'relation':other['type']} for other in members if other['id']!=member['id']]
            game['relationship_evidence']={'kind':'editorial_edition_alignment',
                'source_urls':[games[other['id']]['source_url'] for other in members]}
            if member.get('title'):
                game['title']=member['title']
                game['aliases'].append(member['title'])


def write_exports(catalogue):
    by_id={game['id']:game for game in catalogue['games']}
    lines=['# 《游格》游戏分类清单','','- 更新日期：'+AS_OF,'- 游戏库版本：0.5.0',
           f'- 已展示作品：{catalogue["game_count"]} 款；候选：{catalogue["candidate_count"]} 款。',
           f'- 分类：{catalogue["category_count"]} 类；归类关系：{catalogue["category_assignment_count"]} 条。',
           '- 各分类不设数量上限，同一作品可归属多个分类。',
           '- 以原生PC作品为主，保留知名主机作品；不新增手机专属或仅模拟器可玩的作品。',
           '- 中文名分别标明商店名称、中文资料通称和原文品牌；括号中的类型说明不是官方译名。',
           '- 中文评测数量仅用来证明存在中文受众；尚未通过真人抽样验证97%覆盖率。','']
    for category in catalogue['categories']:
        lines += [f'## {category["name"]}（{len(category["game_ids"])}款）','',
                  '| 作品 | 原文名 | 别名与检索词 | 版本 | 来源 |','|---|---|---|---|---|']
        for identifier in category['game_ids']:
            game=by_id[identifier]
            aliases='、'.join(alias for alias in game['aliases'] if alias not in [game['title'],game['original_title']])
            row=[game.get('display_title') or game['title'],game.get('display_original_title',game['original_title']),aliases,game['version_label'],f'[产品资料]({game["source_url"]})']
            lines.append('| '+' | '.join(value.replace('|',' / ').replace('\n',' ') for value in row)+' |')
        lines.append('')
    (ROOT/'exports/游格-游戏分类清单.md').write_text('\n'.join(lines),encoding='utf-8')
    (ROOT/'docs/12-v0.4-games.md').write_text('\n'.join(lines)+'\n\n维护方式、名称口径及验收方法见 [作品库扩充说明](16-v0.5-catalogue.md)。\n',encoding='utf-8')
    pending=['# 《游格》待核实游戏候选清单','','候选不会出现在新选择游戏的搜索结果中；原有答卷仍可按旧ID读取。','',
             '| 作品 | 原文名 | 待核对原因 | 来源 |','|---|---|---|---|']
    pending += [f'| {game["title"]} | {game["original_title"]} | {game["candidate_reason"]} | [核对来源]({game["source_url"]}) |'
                for game in catalogue['candidates']]
    (ROOT/'exports/游格-待核实游戏候选清单.md').write_text('\n'.join(pending)+'\n',encoding='utf-8')
    summary={'checked_at':AS_OF,'legacy_count':len(catalogue['legacy_game_ids']),
             'published_count':catalogue['game_count'],'candidate_count':catalogue['candidate_count'],
             'added_published':sum(game['id'] not in catalogue['legacy_game_ids'] for game in catalogue['games']),
             'legacy_in_candidates':sum(game['id'] in catalogue['legacy_game_ids'] for game in catalogue['candidates']),
             'source_statuses':dict(Counter(game['source_status'] for game in catalogue['games'])),
             'name_statuses':dict(Counter(game['name_status'] for game in catalogue['games'])),
             'categories':[{key:category[key] for key in ['id','name']}|{'count':len(category['game_ids'])} for category in catalogue['categories']]}
    write(BASE/'build-summary.json',summary)


if __name__ == '__main__':
    main()
