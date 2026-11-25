import {setAccessToken,clearAccessToken,authorizedFetch} from './access-client.js';

const form=document.querySelector('#access-form');
const password=document.querySelector('#access-password');
const submit=document.querySelector('#access-submit');
const message=document.querySelector('#access-message');
const showPassword=document.querySelector('#show-password');
let busy=false;

showPassword.addEventListener('click',()=>{
  const show=password.type==='password';
  password.type=show?'text':'password';
  showPassword.setAttribute('aria-pressed',String(show));
  showPassword.setAttribute('aria-label',show?'隐藏密码':'显示密码');
});

async function mountApplication(payload) {
  if (payload.module!=='/v4.js') throw new Error('页面没有加载成功，请刷新后重新登录。');
  const parsed=new DOMParser().parseFromString(payload.html,'text/html');
  parsed.querySelectorAll('script').forEach(script=>script.remove());
  await Promise.all([...parsed.head.querySelectorAll('link[rel="stylesheet"]')].map(style=>new Promise((resolve,reject)=>{
    const link=document.createElement('link');link.rel='stylesheet';link.href=style.getAttribute('href');
    link.onload=resolve;link.onerror=()=>reject(new Error('页面样式没有加载成功，请重试。'));
    document.head.append(link);
  })));
  document.title=parsed.title;
  password.value='';
  document.body.className=parsed.body.className;
  document.body.replaceChildren(...[...parsed.body.childNodes].map(node=>document.importNode(node,true)));
  history.replaceState(null,'','/#home');
  await import(payload.module);
  window.scrollTo({top:0,behavior:'instant'});
}

form.addEventListener('submit',async event=>{
  event.preventDefault();if(busy)return;
  message.textContent='';message.hidden=true;
  if (!password.value) {password.focus();return;}
  busy=true;submit.disabled=true;submit.setAttribute('aria-busy','true');submit.querySelector('span').textContent='正在验证…';
  try {
    const response=await fetch('/api/access/login',{
      method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:password.value}),
      credentials:'omit',cache:'no-store',
    });
    const data=await response.json();
    if(!response.ok)throw new Error(data.error||'暂时无法登录，请稍后重试。');
    setAccessToken(data.access_token);
    const shellResponse=await authorizedFetch('/api/access/app-shell');
    if(!shellResponse.ok)throw new Error('页面没有加载成功，请稍后重试。');
    await mountApplication(await shellResponse.json());
  }catch(error){
    clearAccessToken();
    if(!form.isConnected){window.location.reload();return;}
    message.textContent=error.message||'连接没有完成，请稍后重试。';message.hidden=false;
    submit.querySelector('span').textContent='解锁我的玩家档案';
    password.focus();password.select();
  }finally{
    busy=false;submit.disabled=false;submit.removeAttribute('aria-busy');
  }
});
