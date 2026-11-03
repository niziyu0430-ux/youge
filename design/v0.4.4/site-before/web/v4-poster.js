/* Local essay rendering: the same two chapters as the reader-facing result. */
const W=1080,M=48,P=36;
const C={paper:'#f6f3eb',surface:'#fffefa',ink:'#233d33',muted:'#6a796c',forest:'#2c5142',line:'#e0e5d7',gold:'#ae7445'};
const FONT='"Microsoft YaHei", "PingFang SC", sans-serif';
function font(ctx,size,weight=400){ctx.font=`${weight} ${size}px ${FONT}`;}
function lines(ctx,text,width){const result=[];for(const para of String(text??'').split('\n')){let line='';for(const char of para){if(line&&ctx.measureText(line+char).width>width){result.push(line);line=char;}else line+=char;}result.push(line);}return result;}
function height(ctx,text,width,size=25,weight=400){font(ctx,size,weight);return lines(ctx,text,width).length*size*1.7;}
function text(ctx,value,x,y,width,size=25,color=C.ink,weight=400){font(ctx,size,weight);ctx.fillStyle=color;ctx.textBaseline='top';for(const line of lines(ctx,value,width)){ctx.fillText(line,x,y);y+=size*1.7;}return y;}
function box(ctx,x,y,w,h,r,fill){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fillStyle=fill;ctx.fill();}
async function picture(src){const img=new Image();img.src=src;await img.decode();return img;}

export async function makePoster(r){
 const scratch=document.createElement('canvas'),m=scratch.getContext('2d'),inner=W-2*M-2*P;
 const sections=[];
 function add(title,paragraphs,credo){const parts=paragraphs.map(value=>({value,size:25,color:C.ink,gap:26}));if(credo)parts.unshift({value:credo,size:29,color:C.gold,gap:28});let h=100;for(const p of parts)h+=height(m,p.value,inner,p.size)+p.gap;sections.push({title,parts,h:h+10});}
 r.report_sections.forEach((s,i)=>add(`0${i+1} · ${s.title}`,s.paragraphs,i===0?r.personality_profile.credo:null));
 const profile=r.personality_profile;
 const textBottom=82+height(m,'游格 / PLAYER ATLAS',530,24,600)+28+(r.fictional?height(m,'虚构示例 · 非真实玩家数据',530,19)+16:0)+height(m,r.display_name+'，你是',530,25)+14+height(m,r.persona.name,540,57,600)+20+height(m,r.one_line,520,26)+25;
 const header=Math.ceil(Math.max(540,textBottom)+height(m,`本命作品 · ${r.game.title}`,inner,25,600)+12+height(m,profile.traits.join('  /  '),inner,22)+45);
 const total=Math.ceil(header+32+sections.reduce((sum,s)=>sum+s.h+24,0)+180);
 if(total>30000)throw new Error('档案内容过长，请使用打印保存。');
 const canvas=document.createElement('canvas');canvas.width=W;canvas.height=total;
 const ctx=canvas.getContext('2d');ctx.fillStyle=C.paper;ctx.fillRect(0,0,W,total);
 const img=await picture(r.persona.portrait);
 box(ctx,M,35,W-2*M,header-35,28,C.surface);
 ctx.save();ctx.beginPath();ctx.roundRect(W-365,76,280,450,140);ctx.fillStyle='#eaf0e2';ctx.fill();ctx.restore();
 const scale=Math.min(350/img.width,480/img.height);ctx.drawImage(img,W-395+(350-img.width*scale)/2,60+(480-img.height*scale)/2,img.width*scale,img.height*scale);
 let y=text(ctx,'游格 / PLAYER ATLAS',M+P,82,530,24,C.gold,600)+28;
 if(r.fictional)y=text(ctx,'虚构示例 · 非真实玩家数据',M+P,y,530,19,C.gold)+16;
 y=text(ctx,r.display_name+'，你是',M+P,y,530,25,C.muted)+14;
 y=text(ctx,r.persona.name,M+P,y,540,57,C.ink,600)+20;
 y=text(ctx,r.one_line,M+P,y,520,26)+25;
 y=Math.max(y,540);
 y=text(ctx,`本命作品 · ${r.game.title}`,M+P,y,inner,25,C.gold,600)+12;
 y=text(ctx,profile.traits.join('  /  '),M+P,y,inner,22,C.muted)+16;
 y=header+32;
 for(const section of sections){box(ctx,M,y,W-2*M,section.h,24,C.surface);let sy=text(ctx,section.title,M+P,y+30,inner,29,C.ink,600)+26;for(const p of section.parts)sy=text(ctx,p.value,M+P,sy,inner,p.size,p.color)+p.gap;y+=section.h+24;}
 y=text(ctx,r.scope_note,M+P,y+15,inner,18,C.muted)+15;
 text(ctx,`游格原创玩家档案 · 性格侧写 ${r.versions.report_rules}`,M+P,y,inner,17,C.gold);
 return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(new Error('长图没有生成，请重试。')),'image/png'));
}
