import {renderPortraitRibbon} from './v4-ribbon.js';

export function renderHome({personas,portraitFor,ribbonPortraitFor,resume,arrow,esc}) {
  return `${renderPortraitRibbon(personas,{portraitFor,ribbonPortraitFor,esc})}
  <section class="hero">
    <img class="hero-world" src="/assets/world-dawn-v1.png" width="1942" height="809" alt="晨光中的岛屿、石径和灯塔，等待不同的玩家踏入" fetchpriority="high">
    <div class="hero-copy">
      <div class="eyebrow">YOUGE · PLAYER ATLAS</div>
      <h1 tabindex="-1">从你的本命游戏，<br><em>认识玩家版的你。</em></h1>
      <p class="hero-description">同一款游戏，也有很多种喜欢。<br>从那些让你留下的瞬间和游玩选择，<br>找到属于你的玩家人格。</p>
      <div class="hero-actions">
        <button class="primary-button" data-action="begin">${resume?'继续上次的旅程':'选一款本命游戏'}${arrow}</button>
        <button class="text-button" data-action="demo">先看一份示例档案${arrow}</button>
      </div>
    </div>
    <div class="hero-stamp"><span>A WORLD<br>OF YOUR OWN</span></div>
  </section>`;
}
