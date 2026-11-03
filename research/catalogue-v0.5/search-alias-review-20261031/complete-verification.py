from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path.cwd()
def read(path):
    return json.loads((root / path).read_text(encoding='utf8'))
def save(path, obj):
    (root / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
def sha(path):
    return hashlib.sha256((root / path).read_bytes()).hexdigest()

logpath = 'output/playwright/reviewed-search-aliases-20261031-check-result.log'
lines = (root / logpath).read_text(encoding='utf8').splitlines()
assert '### Error' not in lines
result = json.loads(lines[lines.index('### Result')+1])
assert result['status'] == 'actual_browser_search_and_identity_passed'
assert len(result['cases']) == 8 and all(r['passed'] for r in result['cases'])
assert result['local_answers_and_reports_unchanged']
ui_path = 'output/playwright/reviewed-search-aliases-20261031-validation.json'
result['source_log'] = logpath
result['source_log_sha256'] = sha(logpath)
save(ui_path, result)

history_path = 'reports/catalogue-reviewed-search-aliases-history-20261031.json'
history = read(history_path)
assert history['passed'] and history['historical_form_and_report_pairs'] == 4660
assert history['changed_pack_ids'] == []
testpath = 'reports/catalogue-reviewed-search-aliases-tests-20261031.log'
testlog = (root / testpath).read_text(encoding='utf8')
assert 'Ran 173 tests' in testlog and testlog.rstrip().endswith('OK')
reportpath = 'reports/catalogue-reviewed-search-aliases-20261031.json'
report = read(reportpath)
assert sha('config/games.v0.5.0.json') == report['after_catalogue_sha256']
report.update(status='source_diff_history_tests_and_actual_browser_search_accepted',
              verification_completed_at_utc=datetime.now(timezone.utc).isoformat(),
              actual_browser_search=ui_path, actual_browser_search_sha256=sha(ui_path),
              historical_report_check=history_path, historical_report_check_sha256=sha(history_path),
              historical_form_and_report_pairs_unchanged=4660,
              tests={'path':testpath, 'sha256':sha(testpath), 'count':173, 'passed':True})
report['qualification'] = ('Four verified search aliases added to two existing formal records. '
    'Display titles, versions, questions, signals, inclusion and all 4660 historical form/report '
    'pairs unchanged. Eight real browser searches and all 173 existing tests passed.')
save(reportpath, report)

activepath = 'research/question-design-v0.5/active-rewrite-run.json'
active = read(activepath)
for item in active.get('catalogue_alias_followups', []):
    if item['game_id'] == 'steam-1245560':
        item.update(status='reviewed_aliases_added_history_and_browser_verified', acceptance=reportpath)
    elif item['game_id'] == 'steam-690830':
        item.update(state='existing_reviewed_alias_already_present_actual_browser_verified',
                    browser_evidence=ui_path)
active['latest_catalogue_alias_acceptance'] = reportpath
save(activepath, active)

prepath = 'research/question-design-v0.5/source-cache/batch09-i-preflight/parent-preflight-reading.json'
pre = read(prepath)
pre['additional_full_articles_actually_read'] = [
    '1084600-6890025005347946128-body.txt',
    '1432860-1836506165544621-body.txt',
    '1158160-1846651706682664-body.txt',
]
pre['additional_reading_findings'] = [
    'Sandrock Online1.2.0 crossplay June13,2024 full4279charbodyread; independent Online progression requires current author verification.',
    'SunHaven3.1QoL full8297charbodyread. 8repairables, namedLargeChests, enemy/mana/cooldown-limited ChainLightning, realtime consumable duration, seasonalSnaccoon partialitems reset annually. Current3.1.3b4760charbody not yet parent-read.',
    'Coral future1.4 KidsGrowUp full4011charbodyread: winter2026 future, not current1.3. Do not use announced school/teen/hobby or1.4UI features as available.',
]
pre['reviewed_pacha_search_alias_acceptance'] = reportpath
pre['qualification'] = ('Six full store About bodies, three listed short articles and three listed '
    'additional articles actually read. Other downloaded news are not automatically read or accepted. '
    'No question authorship or dispatch is implied. Pacha aliases now separately verified in real search.')
save(prepath, pre)
print(json.dumps({'status':report['status'], 'unchanged_history_pairs':4660,
                  'actual_searches':8, 'tests':173}, ensure_ascii=False))
