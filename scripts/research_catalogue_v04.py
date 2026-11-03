"""Collect only public product metadata and aggregate reviews; never store user reviews."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html import unescape
from html.parser import HTMLParser
import argparse
import json
from pathlib import Path
import re
import time
import threading
import unicodedata
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/catalogue-v0.4'
CACHE=OUT/'records'
REVIEW_LOCK=threading.Lock()
NEXT_REVIEW=0.0
STORE_LOCK=threading.Lock()
NEXT_STORE=0.0


def key(name):
    name=name.replace('™','').replace('®','').replace('©','')
    return ''.join(c for c in unicodedata.normalize('NFKD',name).casefold().replace('&','and') if c.isalnum() and not unicodedata.combining(c))


def slug(name):
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower()).strip('-')


def fetch(url):
    global NEXT_REVIEW,NEXT_STORE
    req=Request(url,headers={'User-Agent':'YougeCatalogueResearch/0.4 (public product metadata)'} )
    if 'api.steampowered.com/IUserReviewsService/' in url:
        with REVIEW_LOCK:
            time.sleep(max(0,NEXT_REVIEW-time.monotonic()))
            try:
                with urlopen(req,timeout=18) as r:result=r.read().decode('utf-8')
            except Exception as error:
                if getattr(error,'code',None)==429:
                    delay=max(60,int(error.headers.get('Retry-After','60')))
                    NEXT_REVIEW=time.monotonic()+delay
                raise
            finally:
                NEXT_REVIEW=max(NEXT_REVIEW,time.monotonic()+1.15)
        return result
    if 'store.steampowered.com/' in url:
        with STORE_LOCK:
            time.sleep(max(0,NEXT_STORE-time.monotonic()))
            try:
                with urlopen(req,timeout=18) as r:result=r.read().decode('utf-8')
            except Exception as error:
                if getattr(error,'code',None)==429:NEXT_STORE=time.monotonic()+max(90,int(error.headers.get('Retry-After','90')))
                raise
            finally:NEXT_STORE=max(NEXT_STORE,time.monotonic()+2.1)
        return result
    for attempt in range(2):
        try:
            with urlopen(req,timeout=18) as r:return r.read().decode('utf-8')
        except Exception as error:
            if getattr(error,'code',None)==429:raise
            if attempt:raise
            time.sleep(1.5)


class SearchParser(HTMLParser):
    def __init__(self):
        super().__init__();self.rows=[];self.current=None;self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and 'search_result_row' in a.get('class',''):
            m=re.search(r'/app/(\d+)',a.get('href',''))
            if m:self.current={'appid':int(m[1]),'title':''}
        if tag=='span' and self.current and 'title' in a.get('class','').split():self.in_title=True
    def handle_endtag(self,tag):
        if tag=='span':self.in_title=False
        if tag=='a' and self.current:
            self.rows.append(self.current);self.current=None
    def handle_data(self,data):
        if self.current and self.in_title:self.current['title']+=data


OVERRIDES={
 'Sid Meier\'s Civilization VI':289070,'Sid Meier\'s Civilization V':8930,'Sid Meier\'s Civilization IV':3900,
 'Red Dead Redemption 2':1174180,'DEATH STRANDING DIRECTOR\'S CUT':1850570,
 'Dead Cells':588650,'Slay the Spire':646570,'Mount & Blade II: Bannerlord':261550,
 'Kingdom Come: Deliverance II':1771300,'DAVE THE DIVER':1868140,
 'NieR:Automata':524220,'Sekiro: Shadows Die Twice - GOTY Edition':814380,
 'The Elder Scrolls III: Morrowind':22320,'ELDEN RING':1245620,
 'FIFA 23':1811260,'Football Manager 2024':2252570,'Football Manager 2023':1904540,
 'Forza Horizon 4':1293830,'Project CARS 2':378860,'Project CARS':234630,
 'Pro Evolution Soccer 2017':456610,'eFootball PES 2021 SEASON UPDATE':1259970,
 'NBA 2K23':1919590,'NBA 2K24':2338770,'NBA 2K25':2878980,
 'Warcraft III':None,'StarCraft II':None,'StarCraft: Remastered':None,
}


def research(name,force=False):
    path=CACHE/(slug(name)+'.json')
    previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
    if previous and not force and previous['verification_status']!='pending':return previous
    item={'id':slug(name),'query_title':name,'original_title':name,'checked_at':datetime.now(timezone.utc).isoformat(),'verification_status':'pending','sources':[]}
    try:
        appid=(previous.get('steam_appid') if previous else None) or OVERRIDES.get(name)
        search_url='https://store.steampowered.com/search/?'+urlencode({'term':name,'l':'english'})
        if not appid and name not in OVERRIDES:
            parser=SearchParser();parser.feed(fetch(search_url))
            exact=[r for r in parser.rows if key(r['title'])==key(name)]
            similar=sorted([(SequenceMatcher(None,key(name),key(r['title'])).ratio(),r) for r in parser.rows],key=lambda pair:pair[0],reverse=True)
            match=exact[0] if exact else (similar[0][1] if similar and similar[0][0]>=.94 else None)
            if match:appid=match['appid'];item['original_title']=match['title']
            else:item['search_candidates']=parser.rows[:5]
        if appid:
            item['steam_appid']=appid;item['store_url']=f'https://store.steampowered.com/app/{appid}/'
            item['sources'].append(item['store_url'])
            html=fetch(item['store_url']+'?l=schinese')
            title=re.search(r'<div[^>]+class="apphub_AppName"[^>]*>(.*?)</div>',html,re.S)
            if title:item['store_title_zh']=unescape(re.sub('<.*?>','',title[1])).strip()
            item['store_tags_zh']=[unescape(re.sub('<.*?>','',t)).strip() for t in re.findall(r'<a[^>]+class="app_tag"[^>]*>(.*?)</a>',html,re.S)]
            params={'appid':appid,'languages':['all'],'filter':1,'review_type':0,'purchase_type':0,'num_per_page':1}
            reviews_url='https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/?'+urlencode({'input_json':json.dumps(params,separators=(',',':'))})
            payload=json.loads(fetch(reviews_url))
            # Deliberately retain only totals; reviewers and review text are discarded.
            summary=payload.get('response',{}).get('query_summary',{})
            total=int(summary.get('total_reviews',0));positive=int(summary.get('total_positive',0))
            item['review_snapshot']={'total_reviews':total,'positive_reviews':positive,'positive_percent':round(100*positive/total,2) if total else None,'description':summary.get('review_score_desc'),'language_scope':'all','purchase_scope':'steam_purchases','offtopic_filtered':True,'source_url':reviews_url}
            item['verification_status']='verified_steam_product_and_review_totals' if total else 'verified_steam_product_no_review_totals'
        else:
            item['search_url']=search_url
            item['verification_status']='needs_publisher_or_console_source'
    except Exception as error:item['error']=str(error)[:180]
    CACHE.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return item


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=0);parser.add_argument('--workers',type=int,default=4);parser.add_argument('--force',action='store_true');args=parser.parse_args()
    data=json.loads((OUT/'shortlist.json').read_text(encoding='utf-8'))
    names=list(dict.fromkeys(x for group in data.values() for x in group))
    if args.limit:names=names[:args.limit]
    results=[]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs={pool.submit(research,n,args.force):n for n in names}
        for future in as_completed(jobs):
            results.append(future.result())
            if len(results)%25==0:print(f'Public catalogue metadata: {len(results)}/{len(names)}',flush=True)
    summary={'total':len(results),'steam_verified':sum(r['verification_status'].startswith('verified_steam') for r in results),'remaining':[r['query_title'] for r in results if not r['verification_status'].startswith('verified_steam')]}
    (OUT/'verification-progress.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='remaining'}),flush=True)


if __name__=='__main__':main()
