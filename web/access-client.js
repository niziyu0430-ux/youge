// Intentionally lives only in this document's JS module memory.
// Never put access tokens or the shared password in cookies or browser storage.
let accessToken = null;

export function setAccessToken(value) {
  if (typeof value !== 'string' || value.length < 32) throw new Error('登录验证没有完成，请重新输入密码。');
  accessToken = value;
}

export function clearAccessToken() { accessToken = null; }

export async function authorizedFetch(url, options = {}) {
  if (!accessToken) {
    window.location.reload();
    throw new Error('请重新输入访问密码。');
  }
  const headers = new Headers(options.headers || {});
  headers.set('Authorization', `Bearer ${accessToken}`);
  const response = await fetch(url, {...options, headers, cache:'no-store', credentials:'omit'});
  if (response.status === 401) {
    accessToken = null;
    window.location.reload();
    throw new Error('登录已结束，请重新输入访问密码。');
  }
  return response;
}

export async function logout() {
  const token = accessToken;
  accessToken = null;
  try {
    if (token) await fetch('/api/access/logout', {
      method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`},
      body:'{}', credentials:'omit', cache:'no-store',
    });
  } finally { window.location.reload(); }
}

window.addEventListener('pagehide', () => {
  const token=accessToken;
  accessToken=null;
  if (token) void fetch('/api/access/logout', {
    method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`},
    body:'{}', keepalive:true, credentials:'omit', cache:'no-store',
  }).catch(()=>{});
});
window.addEventListener('pageshow', event => { if (event.persisted) window.location.reload(); });
