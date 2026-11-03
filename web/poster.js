/* Generates a private, local PNG from the same evidence-bound report as the page. */
const W=1080,M=44,P=32;
const FONT='"Microsoft YaHei", "PingFang SC", sans-serif';
const colors={paper:'#f4f1e7',surface:'#fffefa',ink:'#233d33',muted:'#65735f',forest:'#2c5142',line:'#e0e3d4',gold:'#ae7445',sage:'#eaf0e2'};

function font(ctx,size,weight=400){ctx.font=`${weight} ${size}px ${FONT}`;}
function linesFor(ctx,text,width){const lines=[];for(const paragraph of String(text??'').split('\n')){let line='';for(const char of paragraph){if(ctx.measureText(line+char).width>width&&line){lines.push(line);line=char;}else line+=char;}lines.push(line);}return lines;}
function rect(ctx,x,y,w,h,r,fill){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fillStyle=fill;ctx.fill();}
function paragraph(ctx,text,x,y,width,size=25,color=colors.ink,weight=400){font(ctx,size,weight);ctx.fillStyle=color;const lineHeight=size*1.75;const lines=linesFor(ctx,text,width);for(const line of lines){ctx.fillText(line,x,y+size);y+=lineHeight;}return y;}
function measure(ctx,text,width,size=25,weight=400){font(ctx,size,weight);return linesFor(ctx,text,width).length*size*1.75;}
function score(value){return value===null?'资料不足':Number(value).toFixed(1).replace(/\.0$/,'');}
function evidenceSummary(claim,report){const refs=claim.evidence_refs||[];const counts={};const pieces=[];for(const ref of refs){const e=report.evidence[ref];if(!e)continue;if(e.source==='core'){const key=e.question_id.slice(0,3);counts[key]=(counts[key]||0)+1;if(counts[key]<=2)pieces.push(`${e.context}：${e.label}`);}else if(e.source==='followup')pieces.push(e.label);}return pieces.join('；');}
async function loadLandscape(){const image=new Image();image.src='/assets/world-dawn-v1.png';try{await image.decode();return image;}catch{return null;}}

