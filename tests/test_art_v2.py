"""Current portrait selection and preservation of archived artwork."""
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
    def test_current_portraits_ignore_an_older_saved_preference(self):
        module = base64.b64encode((ROOT / 'web/v4-art.js').read_bytes()).decode('ascii')
        manifest = (ROOT / 'web/assets/personas-v2/preview.json').read_text(encoding='utf-8-sig')
        script = r"""
import assert from 'node:assert/strict';
const manifest = MANIFEST;
globalThis.localStorage = {getItem:()=> 'v1'};
const art = await import('data:text/javascript;base64,MODULE');
for (const asset of manifest.assets) {
  assert.equal(art.portraitFor({id:asset.id,portrait:asset.v1}),asset.v2);
  assert.equal(art.ribbonPortraitFor(asset),`/assets/personas-ribbon/v2/${asset.id}.webp`);
  assert.equal(art.heroPortraitFor(asset),`/assets/personas-hero/v2/${asset.id}.webp`);
}
const original = {persona:{id:'style_director',name:'A',portrait:'/assets/personas/style_director.png'}, scores:{EXP:75}, response:{answers:{Q01:'A'}}, versions:{scoring:'0.4.0'}};
const frozenJSON = JSON.stringify(original);
const v2 = art.styledReport(original);
assert.match(v2.persona.portrait,/personas-v2\/style_director-r2\.png$/);
assert.equal(JSON.stringify(original),frozenJSON);
assert.deepEqual(v2.scores,original.scores);
assert.deepEqual(v2.response,original.response);
assert.notEqual(v2.persona,original.persona);
""".replace('MANIFEST', manifest).replace('MODULE', module)
        result = subprocess.run(['node', '--input-type=module', '-e', script], capture_output=True, text=True, encoding='utf-8', cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
