const grid = document.querySelector('#portraits');
const note = document.querySelector('#view-note');
const zoom = document.querySelector('#zoom');
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const notes = {
  samples: '首轮四位与修订后的细节，点击人物可放大。',
  compare: '左侧 V1 原版，右侧 V2 样张；点击可看大图。',
  lineup: '16位 V2 新造型，点击任一人物可放大查看新旧对照。',
  originals: '完整的16位 V1 原版。所有原文件均保留。'
};
let data, mode = 'lineup';
const swatches = p => `<div class="mini-swatches" aria-hidden="true">${p.colors.map(c => `<i style="background:${c}"></i>`).join('')}</div>`;
function picture(p, version) {
  return `<button class="figure-button" data-zoom="${p.id}" data-version="${version}" type="button" aria-label="放大${esc(p.name)} ${version.toUpperCase()}${version === 'v2' ? '新造型' : '原版'}"><span class="image-version ${version === 'v2' ? 'new' : ''}">${version === 'v2' ? 'V2 · 新装' : 'V1 · 原版'}</span><img src="${p[version]}" alt="${esc(p.name)}${version === 'v2' ? '换装新造型' : '原版人物'}" width="1024" height="1536" loading="lazy"></button>`;
}
function copy(p, isNew) {
  return `<div class="card-copy"><h2>${esc(p.name)}</h2>${isNew ? `<p class="palette-line">${p.palette.map(esc).join(' · ')}</p><p class="outfit-line">${esc(p.silhouette)}<br>${esc(p.footwear)}</p>${swatches(p)}` : `<p class="palette-line">原版造型 · 完整保留</p>`}</div>`;
}
function render() {
  const focus = (data.focus_ids || []).map(id => data.assets.find(p => p.id === id)).filter(Boolean);
  const list = mode === 'samples' ? focus : data.assets;
  document.querySelectorAll('[data-mode]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
  grid.className = mode === 'compare' ? 'comparison-list' : `portrait-grid ${mode === 'lineup' || mode === 'originals' ? 'lineup' : ''}`;
  grid.innerHTML = list.map(p => {
    if (mode === 'compare') return `<article class="compare-card"><header><h2>${esc(p.name)}</h2></header><div class="compare-figures">${picture(p, 'v1')}${picture(p, 'v2')}</div><div class="card-copy"><p class="palette-line">${p.palette.map(esc).join(' · ')}</p><p class="outfit-line">${esc(p.silhouette)}<br>${esc(p.footwear)}</p></div></article>`;
    const version = mode !== 'originals' && p.sample ? 'v2' : 'v1';
    return `<article class="portrait-card">${picture(p, version)}${copy(p, version === 'v2')}</article>`;
  }).join('');
  note.textContent = notes[mode];
}
document.querySelector('.view-buttons').addEventListener('click', event => {
  const button = event.target.closest('[data-mode]');
  if (!button || !data) return;
  mode = button.dataset.mode;
  render();
});
grid.addEventListener('click', event => {
  const button = event.target.closest('[data-zoom]');
  if (!button) return;
  const p = data.assets.find(p => p.id === button.dataset.zoom);
  if (!p) return;
  document.querySelector('#zoom-title').textContent = p.name;
  const versions = p.sample ? ['v1', 'v2'] : ['v1'];
  const body = document.querySelector('#zoom-body');
  body.classList.toggle('single', !p.sample);
  body.innerHTML = versions.map(v => `<figure><figcaption>${v === 'v2' ? 'V2 · 新造型' : 'V1 · 原版'}</figcaption><img src="${p[v]}" alt="${esc(p.name)} ${v.toUpperCase()}全身图" width="1024" height="1536"></figure>`).join('');
  zoom.showModal();
});
document.querySelector('#zoom-close').addEventListener('click', () => zoom.close());
zoom.addEventListener('click', event => { if (event.target === zoom) { const rect = zoom.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) zoom.close(); } });
try {
  const response = await fetch('/assets/personas-v2/preview.json');
  if (!response.ok) throw new Error('preview configuration unavailable');
  data = await response.json();
  document.querySelector('#palette-grid').innerHTML = data.assets.map(p => `<article class="palette-item"><div class="palette-name"><h3>${esc(p.name)}</h3>${p.sample ? '<span class="sample-tag">V2</span>' : ''}</div><div class="palette-stripe" aria-hidden="true">${p.colors.map(c => `<span style="background:${c}"></span>`).join('')}</div><p>${p.palette.map(esc).join(' / ')}</p><p>${esc(p.period)}</p></article>`).join('');
  render();
} catch (error) {
  grid.innerHTML = '<p class="error">人物暂时没有加载成功，请确认本地服务已启动后刷新页面。</p>';
  note.textContent = '加载失败。';
}
