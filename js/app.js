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

  const backToTopBtn = document.querySelector('[data-back-to-top]');
  if (backToTopBtn) {
    let isTicking = false;
    const onScroll = () => {
      if (!isTicking) {
        window.requestAnimationFrame(() => {
          if (window.scrollY > 280) {
            backToTopBtn.classList.add('is-visible');
          } else {
            backToTopBtn.classList.remove('is-visible');
          }
          isTicking = false;
        });
        isTicking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    backToTopBtn.addEventListener('click', () => {
      const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({
        top: 0,
        behavior: reduceMotion ? 'auto' : 'smooth'
      });
    });
  }

  // App Catalog Interactive Filtering
  const filterPills = document.querySelectorAll('[data-app-filter]');
  const appCards = document.querySelectorAll('.app-row-card[data-category]');
  if (filterPills.length && appCards.length) {
    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const target = pill.getAttribute('data-app-filter');
        filterPills.forEach(p => {
          const isActive = p === pill;
          p.classList.toggle('is-active', isActive);
          p.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });
        appCards.forEach(card => {
          const cat = card.getAttribute('data-category');
          if (target === 'all' || cat === target) {
            card.classList.remove('is-hidden');
          } else {
            card.classList.add('is-hidden');
          }
        });
      });
    });
  }
})();

if (
  'serviceWorker' in navigator &&
  (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')
) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
}
