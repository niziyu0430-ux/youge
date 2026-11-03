"""Check and freeze public publisher pages for native-PC catalogue targets."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
import json
from pathlib import Path
import re
import sys
import argparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/catalogue-v0.5'


def check(game, refresh=False):
    path = BASE / 'publishers' / (game['id'] + '.json')
    if path.exists() and not refresh:
        return json.loads(path.read_text(encoding='utf-8'))
    record = {'id': game['id'], 'source_url': game['url'], 'checked_at': datetime.now(timezone.utc).isoformat()}
    try:
        with urlopen(Request(game['url'], headers={'User-Agent':'YougeCatalogueResearch/0.5 (public game identity)'}), timeout=18) as response:
            raw = response.read(2_000_000)
            encoding = response.headers.get_content_charset() or 'utf-8'
            text = raw.decode(encoding, errors='replace')
            if text.count('\ufffd') > 10:
                text = raw.decode('gb18030', errors='replace')
            record['resolved_url'] = response.url
        match = re.search(r'<title[^>]*>(.*?)</title>', text, re.S | re.I)
        record['page_title'] = unescape(re.sub('<[^>]+>', '', match[1])).strip() if match else ''
        plain = re.sub(r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>', '', text, flags=re.S|re.I)
        plain = re.sub(r'\s+', ' ', unescape(re.sub('<[^>]+>', ' ', plain)))
        names = [game['title']] + game['aliases']
        record['matched_names'] = [name for name in names if
            (re.search('[\u3400-\u9fff]',name) and len(name)>=2 and name in text) or
            (len(name)>=3 and re.search(r'(?<![A-Za-z0-9])'+re.escape(name)+r'(?![A-Za-z0-9])',text,re.I))]
        record['native_pc_markers'] = sorted(set(re.findall(r'Windows|PC版|PC端|电脑版|端游|客户端下载|下载游戏|游戏客户端', text, re.I)))
        record['text_excerpt'] = plain[:650]
        record['status'] = 'publisher_identity_observed' if record['matched_names'] else 'publisher_page_needs_manual_review'
    except Exception as error:
        record['status'] = 'publisher_fetch_pending'
        record['error'] = str(error)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return record


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser();parser.add_argument('--refresh',action='store_true');args=parser.parse_args()
    games = json.loads((BASE/'native-seeds.json').read_text(encoding='utf-8'))['games']
    with ThreadPoolExecutor(max_workers=5) as pool:
        for future in as_completed([pool.submit(check, game,args.refresh) for game in games]):
            record = future.result()
            print(record['id'], record['status'], record.get('page_title','')[:70], flush=True)


if __name__ == '__main__':
    main()
