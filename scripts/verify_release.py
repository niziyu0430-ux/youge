"""Run the acceptance suite and write its real result into the delivered package."""

import io
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


class RecordedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.records=[]
    def record(self,test,status):
        self.records.append({'id':test.id(),'description':test.shortDescription() or test.id(),'status':status})
    def addSuccess(self,test):
        super().addSuccess(test);self.record(test,'passed')
    def addFailure(self,test,err):
        super().addFailure(test,err);self.record(test,'failed')
    def addError(self,test,err):
        super().addError(test,err);self.record(test,'error')
    def addSkip(self,test,reason):
        super().addSkip(test,reason);self.record(test,'skipped')


def main():
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    log=io.StringIO()
    result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=RecordedResult).run(suite)
    summary={'status':'passed' if result.wasSuccessful() else 'failed','tests_run':result.testsRun,
             'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
             'scope':'自动检查计算、分支、证据和内容包一致性，不是实际玩家试测或假设验证。','cases':result.records}
    directory=ROOT/'reports';directory.mkdir(exist_ok=True)
    (directory/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 游格内容包实际验收记录','',
           f"执行结果：{'通过' if result.wasSuccessful() else '未通过'}。共{result.testsRun}项自动检查，失败{len(result.failures)}，错误{len(result.errors)}，跳过{len(result.skipped)}。",'',summary['scope'],'',
           '| 检查 | 结果 |','|---|---|']
    lines += [f"| {item['description']} | {item['status']} |" for item in result.records]
    if not result.wasSuccessful():lines += ['', '## 失败详情','', '```text',log.getvalue(),'```']
    lines += ['', '真实理解测试、120人试用和两周重测尚未执行；操作方案见docs/06-research.md。','']
    (directory/'verification.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'},ensure_ascii=False))
    if not result.wasSuccessful():
        print(log.getvalue())
        raise SystemExit(1)


if __name__=='__main__':main()
