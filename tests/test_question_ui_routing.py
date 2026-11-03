"""Regression: Terraria's T-prefixed authored IDs are formal questions, never ties."""
from pathlib import Path
import json
import shutil
import subprocess
import unittest
from youge import v05

ROOT=Path(__file__).resolve().parents[1]


class QuestionUIRoutingTests(unittest.TestCase):
    def test_all_real_authored_variants_and_shared_questions_are_not_supplements(self):
        items=[{'id':v['id'],'scope':'anchor','order':s['number']}
               for p in v05.bank()['packs'] for s in p['slots'] for v in s['variants']]
        items += [{'id':q['id'],'scope':'cross','order':i} for i,q in enumerate(v05.bank()['shared_questions'],13)]
        node=shutil.which('node')
        self.assertIsNotNone(node,'Node is needed to check the actual frontend module')
        code="""
import fs from 'node:fs';
const text=fs.readFileSync('web/v4-question-kind.js','utf8');
const {isSupplementaryQuestion}=await import('data:text/javascript;base64,'+Buffer.from(text).toString('base64'));
const items=JSON.parse(fs.readFileSync(0,'utf8'));
for(const q of items)if(isSupplementaryQuestion(q))throw new Error('Formal question misclassified: '+q.id);
for(const q of [{id:'T01.legacy',scope:'cross',order:17},{id:'T02.v05.current',scope:'cross',order:18}]){
 if(!isSupplementaryQuestion(q))throw new Error('Actual tie ignored: '+q.id);
}
for(const q of [{id:'T01',scope:'anchor',order:1},{id:'X13',scope:'cross',order:13},{id:'T01',scope:'cross',order:1}]){
 if(isSupplementaryQuestion(q))throw new Error('ID prefix incorrectly decides kind');
}
"""
        result=subprocess.run([node,'--input-type=module','-e',code],input=json.dumps(items),
                              text=True,cwd=ROOT,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_real_frontend_saves_and_advances_terraria_formal_answers_and_actual_ties(self):
        items=v05.questions('steam-105600')['questions']
        code=r"""
import fs from 'node:fs';
import vm from 'node:vm';
const module=fs.readFileSync('web/v4-question-kind.js','utf8');
const {isSupplementaryQuestion}=await import('data:text/javascript;base64,'+Buffer.from(module).toString('base64'));
const source=fs.readFileSync('web/v4.js','utf8').replace(/^import .*\r?\n/gm,'').replace(/^init\(\);\s*$/m,'');
const data=JSON.parse(fs.readFileSync(0,'utf8')),stored=new Map(),timers=[];
const context=vm.createContext({
 isSupplementaryQuestion,structuredClone,console,
 document:{addEventListener(){},querySelector(){return {addEventListener(){}};}},
 localStorage:{getItem:k=>stored.get(k)??null,setItem:(k,v)=>stored.set(k,v)},
 window:{scrollY:0,scrollTo(){}},requestAnimationFrame:fn=>fn(),
 setTimeout:fn=>timers.push(fn),clearTimeout(){}
});
vm.runInContext(source,context);
context.fixture=data;
vm.runInContext(`
 render=()=>{};setView=view=>{state.view=view;};generate=()=>{state.generated=true;};
 cfg={rules:{report_only_question_ids:[]}};
 state.draft={versions:{instrument:'0.5.0'},answers:{},extra_answers:[],completed:false};
 state.view='quiz';state.questions=fixture;state.qIndex=0;
 state.questions.push({id:'T01.v05.regression',scope:'cross',order:17,options:['A','B','C','D'].map(id=>({id}))});
 save();
 if(pausedCopy().extraQuestions.length!==1)throw Error('Formal T questions copied as supplements');
 answer('A');
`,context);
let state=vm.runInContext('JSON.parse(JSON.stringify(state))',context);
if(state.draft.answers[data[0].id]!=='A'||state.draft.extra_answers.length!==0)throw Error('Formal answer went to supplementary answers');
for(const fn of timers.splice(0))fn();
if(vm.runInContext('state.qIndex',context)!==1)throw Error('Formal answer did not advance');
let saved=JSON.parse(stored.get('youge-v04-draft'));
if(saved.extraQuestions.length!==0)throw Error('Formal questions persisted as supplements');
vm.runInContext(`
 state.questions.push({id:'T01.v05.regression',scope:'cross',order:17,options:['A','B','C','D'].map(id=>({id}))});
 state.qIndex=16;busy=false;answer('C');
`,context);
for(const fn of timers.splice(0))fn();
state=vm.runInContext('JSON.parse(JSON.stringify(state))',context);
if(state.draft.extra_answers[0]?.answer!=='C'||!state.generated)throw Error('Actual tie did not save or generate report');
if(Object.keys(state.draft.answers).length!==1)throw Error('Tie incorrectly became a formal answer');
"""
        result=subprocess.run([shutil.which('node'),'--input-type=module','-e',code],
                              input=json.dumps(items),text=True,cwd=ROOT,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':unittest.main()
