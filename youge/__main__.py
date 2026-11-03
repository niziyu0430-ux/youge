"""Command-line access to the reference content engine."""

import argparse
import json
from pathlib import Path
import sys

from .engine import InputError, build_report, compare_reports, load_config
from .render import write_comparison, write_report


def main():
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser=argparse.ArgumentParser(description="游格内容规格参考实现，无网站或外部服务。")
    parser.add_argument("--config",default=None)
    sub=parser.add_subparsers(dest="command",required=True)
    score=sub.add_parser("report",help="从完整答卷生成JSON、Markdown和横向条形图")
    score.add_argument("response")
    score.add_argument("--output",default="reports")
    score.add_argument("--stem",default=None)
    pair=sub.add_parser("compare",help="比较两份同版本原始答卷")
    pair.add_argument("left")
    pair.add_argument("right")
    pair.add_argument("--output",default="reports")
    pair.add_argument("--stem",default="comparison")
    args=parser.parse_args()
    try:
        cfg=load_config(args.config) if args.config else load_config()
        def read(path):
            return json.loads(Path(path).read_text(encoding="utf-8-sig"))
        if args.command=="report":
            report=build_report(read(args.response),cfg)
            stem=args.stem or Path(args.response).stem
            write_report(report,cfg,args.output,stem)
            print(f"已生成：{Path(args.output).resolve()/ (stem+'.md')}")
        else:
            comparison=compare_reports(build_report(read(args.left),cfg),build_report(read(args.right),cfg),cfg)
            write_comparison(comparison,cfg,args.output,args.stem)
            print(f"已生成：{Path(args.output).resolve()/ (args.stem+'.md')}")
    except (InputError,OSError,json.JSONDecodeError) as error:
        parser.exit(2,f"输入错误：{error}\n")


if __name__=="__main__":
    main()
