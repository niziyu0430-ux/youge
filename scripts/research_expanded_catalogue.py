"""Freeze public game identities and Chinese-language review totals for catalogue 0.5.

Only aggregates and product metadata are retained. Normal catalogue builds are offline.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
import argparse
import json
from pathlib import Path
import re
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/catalogue-v0.5'
STORE_LOCK = threading.Lock()
REVIEW_LOCK = threading.Lock()
NEXT = {'store': 0.0, 'review': 0.0}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def fetch(url, group='store'):
    lock = REVIEW_LOCK if group == 'review' else STORE_LOCK
    for attempt in range(2):
        with lock:
            time.sleep(max(0, NEXT[group] - time.monotonic()))
            NEXT[group] = time.monotonic() + (1.15 if group == 'review' else 2.2)
        try:
            req = Request(url, headers={'User-Agent': 'YougeCatalogueResearch/0.5 (public metadata; no reviews retained)'})
            with urlopen(req, timeout=22) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code == 429:
                delay=max(90, int(error.headers.get('Retry-After', '90')))
                with lock:
                    NEXT[group] = max(NEXT[group], time.monotonic() + delay)
                save(BASE/'steam-cooldown.json',{'retry_after_epoch':time.time()+delay,'group':group})
                raise
            if attempt:
                raise
        except Exception:
            if attempt:
                raise
        time.sleep(2)


class SearchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current = None
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'search_result_row' in attrs.get('class', ''):
            match = re.search(r'/app/(\d+)', attrs.get('href', ''))
            if match:
                self.current = {'appid': int(match[1]), 'title': ''}
        if tag == 'span' and self.current and 'title' in attrs.get('class', '').split():
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'span':
            self.in_title = False
        if tag == 'a' and self.current:
            self.rows.append(self.current)
            self.current = None

    def handle_data(self, data):
        if self.current and self.in_title:
            self.current['title'] += data


def discover(query):
    label = query.get('key') or re.sub(r'[^\w-]+', '-', query['term']).strip('-')
    cache = BASE / 'searches' / (label + '.json')
    if cache.exists():
        cached = json.loads(cache.read_text(encoding='utf-8'))
        if cached.get('parser_version') == 2:
            return cached
    url = 'https://store.steampowered.com/search/results/?' + urlencode({
        'term': query['term'], 'l': 'schinese', 'cc': 'cn', 'category1': '998',
        'count': 50, 'start': query.get('start', 0), 'json': 1, 'ignore_preferences': 1,
        **({'filter': query['filter']} if query.get('filter') else {}),
    })
    try:
        payload = fetch(url)
        parser = SearchParser()
        parser.feed(payload.get('results_html', ''))
        # The current public search also returns a compact {items:[{name,logo}]} form.
        # Extract IDs only from the official item's explicitly supplied Steam URL.
        if not parser.rows and 'items' in payload:
            for item in payload['items']:
                match = re.search(r'/(?:apps|app)/(\d+)/', item.get('url', '') + ' ' + item.get('logo', ''))
                if match:
                    parser.rows.append({'appid': int(match[1]), 'title': unescape(item.get('name', ''))})
        result = dict(query, source_url=url, checked_at=datetime.now(timezone.utc).isoformat(),
                      results=parser.rows, total_count=payload.get('total_count'), parser_version=2)
        save(cache, result)
        return result
    except Exception as error:
        return dict(query, results=[], error=str(error))


def basic(appids):
    missing = [appid for appid in appids if not (BASE / 'products' / f'{appid}.json').exists()]
    for start in range(0, len(missing), 40):
        batch = missing[start:start + 40]
        params = {'ids': [{'appid': appid} for appid in batch],
                  'context': {'language': 'schinese', 'country_code': 'CN'},
                  'data_request': {'include_basic_info': True, 'include_release': True,
                                   'include_platforms': True, 'include_tag_count': 40,
                                   'include_reviews': True, 'include_supported_languages': True,
                                   'include_best_purchase_option': False}}
        url = 'https://api.steampowered.com/IStoreBrowseService/GetItems/v1/?' + urlencode({'input_json': json.dumps(params, separators=(',', ':'))})
        try:
            items = fetch(url, 'review').get('response', {}).get('store_items')
            if items is None:
                raise ValueError('No store_items; failed requests must not become empty products')
            data = {item.get('appid', item.get('id')): item for item in items}
            params['context']['language'] = 'english'
            params['data_request'] = {'include_best_purchase_option': False}
            english_url = 'https://api.steampowered.com/IStoreBrowseService/GetItems/v1/?' + urlencode({'input_json': json.dumps(params, separators=(',', ':'))})
            english_data = {item.get('appid', item.get('id')): item for item in
                            fetch(english_url, 'review').get('response', {}).get('store_items', [])}
            for appid in batch:
                item = data.get(appid, {})
                release = item.get('release', {})
                game = {'steam_appid': appid, 'name': item.get('name'),
                        'type': 'game' if item.get('type', -1) == 0 else str(item.get('type')),
                        'short_description': item.get('basic_info', {}).get('short_description'),
                        'platforms': item.get('platforms', {}),
                        'release_date': {'coming_soon': release.get('is_coming_soon', False),
                                         'steam_release_timestamp': release.get('steam_release_date')},
                        'tagids': item.get('tagids', []), 'related_items': item.get('related_items', {}),
                        'review_summaries': item.get('reviews', {}),
                        'franchises': item.get('basic_info', {}).get('franchises', [])}
                checked = datetime.now(timezone.utc).isoformat()
                save(BASE / 'products' / f'{appid}.json', {
                    'appid': appid, 'success': item.get('success') == 1,
                    'data': game,
                    'english_name': english_data.get(appid, {}).get('name'),
                    'source_url': url, 'english_source_url': english_url,
                    'checked_at': checked,
                })
                summary = item.get('reviews', {}).get('summary_language_specific')
                if summary is not None:
                    save(BASE / 'chinese-reviews' / f'{appid}.json', {
                        'appid': appid, 'checked_at': checked,
                        'total_reviews': summary.get('review_count', 0),
                        'positive_percent': summary.get('percent_positive'),
                        'language_scope': ['schinese'], 'purchase_scope': 'steam_purchases',
                        'offtopic_filtered': True, 'source_url': url,
                    })
        except Exception as error:
            print(f'PRODUCT_BATCH_ERROR {batch}: {error}', flush=True)
        print(f'PRODUCTS {min(start + 40, len(missing))}/{len(missing)}', flush=True)


def reviews(appid):
    cache = BASE / 'chinese-reviews' / f'{appid}.json'
    if cache.exists():
        return json.loads(cache.read_text(encoding='utf-8'))
    params = {'appid': appid, 'languages': ['schinese', 'tchinese'], 'filter': 1,
              'review_type': 0, 'purchase_type': 0, 'num_per_page': 1}
    url = 'https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/?' + urlencode({'input_json': json.dumps(params, separators=(',', ':'))})
    try:
        data = fetch(url, 'review').get('response', {}).get('query_summary')
        if data is None:
            raise ValueError('No query_summary; missing data is not zero reviews')
        result = {'appid': appid, 'checked_at': datetime.now(timezone.utc).isoformat(),
                  'total_reviews': data.get('total_reviews'), 'total_positive': data.get('total_positive'),
                  'total_negative': data.get('total_negative'), 'language_scope': ['schinese', 'tchinese'],
                  'purchase_scope': 'steam_purchases', 'offtopic_filtered': True, 'source_url': url}
        save(cache, result)
        return result
    except Exception as error:
        return {'appid': appid, 'error': str(error)}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=['discover', 'products', 'reviews', 'all'], default='all')
    args = parser.parse_args()
    cooldown_path = BASE / 'steam-cooldown.json'
    if cooldown_path.exists():
        cooldown = json.loads(cooldown_path.read_text(encoding='utf-8'))
        remaining = cooldown.get('retry_after_epoch', 0) - time.time()
        if remaining > 0:
            NEXT['store'] = time.monotonic() + remaining
            NEXT['review'] = time.monotonic() + remaining
            print(f'Respecting Steam cooldown: {remaining:.0f}s before next store request', flush=True)
    manifest = json.loads((BASE / 'manifest.json').read_text(encoding='utf-8'))
    legacy = json.loads((ROOT / 'config/games.v0.4.0.json').read_text(encoding='utf-8'))
    discovered = []
    if args.stage in ('discover', 'all'):
        with ThreadPoolExecutor(max_workers=3) as pool:
            for index, result in enumerate(pool.map(discover, manifest['queries']), 1):
                discovered.append(result)
                print(f'SEARCH {index}/{len(manifest["queries"])} {result["term"]}: {len(result["results"])} {result.get("error", "")}', flush=True)
        save(BASE / 'discovered.json', discovered)
    elif (BASE / 'discovered.json').exists():
        discovered = json.loads((BASE / 'discovered.json').read_text(encoding='utf-8'))
    if (BASE/'supplementary-discovered.json').exists():
        discovered += json.loads((BASE/'supplementary-discovered.json').read_text(encoding='utf-8'))
    appids = sorted({int(game['appid']) for game in manifest['steam_seeds']} |
                    {int(game['appid']) for group in discovered for game in group['results']} |
                    {int(game['id'][6:]) for game in legacy['games'] if game['id'].startswith('steam-')})
    if args.stage in ('products', 'all'):
        basic(appids)
    if args.stage in ('reviews', 'all'):
        legacy_ids = {int(game['id'][6:]) for game in legacy['games'] if game['id'].startswith('steam-')}
        wanted = {int(game['id'][6:]) for game in legacy['games']
                  if game['id'].startswith('steam-') and not re.search(r'[\u3400-\u9fff]', game['title'])}
        for appid in appids:
            path = BASE / 'products' / f'{appid}.json'
            if not path.exists():
                continue
            product = json.loads(path.read_text(encoding='utf-8'))
            data = product['data']
            if product['success'] and data.get('type') == 'game' and appid not in legacy_ids:
                if not re.search(r'[\u3400-\u9fff]', data.get('name', '')):
                    wanted.add(appid)
        failed = []
        with ThreadPoolExecutor(max_workers=4) as pool:
            jobs = {pool.submit(reviews, appid): appid for appid in sorted(wanted)}
            for index, future in enumerate(as_completed(jobs), 1):
                result = future.result()
                if 'error' in result:
                    failed.append(result)
                if index % 25 == 0 or index == len(jobs):
                    print(f'CHINESE_REVIEWS {index}/{len(jobs)} errors={len(failed)}', flush=True)
        save(BASE / 'fetch-errors.json', failed)


if __name__ == '__main__':
    main()