export async function makePoster(report){
 const scratch=document.createElement('canvas');scratch.width=W;scratch.height=100;
 const measureCtx=scratch.getContext('2d');
 const inner=W-2*M-2*P;
 const blocks=[];
 function add(title,paragraphs){const entries=paragraphs.filter(p=>p.text).map(p=>({size:25,color:colors.ink,...p}));let height=92;for(const entry of entries)height+=measure(measureCtx,entry.text,inner,entry.size,entry.weight||400)+entry.gapAfter+12;blocks.push({kind:'text',title,entries,height:height+20});}
 for(const [i,claim]of report.insights.entries()){
  add(`0${i+1} · 从选择中留下的线索`,[{text:claim.text,gapAfter:12},{text:'依据：'+evidenceSummary(claim,report),size:18,color:colors.muted,gapAfter:0}]);
 }
 if(!report.insights.length)add('这次先留下已有的记录',[{text:'当前证据还不足以展开具体判断。保留已经明确的选择，不急着把它们拼成确定的人格。',gapAfter:0}]);
 blocks.push({kind:'axes',height:780});
 const taste=[];
 for(const [i,g]of report.response.favorites.entries()){
  const labels=g.attractions.map(t=>report.evidence[`favorite:${i}:${t}`]?.label).filter(Boolean);
  taste.push({text:`《${g.title}》 · ${g.experience==='yes'?'亲自体验过':g.experience==='no'?'未亲自体验':'亲玩状态未确认'}\n${labels.join('、')||'吸引点尚未填写'}`,size:22,gapAfter:14});
 }
 taste.push(...report.taste.claims.map(c=>({text:c.text,gapAfter:12})),...report.taste.alignment.map(c=>({text:c.text,size:22,color:colors.muted,gapAfter:10})));
 if(!report.taste.claims.length)taste.push({text:report.taste.note,gapAfter:0});
 add('喜欢之间的共同线索',taste);
 add('容易让你留下的体验',[
  ...report.enjoyments.map(c=>({text:'· '+c.text,gapAfter:8})),
  ...(report.supplement.length?[{text:'你另外提到了：'+report.supplement.map(c=>c.text).join('、'),size:22,color:colors.muted,gapAfter:0}]:[]),
  ...(!report.enjoyments.length&&!report.supplement.length?[{text:'这部分暂时没有足够的明确资料。',gapAfter:0}]:[])
 ]);
 add('值得提前留意的体验',report.drains.length?report.drains.map(c=>({text:c.text,gapAfter:12})):[{text:'目前没有明确的回避或负面体验资料，不从低分补写消耗点。',size:23,color:colors.muted,gapAfter:0}]);
 add('一起玩之前，先说好这些',report.advice.map(a=>({text:`${a.title}${a.basis==='needs_confirmation'?'（尚待确认）':''}\n${a.text}`,size:23,gapAfter:18})));
 add('留给游戏外的自己',[
  {text:'以下仅是自我核对，不计分，也不直接推断现实人格。',size:20,color:colors.muted,gapAfter:12},
  ...report.self_checks.map(c=>({text:c.text,gapAfter:14}))
 ]);
 font(measureCtx,48,600);const titleHeight=linesFor(measureCtx,report.display.title,inner).length*76;
 const headerHeight=310+titleHeight;
 const totalHeight=Math.ceil(headerHeight+36+blocks.reduce((sum,b)=>sum+b.height+24,0)+180);
 if(totalHeight>30000)throw new Error('档案内容过长，请使用打印保存完整内容');
 const canvas=document.createElement('canvas');canvas.width=W;canvas.height=totalHeight;
 const ctx=canvas.getContext('2d');ctx.textBaseline='alphabetic';ctx.fillStyle=colors.paper;ctx.fillRect(0,0,W,totalHeight);
 const landscape=await loadLandscape();
 if(landscape){const s=Math.max(W/landscape.width,headerHeight/landscape.height);ctx.save();ctx.beginPath();ctx.rect(0,0,W,headerHeight);ctx.clip();ctx.drawImage(landscape,(W-landscape.width*s)/2,0,landscape.width*s,landscape.height*s);ctx.restore();}
 const wash=ctx.createLinearGradient(0,0,W,0);wash.addColorStop(0,'rgba(246,241,224,.98)');wash.addColorStop(.65,'rgba(246,241,224,.9)');wash.addColorStop(1,'rgba(246,241,224,.2)');ctx.fillStyle=wash;ctx.fillRect(0,0,W,headerHeight);
 let y=55;
 y=paragraph(ctx,'游格  /  PLAYER ATLAS',M+P,y,inner,23,colors.gold,500)+22;
 if(report.fictional)y=paragraph(ctx,'虚构示例档案 · 并非真实玩家结果',M+P,y,inner,18,colors.gold)+14;
 y=paragraph(ctx,`${report.display_name}的玩家档案`,M+P,y,inner,21,colors.muted)+14;
 y=paragraph(ctx,report.display.title,M+P,y,inner,48,colors.ink,600)+14;
 y=paragraph(ctx,report.display.one_line,M+P,y,inner,25,colors.muted)+16;
 if(report.behavior_tags.length)paragraph(ctx,report.behavior_tags.map(t=>t.text).join('  ·  '),M+P,y,inner,18,colors.forest);
 y=headerHeight+36;
 for(const block of blocks){
  rect(ctx,M,y,W-2*M,block.height,23,colors.surface);
  if(block.kind==='axes'){
   paragraph(ctx,'八个偏好坐标',M+P,y+27,inner,30,colors.ink,600);
   const bx=M+P+156,bw=inner-260;
   font(ctx,16);ctx.fillStyle=colors.muted;for(const tick of [0,25,50,75,100])ctx.fillText(String(tick),bx+bw*tick/100-8,y+108);
   let rowY=y+133;
   for(const row of Object.values(report.scores)){
    paragraph(ctx,row.name,M+P,rowY-9,145,22,colors.muted);
    rect(ctx,bx,rowY+1,bw,13,6,colors.sage);
    if(row.score!==null&&row.score>0)rect(ctx,bx,rowY+1,bw*row.score/100,13,6,colors.forest);
    paragraph(ctx,score(row.display_score),bx+bw+17,rowY-13,100,21,colors.ink,500);
    paragraph(ctx,`${row.valid_n}/4题`,bx+bw+17,rowY+18,100,14,colors.muted);
    rowY+=67;
   }
   paragraph(ctx,'0—100问卷偏好分，不是能力分或在人群中的排名。',M+P,y+block.height-65,inner,18,colors.muted);
  }else{
   paragraph(ctx,block.title,M+P,y+26,inner,29,colors.ink,600);
   let contentY=y+89;
   for(const entry of block.entries){contentY=paragraph(ctx,entry.text,M+P,contentY,inner,entry.size,entry.color,entry.weight||400)+entry.gapAfter+12;}
  }
  y+=block.height+24;
 }
 paragraph(ctx,'游格 · 让每一种玩法，都有自己的坐标。',M+P,y+7,inner,23,colors.forest,500);
 paragraph(ctx,`原创探索版，模型及称号仍待真实样本验证。游戏偏好不等于现实人格。\n题库 ${report.versions.instrument} · 这张图仅在本机生成。`,M+P,y+62,inner,17,colors.muted);
 return await new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(new Error('浏览器未能导出图片')),'image/png'));
}
