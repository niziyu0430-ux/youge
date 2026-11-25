/* Reader-facing essays; evidence and scoring records remain outside the presentation. */
export function renderPersonalityReport(r,{esc,arrow}){
 const profile=r.personality_profile;
 return `<section class="report-shell report-essay">
  <div class="report-toolbar"><span class="quiet-label">YOUGE · YOUR PLAYER PORTRAIT</span></div>
  ${r.fictional?'<div class="sample-banner notice sample"><span>虚构示例 · 用于展示格式，不是真实玩家数据。</span><button data-action="begin-fresh">开始自己的测试</button></div>':''}
  <article class="persona-cover">
   <div class="cover-copy"><div class="result-persona-label">你的玩家人格</div><div class="cover-kicker">${esc(r.display_name)}，你是</div>
    <h1 tabindex="-1">${esc(r.persona.name)}</h1><p class="report-one-line">${esc(r.one_line)}</p>
    <div class="pill-group personality-traits">${profile.traits.map(t=>`<span class="pill">${esc(t)}</span>`).join('')}</div>
    <p class="cover-game">这次，从《${esc(r.game.title)}》开始认识自己。</p>
    <div class="result-actions"><button class="primary-button" data-action="poster">收好完整档案${arrow}</button><button class="secondary-button" data-action="compare">和另一位玩家对照</button></div>
   </div><div class="cover-figure"><img src="${r.persona.portrait}" alt="${esc(r.persona.name)}的专属3D卡通角色" fetchpriority="high"></div>
  </article>
  <div class="personality-reading">${r.report_sections.map((s,i)=>`<section class="report-section personality-chapter" aria-labelledby="portrait-${s.id}"><div class="chapter-heading"><span class="chapter-index">0${i+1}</span><h2 id="portrait-${s.id}">${esc(s.title)}</h2></div><div class="chapter-prose">${i===0?`<blockquote class="personality-credo">${esc(profile.credo)}</blockquote>`:''}${s.paragraphs.map(p=>`<p>${esc(p)}</p>`).join('')}</div></section>`).join('')}</div>
  <div class="report-end"><div class="button-row"><button class="primary-button" data-action="poster">保存完整长图${arrow}</button><button class="secondary-button" data-action="export">导出答卷</button><button class="text-button" data-action="rename">留个称呼</button><button class="text-button" data-action="print">打印 / PDF</button><button class="text-button" data-action="begin-fresh">再开启一次</button></div></div>
  <p class="report-fineprint">${esc(r.scope_note)} · 侧写 ${esc(r.versions.report_rules)}</p>
 </section>`;
}

export function renderPersonaDescription(p,{esc,arrow,header}){
 const profile=p.personality_profile;
 return `${header(p.name)}<div class="persona-detail-intro"><img src="${p.portrait}" alt="${esc(p.name)}"><div><p class="persona-detail-line">${esc(profile.headline)}</p><div class="pill-group">${profile.traits.map(t=>`<span class="pill">${esc(t)}</span>`).join('')}</div><blockquote>${esc(profile.credo)}</blockquote></div></div><div class="persona-detail-prose"><h3>你的性格底色</h3>${profile.inner_world.map(t=>`<p>${esc(t)}</p>`).join('')}<h3>与你相处的方式</h3>${profile.with_others.map(t=>`<p>${esc(t)}</p>`).join('')}</div><div class="modal-actions"><button class="primary-button" data-action="close-and-library">选择我的本命游戏${arrow}</button></div>`;
}
