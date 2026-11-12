const CACHE = 'rewiza-static-v6';
const CORE = [
  '/',
  '/apps/',
  '/apps/kasir-laris/',
  '/about/',
  '/privacy-policy/',
  '/privacy-policy/kasir-laris.html',
  '/privacy-policy/utility.html',
  '/terms/',
  '/support/',
  '/faq/',
  '/css/style.css',
  '/js/app.js',
  '/manifest.json',
  '/data/apps.json',
  '/favicon.ico',
  '/assets/icons/favicon.svg',
  '/assets/icons/favicon-32x32.png',
  '/assets/icons/apple-touch-icon.png',
  '/assets/brand/logo-transparent.png',
  '/assets/brand/og-image.png',
  '/assets/icons/icon-192.png',
  '/assets/icons/icon-512.png',
  '/assets/kasir-laris.png',
  '/assets/icons/smart-compress.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  const isHtml =
    req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html') ||
    url.pathname.endsWith('/') ||
    url.pathname.endsWith('.html');

  if (isHtml) {
    event.respondWith(
      fetch(req)
        .then(res => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy));
          }
          return res;
        })
        .catch(() => caches.match(req).then(r => r || caches.match('/')))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then(cached =>
      cached ||
      fetch(req)
        .then(res => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy));
          }
          return res;
        })
        .catch(() => caches.match('/'))
    )
  );
});
