"""Freeze the public IPIP translation and the official item-order scoring key.

This is an explicit research-source refresh command, not part of normal builds.
It refuses to overwrite a frozen version. No simplified-Chinese adaptation is made.
"""

from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.request import urlopen


ROOT=Path(__file__).resolve().parents[1]
DESTINATION=ROOT/"research"/"ipip50.zh-Hant.source-v1.json"
TRANSLATION="https://ipip.ori.org/ChineseAB5CFactorMarkers.htm"
KEY="https://ipip.ori.org/new_ipip-50-item-scale.htm"
PERMISSION="https://ipip.ori.org/newPermission.htm"


class TableRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows=[]
        self.row=None
        self.cell=None

    def handle_starttag(self,tag,attrs):
        if tag=="tr":
            self.row=[]
        elif tag in ("td","th") and self.row is not None:
            self.cell=[]

    def handle_data(self,data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self,tag):
        if tag in ("td","th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell=None
        elif tag=="tr" and self.row is not None:
            self.rows.append(self.row)
            self.row=None


def fetch_rows(url):
    with urlopen(url,timeout=30) as connection:
        raw=connection.read()
    encoding="utf-16" if raw.startswith((b"\xff\xfe",b"\xfe\xff")) else "utf-8-sig"
    parser=TableRows()
    parser.feed(raw.decode(encoding))
    numbered={int(row[0].rstrip(".")):row for row in parser.rows if row and row[0].rstrip(".").isdigit()}
    if set(numbered)!=set(range(1,51)):
        raise ValueError("Source does not contain exactly the expected 50 items")
    return numbered,{"url":url,"sha256":sha256(raw).hexdigest(),"encoding":encoding}


def normalize_english(text):
    text=text.strip().rstrip(".").casefold()
    return text[2:] if text.startswith("i ") else text


def main():
    if DESTINATION.exists():
        raise SystemExit("Frozen version already exists. A source change requires a new destination/version.")
    translated,translated_meta=fetch_rows(TRANSLATION)
    keyed,key_meta=fetch_rows(KEY)
    factor_names={1:("E","外向性"),2:("A","宜人性"),3:("C","尽责性"),4:("ES","情绪稳定性"),5:("I","智性／想象")}
    items=[]
    for number in range(1,51):
        original,translation=translated[number][1:3]
        if normalize_english(original)!=normalize_english(keyed[number][1]):
            raise ValueError(f"English text differs between sources at item {number}")
        match=re.fullmatch(r"\(([1-5])([+-])\)",keyed[number][-1])
        if not match:
            raise ValueError(f"Scoring key missing at item {number}")
        factor,sign=int(match.group(1)),match.group(2)
        items.append({"id":f"IPIP{number:02}","source_order":number,"english":original,"zh_Hant":translation,
                      "factor":factor_names[factor][0],"direction":1 if sign=="+" else -1,
                      "score_map":{str(v):v if sign=="+" else 6-v for v in range(1,6)}})
    document={
        "instrument":"IPIP 50-item Big-Five markers","source_version":"1.0.0","frozen_date":"2026-10-26",
        "language":"zh-Hant","translator":"Sih-Ci Jhu","permission":"IPIP public-domain materials; see source permission page",
        "permission_url":PERMISSION,"source_files":[translated_meta,key_meta],
        "usage":"独立、自愿的研究起点；不进入游格计分、不生成MBTI类型。保留原译文，尚未进行简体适配或本项目人群验证。",
        "instructions":"本研究模块自愿参加，可选择不回答。请按通常的自己回答，而不是理想中的自己。",
        "options":[{"value":1,"label":"非常不贴切"},{"value":2,"label":"有些不贴切"},{"value":3,"label":"普通"},{"value":4,"label":"有些贴切"},{"value":5,"label":"非常贴切"}],
        "scoring":"正向题按原值，反向题按6减原值；按原计分键计算各因子的题目平均值。研究主分析使用因子10题完整数据，不做缺失填补；退出和缺失单独报告。",
        "factor_note":"第四因子保持原键的情绪稳定性方向；第五因子保持智性／想象命名，不直接替换成MBTI维度。",
        "factors":[{"id":factor_names[n][0],"name":factor_names[n][1],"item_ids":[x["id"] for x in items if x["factor"]==factor_names[n][0]]} for n in range(1,6)],
        "items":items,
    }
    DESTINATION.parent.mkdir(parents=True,exist_ok=True)
    DESTINATION.write_text(json.dumps(document,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Frozen 50 source items, 5 factors, original translation and verified scoring directions.")


if __name__=="__main__":
    main()
