"""Catalogue contracts: real identities, visible names, legacy answers and search."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

from youge import questionnaires, v04
from youge.engine import InputError

ROOT=Path(__file__).resolve().parents[1]


class ExpandedCatalogueTests(unittest.TestCase):
    def test_published_names_have_chinese_context_and_no_pending_status(self):
        for game in v04.catalog()['games']:
            self.assertRegex(game['title'],r'[\u3400-\u9fff]',game['id'])
            self.assertEqual(game['visibility'],'published')
            self.assertNotIn('candidate_reason',game)
            self.assertTrue(game['source_url'].startswith('https://'))
            if game['name_status']=='original_brand_with_chinese_context':
                self.assertGreaterEqual(game['chinese_review_evidence']['total_reviews'],50,game['id'])

    def test_candidates_are_excluded_from_public_picker_but_legacy_ids_still_resolve(self):
        lib=v04.catalog();public=v04.bootstrap()
        ids={game['id'] for game in public['games']}
        self.assertFalse(ids & {game['id'] for game in lib['candidates']})
        for identifier in lib['legacy_game_ids']:
            self.assertEqual(v04.find_game(identifier)['id'],identifier)

    def test_public_game_scope_filters_new_choices_without_breaking_old_forms(self):
        scope=json.loads((ROOT/'config/questionnaire-audience-1149.json').read_bytes())
        public=v04.bootstrap()
        published_ids={game['id'] for game in public['games']}
        self.assertEqual(published_ids,set(scope['accepted_ids']) | {row['game_id'] for row in scope['selected']})
        self.assertLessEqual({game_id for pack in questionnaires.bootstrap()['authored_packs'] for game_id in pack['game_ids']},published_ids)
        self.assertLessEqual(set(public['featured']),published_ids)
        for category in public['categories']:
            self.assertLessEqual(set(category['game_ids']),published_ids)
        for redirect in public['search_redirects'].values():
            self.assertLessEqual(set(redirect['target_ids']),published_ids)
        archived_ids={game['id'] for game in public['archived_games']}
        self.assertFalse(published_ids & archived_ids)
        game_id='steam-1063730'
        self.assertIn(game_id,archived_ids)
        raw={'versions':v04.config()['versions'],'game_id':game_id,'answers':{},'extra_answers':[]}
        self.assertEqual(len(questionnaires.questions(raw=raw)['questions']),16)

    def test_original_question_pack_choices_remain_compatible(self):
        legacy=json.loads((ROOT/'config/games.v0.4.0.json').read_text(encoding='utf-8'))
        for old in legacy['games']:
            updated=v04.find_game(old['id'])
            self.assertEqual(updated['question_pack'],old['question_pack'])
            self.assertEqual(updated['mechanic_family'],old['mechanic_family'])

    def test_call_of_duty_launcher_only_routes_new_searches(self):
        launcher='steam-1938090'
        bootstrap=v04.bootstrap()
        self.assertNotIn(launcher,{game['id'] for game in bootstrap['games']})
        self.assertIn(launcher,{game['id'] for game in bootstrap['archived_games']})
        self.assertFalse(any(launcher in category['game_ids'] for category in bootstrap['categories']))
        with self.assertRaisesRegex(InputError,'具体作品'):
            questionnaires.questions(launcher)
        raw={'versions':v04.config()['versions'],'game_id':launcher,'answers':{},'extra_answers':[]}
        self.assertEqual(len(questionnaires.questions(raw=raw)['questions']),16)

    def test_edition_relationships_are_bidirectional_and_do_not_merge_ids(self):
        lib=v04.catalog();games={game['id']:game for game in lib['games']+lib['candidates']}
        for game in games.values():
            for relation in game['related_games']:
                self.assertIn(relation['id'],games)
                related=games[relation['id']]
                self.assertNotEqual(game['id'],related['id'])
                self.assertEqual(game['work_id'],related['work_id'])
                self.assertIn(game['id'],[record['id'] for record in related['related_games']])
        for original,remake in [('steam-254700','steam-2050650'),('steam-17470','steam-1693980')]:
            self.assertNotEqual(games[original]['version_type'],games[remake]['version_type'])
        self.assertNotIn('CSGO',games['steam-730']['aliases'])
        self.assertIn('CSGO',games['steam-4465480']['aliases'])

    def test_api_types_and_native_pc_are_verified_for_new_steam_games(self):
        for game in v04.catalog()['games']:
            if game['catalogue_origin']=='expanded_v0.5' and game['id'].startswith('steam-'):
                data=json.loads((ROOT/'research/catalogue-v0.5/products'/f'{game["id"][6:]}.json').read_text(encoding='utf-8'))
                self.assertTrue(data['success'])
                self.assertEqual(data['data']['type'],'game')
                self.assertFalse(data['data']['release_date']['coming_soon'])
                self.assertTrue(any(data['data']['platforms'].get(os) for os in ['windows','mac','steamos_linux']))

    @unittest.skipUnless(shutil.which('node'),'Node is needed to exercise the browser search module')
    def test_real_search_module_handles_aliases_scripts_and_distinct_editions(self):
        script=r'''
const fs=await import('node:fs');
const source=fs.readFileSync('web/v4-catalogue.js','utf8');
const {createGameIndex,searchGames,normalizeGameQuery}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const lib=JSON.parse(fs.readFileSync(0,'utf8'));
const index=createGameIndex(lib.games,lib.search_redirects);
const assert=(condition,message)=>{if(!condition)throw new Error(message);};
for(const [query,id] of [['LOL','league-of-legends'],['剑网三','jx-online-iii'],['夢幻西遊','fantasy-westward-journey'],['老滚5','steam-489830'],['给他爱5','steam-271590'],['DOTA 2','steam-570'],['CS２','steam-730'],['CS GO','steam-4465480'],['流星蝴蝶剑','meteor-blade-2002'],['生化危机4原版','steam-254700'],['生化危机4重制版','steam-2050650']]){
 const results=searchGames(index,query);assert(results.some(game=>game.id===id),query+' misses '+id);
}
assert(normalizeGameQuery('NieR™: Automata')===normalizeGameQuery('nier automata'),'Trademark normalization');
assert(searchGames(index,'').length===lib.games.length,'All games must be browsable');
assert(searchGames(index,'LOL',{category:'fps'}).length===0,'Category filter must apply');
assert(searchGames(index,'LOL').every(game=>game.id==='league-of-legends'),'Short acronyms must not match arbitrary substrings');
assert(searchGames(index,'CS GO').every(game=>game.id==='steam-4465480'),'Split short acronyms must not match unrelated words');
assert(searchGames(index,'叛乱（2014）')[0]?.id==='steam-222880','A display title must be searchable without a duplicate alias');
const original=searchGames(index,'生化危机4原版');
assert(original[0].id==='steam-254700','Original edition should rank first');
for(const [query,id] of [['奇异人生','steam-319630'],['Life is Strange','steam-319630'],['奇异人生2','steam-532210'],['Life is Strange 2','steam-532210']]){
 assert(searchGames(index,query)[0]?.id===id,query+' should rank '+id+' first');
}
assert(lib.games.find(game=>game.id==='steam-532210').original_title==='Life is Strange 2','Sequel should show the storefront name');
for(const query of ['极限脱出：九人游戏','999','善人死亡','VLR']){
 assert(searchGames(index,query)[0]?.id==='steam-477740',query+' should open the collection');
}
for(const query of ['激战2','激戰2','GW2']){
 assert(searchGames(index,query)[0]?.id==='steam-1284210',query+' should open Guild Wars 2');
}
for(const query of ['三国杀','三国杀十周年','三国杀：一将成名']){
 assert(searchGames(index,query)[0]?.id==='steam-1180320',query+' should open the verified Steam title');
}
for(const query of ['时光服','泰坦重铸服务器','魔兽世界周年专家']){
 assert(searchGames(index,query)[0]?.id==='world-of-warcraft-classic',query+' should open the Classic branch selector');
}
const codTargetIds=lib.search_redirects['steam-1938090'].target_ids;
for(const query of ['使命召唤','使命召喚','COD','COD HQ','Call of Duty HQ','使命召唤总部']){
 const results=searchGames(index,query);
 assert(results.every(game=>game.id!=='steam-1938090'),query+' must exclude the launcher');
 assert(codTargetIds.every(id=>results.some(game=>game.id===id)),query+' must offer the specific games');
}
for(const [query,id] of [['使命召唤：战争地带','steam-1962663'],['使命召唤：现代战争 II 2022','steam-3595230'],['使命召唤：现代战争 III 2023','steam-3595270'],['使命召唤：黑色行动 6','steam-4384550']]){
 assert(searchGames(index,query)[0]?.id===id,query+' must find the distinct edition first');
}
for(const query of ['使命召唤：现代战争（2019）','現代戰爭2019','COD16','MW2019']){
 assert(searchGames(index,query)[0]?.id==='steam-2000950',query+' must find the 2019 release first');
}
for(const query of ['战舰世界','戰艦世界','WOWS','战舰世界 Steam 国际服']){
 assert(searchGames(index,query)[0]?.id==='steam-552990',query+' must find the Steam international edition');
}
console.log(JSON.stringify({games:lib.games.length,queries:9,status:'passed'}));
'''
        library=v04.catalog()
        search_fixture={'games':[game | v04.current_game_identity(game) for game in library['games']],
                        'search_redirects':library['search_redirects']}
        result=subprocess.run(['node','--input-type=module','-e',script],cwd=ROOT,text=True,
                              input=json.dumps(search_fixture),
                              capture_output=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':
    unittest.main()
