"""Catalogue contracts: real identities, visible names, legacy answers and search."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

from youge import v04

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

    def test_original_question_pack_choices_remain_compatible(self):
        legacy=json.loads((ROOT/'config/games.v0.4.0.json').read_text(encoding='utf-8'))
        for old in legacy['games']:
            updated=v04.find_game(old['id'])
            self.assertEqual(updated['question_pack'],old['question_pack'])
            self.assertEqual(updated['mechanic_family'],old['mechanic_family'])

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
const lib=JSON.parse(fs.readFileSync('config/games.v0.5.0.json','utf8'));
const index=createGameIndex(lib.games);
const assert=(condition,message)=>{if(!condition)throw new Error(message);};
for(const [query,id] of [['LOL','league-of-legends'],['剑网三','jx-online-iii'],['夢幻西遊','fantasy-westward-journey'],['老滚5','steam-489830'],['给他爱5','steam-271590'],['DOTA 2','steam-570'],['CS２','steam-730'],['CS GO','steam-4465480'],['流星蝴蝶剑','meteor-blade-2002'],['生化危机4原版','steam-254700'],['生化危机4重制版','steam-2050650']]){
 const results=searchGames(index,query);assert(results.some(game=>game.id===id),query+' misses '+id);
}
assert(normalizeGameQuery('NieR™: Automata')===normalizeGameQuery('nier automata'),'Trademark normalization');
assert(searchGames(index,'').length===lib.games.length,'All games must be browsable');
assert(searchGames(index,'LOL',{category:'fps'}).length===0,'Category filter must apply');
assert(searchGames(index,'LOL').every(game=>game.id==='league-of-legends'),'Short acronyms must not match arbitrary substrings');
assert(searchGames(index,'CS GO').every(game=>game.id==='steam-4465480'),'Split short acronyms must not match unrelated words');
const original=searchGames(index,'生化危机4原版');
assert(original[0].id==='steam-254700','Original edition should rank first');
console.log(JSON.stringify({games:lib.games.length,queries:9,status:'passed'}));
'''
        result=subprocess.run(['node','--input-type=module','-e',script],cwd=ROOT,text=True,capture_output=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':
    unittest.main()
