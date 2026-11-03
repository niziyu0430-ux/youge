/* Art editions affect presentation only; stored answers and core reports stay intact. */
const STORAGE_KEY = 'youge-art-edition';
let edition = 'v2';
let portraits = new Map();
let available = false;

export async function initArt() {
  try {
    const response = await fetch('/assets/personas-v2/preview.json');
    if (!response.ok) throw new Error('Art manifest unavailable');
    const manifest = await response.json();
    if (manifest.status !== 'complete' || manifest.assets.length !== 16 || manifest.assets.some(p => !p.v2?.startsWith('/assets/personas-v2/'))) throw new Error('Art edition incomplete');
    portraits = new Map(manifest.assets.map(p => [p.id, p.v2]));
    available = portraits.size === 16;
  } catch {
    portraits = new Map();
    available = false;
  }
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'v1' || saved === 'v2') edition = saved;
  } catch { /* Choosing an edition still works when browser storage is unavailable. */ }
  if (!available) edition = 'v1';
}

export function artEdition() { return edition; }
export function setArtEdition(value) {
  if (!['v1', 'v2'].includes(value) || value === 'v2' && !available) return false;
  edition = value;
  try { localStorage.setItem(STORAGE_KEY, edition); } catch { /* Keep the in-memory choice. */ }
  return true;
}
export function portraitFor(persona) {
  return edition === 'v2' ? portraits.get(persona.id) || persona.portrait : persona.portrait;
}
export function ribbonPortraitFor(persona) { return `/assets/personas-ribbon/${edition}/${persona.id}.webp`; }
export function styledPersona(persona) { return {...persona, portrait: portraitFor(persona)}; }
export function styledReport(report) { return {...report, persona: styledPersona(report.persona)}; }
export function artControls() {
  return `<div class="art-edition-control" role="group" aria-label="人物图片版本"><span>人物造型</span><button type="button" data-action="set-art" data-edition="v2" aria-pressed="${edition === 'v2'}" ${available ? '' : 'disabled'}>新装 V2</button><button type="button" data-action="set-art" data-edition="v1" aria-pressed="${edition === 'v1'}">原版 V1</button><a href="/wardrobe.html" target="_blank" rel="noopener">新旧对照<span class="sr-only">（在新标签页打开）</span></a></div>`;
}
