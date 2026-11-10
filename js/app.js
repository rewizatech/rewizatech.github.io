(() => {
  const root = document.documentElement;
  try {
    const stored = localStorage.getItem('rwz-theme');
    if (stored === 'light' || stored === 'dark') {
      root.dataset.theme = stored;
    }
  } catch (e) {}

  const btn = document.querySelector('[data-theme-toggle]');
  if (btn) {
    const update = () => {
      const t = root.dataset.theme || 'system';
      btn.textContent = t === 'dark' ? '☾ Dark' : t === 'light' ? '☀ Light' : '◐ System';
      btn.setAttribute('aria-label', 'Tema saat ini ' + t + '. Klik untuk mengganti tema.');
    };
    btn.addEventListener('click', () => {
      const current = root.dataset.theme || 'system';
      const next = current === 'system' ? 'dark' : current === 'dark' ? 'light' : 'system';
      if (next === 'system') {
        delete root.dataset.theme;
      } else {
        root.dataset.theme = next;
      }
      try {
        localStorage.setItem('rwz-theme', next);
      } catch (e) {}
      update();
    });
    update();
  }

  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reducedMotion) {
    document.querySelectorAll('.button, [data-ripple]').forEach(el => {
      el.addEventListener('pointerdown', e => {
        const r = el.getBoundingClientRect();
        const dot = document.createElement('span');
        dot.className = 'ripple-dot';
        dot.style.left = (e.clientX - r.left) + 'px';
        dot.style.top = (e.clientY - r.top) + 'px';
        el.appendChild(dot);
        setTimeout(() => dot.remove(), 550);
      });
    });
  }

  document.querySelectorAll('[data-copy-email]').forEach(copyBtn => {
    copyBtn.addEventListener('click', async () => {
      const email = copyBtn.getAttribute('data-copy-email') || 'rewizatech@gmail.com';
      const status = document.querySelector('[data-copy-status]');
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(email);
        } else {
          const tmp = document.createElement('input');
          tmp.value = email;
          document.body.appendChild(tmp);
          tmp.select();
          document.execCommand('copy');
          tmp.remove();
        }
        if (status) {
          status.textContent = '✓ Email disalin!';
          setTimeout(() => { status.textContent = ''; }, 2500);
        }
      } catch (e) {
        if (status) {
          status.textContent = email;
        }
      }
    });
  });
})();

if (
  'serviceWorker' in navigator &&
  (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')
) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
}
