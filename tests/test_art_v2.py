"""Art rollback and presentation isolation; no questionnaire scoring changes."""
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ArtEditionTests(unittest.TestCase):
    def test_original_portraits_remain_byte_identical(self):
        baseline = json.loads((ROOT / 'design/v0.4.2/v1-baseline.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(len(baseline['assets']), 16)
        for asset in baseline['assets']:
            payload = (ROOT / asset['path']).read_bytes()
            self.assertEqual(len(payload), asset['bytes'], asset['id'])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), asset['sha256'], asset['id'])

    def test_complete_new_edition_matches_saved_assets(self):
        public = json.loads((ROOT / 'web/assets/personas-v2/preview.json').read_text(encoding='utf-8-sig'))
        manifest = json.loads((ROOT / 'design/v0.4.2/portraits-manifest.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(public['status'], 'complete')
        self.assertEqual(len(public['assets']), 16)
        self.assertEqual(len({p['id'] for p in public['assets']}), 16)
        records = {p['id']: p for p in manifest['assets']}
        self.assertEqual(len(records), 16)
        for persona in public['assets']:
            with self.subTest(persona=persona['id']):
                self.assertTrue(persona['v2'].startswith('/assets/personas-v2/'))
                path = ROOT / 'web' / persona['v2'].lstrip('/')
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), records[persona['id']]['sha256'])
                self.assertTrue((ROOT / 'web' / persona['v1'].lstrip('/')).is_file())

    @unittest.skipUnless(shutil.which('node'), 'Node is needed for the browser art module check')
    def test_switch_changes_only_presentation_and_saves_separate_preference(self):
        module = base64.b64encode((ROOT / 'web/v4-art.js').read_bytes()).decode('ascii')
        manifest = (ROOT / 'web/assets/personas-v2/preview.json').read_text(encoding='utf-8-sig')
        script = r"""
import assert from 'node:assert/strict';
const manifest = MANIFEST;
const storage = new Map();
globalThis.localStorage = {getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)};
globalThis.fetch = async()=>({ok:true,json:async()=>manifest});
const art = await import('data:text/javascript;base64,MODULE');
await art.initArt();
assert.equal(art.artEdition(),'v2');
const original = {persona:{id:'style_director',name:'A',portrait:'/assets/personas/style_director.png'}, scores:{EXP:75}, response:{answers:{Q01:'A'}}, versions:{scoring:'0.4.0'}};
const frozenJSON = JSON.stringify(original);
const v2 = art.styledReport(original);
assert.match(v2.persona.portrait,/personas-v2\/style_director-r2\.png$/);
assert.equal(JSON.stringify(original),frozenJSON);
assert.deepEqual(v2.scores,original.scores);
assert.deepEqual(v2.response,original.response);
assert.notEqual(v2.persona,original.persona);
assert.equal(art.setArtEdition('v1'),true);
assert.equal(art.styledReport(original).persona.portrait,original.persona.portrait);
assert.deepEqual([...storage.keys()],['youge-art-edition']);
assert.equal(art.setArtEdition('invalid'),false);
assert.equal(JSON.stringify(original),frozenJSON);
await art.initArt();
assert.equal(art.artEdition(),'v1');
globalThis.fetch=async()=>{throw Error('unavailable')};
await art.initArt();
assert.equal(art.artEdition(),'v1');
assert.equal(art.setArtEdition('v2'),false);
assert.equal(art.portraitFor(original.persona),original.persona.portrait);
console.log('Art switching, persistence, immutable reports and fallback passed');
""".replace('MANIFEST', manifest).replace('MODULE', module)
        result = subprocess.run(['node', '--input-type=module', '-e', script], capture_output=True, text=True, encoding='utf-8', cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
