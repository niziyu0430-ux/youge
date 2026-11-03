const pauseIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12"/></svg>';
const playIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 10 7-10 7Z"/></svg>';

export function renderPortraitRibbon(personas,{portraitFor,ribbonPortraitFor,heroPortraitFor,esc,large=false}) {
  const group = duplicate => `<div class="persona-ribbon-group" ${duplicate?'aria-hidden="true"':''}>${personas.map(persona=>`
    <button class="ribbon-persona" data-action="persona" data-id="${esc(persona.id)}" ${duplicate?'tabindex="-1"':''}>
      <picture><source srcset="${esc(ribbonPortraitFor(persona))} 320w${large?`, ${esc(heroPortraitFor(persona))} 640w`:''}" sizes="${large?'(max-width: 380px) 176px, (max-width: 700px) 196px, (max-width: 1000px) 260px, 310px':'138px'}" type="image/webp"><img src="${esc(portraitFor(persona))}" width="${large?640:320}" height="${large?960:480}" alt="" decoding="async" loading="eager" fetchpriority="${large&& !duplicate?'auto':'low'}"></picture>
      <span>${esc(persona.name)}</span>
    </button>`).join('')}</div>`;
  return `<section class="persona-ribbon${large?' persona-ribbon-large':''}" aria-label="16位玩家人格画像" data-paused="false">
    <div class="persona-ribbon-viewport"><div class="persona-ribbon-track">${group(false)}${group(true)}</div></div>
    <button class="ribbon-pause" type="button" data-ribbon-toggle aria-label="暂停人物滚动" aria-pressed="false">${pauseIcon}</button>
  </section>`;
}

export function mountPortraitRibbon(container) {
  const ribbon = container.querySelector('.persona-ribbon');
  if (!ribbon) return () => {};
  const track = ribbon.querySelector('.persona-ribbon-track');
  const group = ribbon.querySelector('.persona-ribbon-group');
  const viewport = ribbon.querySelector('.persona-ribbon-viewport');
  const toggle = ribbon.querySelector('[data-ribbon-toggle]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const dialog = document.querySelector('#modal');
  const controller = new AbortController();
  const {signal} = controller;
  let userPaused = false, holding = false;
  let focusFrame;

  const update = () => {
    ribbon.dataset.paused = String(userPaused || holding || document.hidden || Boolean(dialog?.open));
    ribbon.dataset.reducedMotion = String(reducedMotion.matches);
    toggle.hidden = reducedMotion.matches;
    toggle.setAttribute('aria-pressed',String(userPaused));
    toggle.setAttribute('aria-label',userPaused?'继续人物滚动':'暂停人物滚动');
    toggle.innerHTML = userPaused ? playIcon : pauseIcon;
  };
  const resize = () => {
    // One full group is the travel distance. Its trailing gap matches every other gap.
    const distance = group.getBoundingClientRect().width;
    track.style.setProperty('--ribbon-duration',`${distance / 36}s`);
  };
  const observer = new ResizeObserver(resize);
  observer.observe(group);
  const modalObserver = new MutationObserver(update);
  if (dialog) modalObserver.observe(dialog,{attributes:true,attributeFilter:['open']});

  toggle.addEventListener('click',() => { userPaused=!userPaused;update(); },{signal});
  document.addEventListener('visibilitychange',update,{signal});
  reducedMotion.addEventListener('change',update,{signal});
  viewport.addEventListener('pointerdown',event => {if(event.pointerType!=='mouse'){holding=true;update();}},{signal,passive:true});
  const release = () => {if(holding){holding=false;update();}};
  window.addEventListener('pointerup',release,{signal,passive:true});
  window.addEventListener('pointercancel',release,{signal,passive:true});
  ribbon.addEventListener('focusin',event => {
    if (event.target.matches('.ribbon-persona:focus-visible')) {
      ribbon.classList.add('ribbon-keyboard');
      focusFrame=requestAnimationFrame(() => event.target.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'}));
    }
  },{signal});
  ribbon.addEventListener('focusout',event => {
    if (!ribbon.contains(event.relatedTarget)) {
      ribbon.classList.remove('ribbon-keyboard');
      viewport.scrollLeft=0;
    }
  },{signal});
  resize();
  update();
  return () => {
    cancelAnimationFrame(focusFrame);
    controller.abort();
    observer.disconnect();
    modalObserver.disconnect();
  };
}
