
(() => {
 const root=document.documentElement;
 const stored=localStorage.getItem('rwz-theme');
 if(stored==='light'||stored==='dark') root.dataset.theme=stored;
 const btn=document.querySelector('[data-theme-toggle]');
 if(btn){
  const update=()=>{const t=root.dataset.theme||'system';btn.textContent=t==='dark'?'☾ Dark':t==='light'?'☀ Light':'◐ System';btn.setAttribute('aria-label','Tema saat ini '+t+'. Klik untuk mengganti tema.');};
  btn.addEventListener('click',()=>{const current=root.dataset.theme||'system';const next=current==='system'?'dark':current==='dark'?'light':'system';if(next==='system')delete root.dataset.theme;else root.dataset.theme=next;localStorage.setItem('rwz-theme',next);update();});
  update();
 }
 document.querySelectorAll('[data-ripple]').forEach(el=>{el.addEventListener('pointerdown',e=>{const r=el.getBoundingClientRect();const dot=document.createElement('span');dot.className='ripple-dot';dot.style.left=(e.clientX-r.left)+'px';dot.style.top=(e.clientY-r.top)+'px';el.appendChild(dot);setTimeout(()=>dot.remove(),550);});});
})();

if('serviceWorker' in navigator && location.protocol==='https:'){window.addEventListener('load',()=>navigator.serviceWorker.register('/sw.js').catch(()=>{}));}
