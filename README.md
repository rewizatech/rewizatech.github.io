# Rewiza Tech Official Website

Repositori ini berisi kode sumber dan aset untuk situs web resmi **Rewiza Tech** ([rewizatech.github.io](https://rewizatech.github.io)).

Situs ini berfungsi sebagai portal informasi resmi mengenai profil studio pengembang, katalog aplikasi Android, pusat kebijakan privasi (*privacy policy*), tanya-jawab (*FAQ*), serta layanan bantuan dan dukungan (*support*).

---

## 📱 Fokus Studio & Produk

Rewiza Tech berfokus pada pengembangan aplikasi Android yang ringan, efisien, offline-first, dan dapat diandalkan untuk kebutuhan sehari-hari maupun UMKM:
- **Kasir Laris POS:** Solusi pencatatan penjualan dan manajemen kasir offline-first untuk UMKM.
- **Utilitas Android:** Aplikasi produktivitas dan utilitas digital praktis.

---

## 📂 Struktur Repositori

- `index.html` — Halaman utama (desain split-screen responsif & app shell).
- `/apps/` — Katalog aplikasi dan changelog rilis.
  - `/apps/kasir-laris/` — Detail aplikasi dan panduan Kasir Laris POS.
- `/about/` — Profil developer, visi studio, dan standar kualitas.
- `/privacy-policy/` — Pusat Kebijakan Privasi resmi untuk kepatuhan Google Play Store.
  - `/privacy-policy/kasir-laris.html` — Kebijakan privasi Kasir Laris POS.
  - `/privacy-policy/utility.html` — Kebijakan privasi aplikasi utilitas.
- `/terms/` — Syarat dan ketentuan penggunaan layanan.
- `/support/` — Pusat bantuan, kontak WhatsApp, dan email resmi.
- `/faq/` — Pertanyaan yang sering diajukan seputar aplikasi dan penyimpanan data lokal.
- `/assets/` — Aset visual, logo brand, dan ikon PWA.
- `/css/` — Stylesheet CSS mandiri (Dark/Light theme switch).
- `/js/` — Skrip interaksi tema, ripple effect, dan Service Worker PWA.
- `manifest.json` — Konfigurasi Progressive Web App (PWA).
- `sw.js` — Service Worker untuk fungsionalitas caching offline (Network-First untuk HTML).
- `robots.txt` & `sitemap.xml` — Konfigurasi SEO dan pengindeksan search engine.
- `data/apps.json` — Sumber data tunggal katalog aplikasi studio.
- `src/` & `scripts/` — Template layout terpusat (`build.py`) dan skrip QA otomatis (`verify.py`).
- `.github/workflows/qa.yml` — Verifikasi otomatis link, SEO, dan kepatuhan privasi pada setiap push.

---

## 🛠️ Pembaruan & Pengujian Lokal

Untuk mengubah menu navigasi, footer, atau menambah aplikasi baru di `data/apps.json`, cukup jalankan:

```bash
python scripts/build.py
python scripts/verify.py
```

Untuk pratinjau lokal lengkap beserta Service Worker:

```bash
python -m http.server 8000
```

---

## 📬 Kontak & Dukungan

- **Email:** [rewizatech@gmail.com](mailto:rewizatech@gmail.com)
- **WhatsApp:** [+62 831-5566-2121](https://wa.me/6283155662121)
- **Website:** [https://rewizatech.github.io](https://rewizatech.github.io)

---
© 2026 Rewiza Tech. All rights reserved.
