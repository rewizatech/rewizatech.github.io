#!/usr/bin/env python3
"""Static site generator for Rewiza Tech (single-source templates + data/apps.json)."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render_mockup_apps(apps: list[dict]) -> str:
    blocks = []
    for app in apps:
        blocks.append(
            f'<a class="mini-app" href="{html.escape(app["url"])}">'
            f'<div class="mini-icon"><img src="{html.escape(app["icon"])}" alt="{html.escape(app["shortName"])}"></div>'
            f'<div><strong>{html.escape(app["name"])}</strong><small>{html.escape(app["tagline"])}</small></div>'
            f"</a>"
        )
    return "\n        ".join(blocks)


def render_home_apps_cards(apps: list[dict]) -> str:
    blocks = []
    for app in apps:
        link_html = ""
        if app["id"] == "kasir-laris":
            link_html = f'<p style="margin-top:16px"><a href="{html.escape(app["url"])}">Pelajari {html.escape(app["shortName"])} →</a></p>'
        play_btn = ""
        if app.get("playStoreUrl"):
            play_btn = f'<p style="margin-top:12px"><a class="button sm" href="{html.escape(app["playStoreUrl"])}" target="_blank" rel="noopener noreferrer">Google Play ↗</a></p>'
        blocks.append(
            f'<article class="card">\n'
            f'      <div class="app-symbol"><img src="{html.escape(app["icon"])}" alt="Ikon {html.escape(app["name"])}"></div>\n'
            f'      <h3>{html.escape(app["name"])}</h3>\n'
            f'      <p>{html.escape(app["homeSummary"])}</p>\n'
            f'      <span class="status">{html.escape(app["status"])}</span>\n'
            f'      {link_html}{play_btn}\n'
            f'    </article>'
        )
    return "\n    ".join(blocks)


def render_catalog_apps_cards(apps: list[dict]) -> str:
    blocks = []
    for app in apps:
        actions = []
        if not app["url"].startswith("/apps/#"):
            actions.append(
                f'<a class="button sm" href="{html.escape(app["url"])}">Detail Aplikasi &amp; Fitur →</a>'
            )
        if app.get("playStoreUrl"):
            actions.append(
                f'<a class="button whatsapp sm" href="{html.escape(app["playStoreUrl"])}" target="_blank" rel="noopener noreferrer">Download di Google Play ↗</a>'
            )
        actions.append(
            f'<a class="button secondary sm" href="{html.escape(app["privacyUrl"])}">Kebijakan Privasi</a>'
        )
        cat_slug = html.escape(app.get("categorySlug", "general"))
        cat_name = html.escape(app.get("categoryName", "Aplikasi"))
        blocks.append(
            f'<section class="card app-row-card" id="{html.escape(app["id"])}" data-category="{cat_slug}">\n'
            f'      <div class="app-symbol"><img src="{html.escape(app["icon"])}" alt="Ikon {html.escape(app["name"])}"></div>\n'
            f'      <div class="app-row-body">\n'
            f'        <div class="app-row-head">\n'
            f'          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">\n'
            f'            <h3 style="margin:0">{html.escape(app["name"])}</h3>\n'
            f'            <span class="badge" style="font-size:11px">{cat_name}</span>\n'
            f'          </div>\n'
            f'          <span class="status">{html.escape(app["status"])}</span>\n'
            f'        </div>\n'
            f'        <p class="app-row-desc">{html.escape(app["summary"])}</p>\n'
            f'        <div class="contact-row">\n'
            f'          {" ".join(actions)}\n'
            f'        </div>\n'
            f'      </div>\n'
            f'    </section>'
        )
    return "\n    ".join(blocks)


def build_breadcrumb_schema(page_url: str, page_title: str, studio_url: str) -> dict | None:
    if page_url in ("/", "/404.html"):
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": studio_url + "/"}]
    parts = [p for p in page_url.strip("/").split("/") if p]
    if not parts:
        return None

    current_path = studio_url
    for idx, part in enumerate(parts, start=2):
        current_path += "/" + part
        name = part.replace(".html", "").replace("-", " ").title()
        if part == "apps":
            name = "Katalog Aplikasi"
        elif part == "about":
            name = "Tentang Kami"
        elif part == "privacy-policy":
            name = "Pusat Legal"
        elif part == "support":
            name = "Layanan Bantuan"
        elif part == "faq":
            name = "FAQ"
        elif part == "terms":
            name = "Syarat & Ketentuan"
        elif part in ("kasir-laris", "kasir-laris.html"):
            name = "Kasir Laris POS"
        elif part == "utility.html":
            name = "Aplikasi Utilitas"

        items.append({
            "@type": "ListItem",
            "position": idx,
            "name": name,
            "item": current_path + ("/" if not current_path.endswith(".html") else ""),
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def render_json_ld(kind: str, studio: dict, apps: list[dict], page: dict) -> str:
    if kind == "organization":
        payload = [
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": studio["name"],
                "url": studio["url"] + "/",
                "logo": studio["url"] + "/assets/icons/favicon-512.png",
                "email": studio["email"],
                "description": "Studio pengembang aplikasi Android modern dengan fokus offline-first, privasi lokal, dan arsitektur Kotlin modern di Indonesia.",
                "knowsAbout": [
                    "Android Development",
                    "Kotlin",
                    "Jetpack Compose",
                    "Offline-First Architecture",
                    "Point of Sale Software",
                    "SQLite & Room Database",
                ],
                "sameAs": [
                    "https://github.com/rewizatech",
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "Customer Support",
                    "email": studio["email"],
                    "telephone": "+6283155662121",
                    "availableLanguage": ["id", "en"],
                },
            },
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": studio["name"],
                "url": studio["url"] + "/",
                "inLanguage": "id-ID",
                "description": "Situs resmi studio pengembang aplikasi Android Rewiza Tech.",
            },
        ]
        return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + "</script>"

    if kind == "kasir-laris":
        app = next((a for a in apps if a["id"] == "kasir-laris"), None)
        if app:
            payload = [
                {
                    "@context": "https://schema.org",
                    "@type": "SoftwareApplication",
                    "name": app["name"],
                    "operatingSystem": "Android",
                    "applicationCategory": "BusinessApplication",
                    "description": app["summary"],
                    "url": studio["url"] + app["url"],
                    "image": studio["url"] + app["icon"],
                    "softwareVersion": "1.0",
                    "author": {
                        "@type": "Organization",
                        "name": studio["name"],
                        "url": studio["url"] + "/",
                    },
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "IDR",
                        "availability": "https://schema.org/InStock",
                    },
                    "featureList": [
                        "Penyimpanan database SQLite lokal tanpa internet",
                        "Pencatatan transaksi kasir",
                        "Manajemen produk dan kategori",
                        "Pratinjau struk belanja transaksi",
                        "Privasi penuh tanpa pelacakan data",
                    ],
                },
                {
                    "@context": "https://schema.org",
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Beranda", "item": studio["url"] + "/"},
                        {"@type": "ListItem", "position": 2, "name": "Katalog Aplikasi", "item": studio["url"] + "/apps/"},
                        {"@type": "ListItem", "position": 3, "name": "Kasir Laris POS", "item": studio["url"] + app["url"]},
                    ],
                },
            ]
            return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + "</script>"

    if kind == "catalog":
        items = []
        for idx, app in enumerate(apps, 1):
            items.append({
                "@type": "ListItem",
                "position": idx,
                "item": {
                    "@type": "SoftwareApplication",
                    "name": app["name"],
                    "url": studio["url"] + app["url"],
                    "applicationCategory": app.get("category", "UtilitiesApplication"),
                    "operatingSystem": "Android",
                    "description": app["summary"],
                },
            })
        payload = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Katalog Aplikasi Android Rewiza Tech",
            "itemListElement": items,
        }
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Beranda", "item": studio["url"] + "/"},
                {"@type": "ListItem", "position": 2, "name": "Katalog Aplikasi", "item": studio["url"] + "/apps/"},
            ],
        }
        return '<script type="application/ld+json">' + json.dumps([payload, breadcrumb], ensure_ascii=False) + "</script>"

    # Default fallback for pages with kind "none"
    bc = build_breadcrumb_schema(page.get("url", "/"), page.get("title", ""), studio["url"])
    if bc:
        return '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + "</script>"
    return ""


def build() -> None:
    data = json.loads((ROOT / "data" / "apps.json").read_text(encoding="utf-8"))
    studio = data["studio"]
    apps = data["apps"]
    layout = (ROOT / "src" / "layout.html").read_text(encoding="utf-8")
    pages = json.loads((ROOT / "src" / "pages.json").read_text(encoding="utf-8"))

    mockup_html = render_mockup_apps(apps)
    home_cards_html = render_home_apps_cards(apps)
    catalog_cards_html = render_catalog_apps_cards(apps)

    sitemap_entries = []
    for page in pages:
        content = (ROOT / page["contentFile"]).read_text(encoding="utf-8")
        content = content.replace("{{MOCKUP_APPS}}", mockup_html)
        content = content.replace("{{HOME_APPS_CARDS}}", home_cards_html)
        content = content.replace("{{CATALOG_APPS_CARDS}}", catalog_cards_html)

        canonical_url = studio["url"].rstrip("/") + page["url"]
        nav = page.get("nav", "none")

        rendered = layout
        rendered = rendered.replace("{{title}}", html.escape(page["title"]))
        rendered = rendered.replace("{{description}}", html.escape(page["description"]))
        rendered = rendered.replace("{{keywords}}", html.escape(page.get("keywords", "")))
        rendered = rendered.replace("{{canonical_url}}", html.escape(canonical_url))
        rendered = rendered.replace("{{og_image}}", html.escape(page["ogImage"]))
        rendered = rendered.replace("{{twitter_card}}", html.escape(page["twitterCard"]))
        rendered = rendered.replace("{{json_ld}}", render_json_ld(page.get("jsonLd", "none"), studio, apps, page))
        for key in ("home", "apps", "about", "legal", "support"):
            attr = ' aria-current="page"' if nav == key else ""
            rendered = rendered.replace(f"{{{{nav_{key}}}}}", attr)
        rendered = rendered.replace("{{content}}", content.strip())

        out_path = ROOT / page["output"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8", newline="\n")

        if page.get("inSitemap"):
            sitemap_entries.append({
                "loc": canonical_url,
                "lastmod": "2026-11-12",
                "changefreq": page.get("changefreq", "monthly"),
                "priority": page.get("priority", "0.5")
            })

    sitemap_blocks = []
    for e in sitemap_entries:
        sitemap_blocks.append(
            f"  <url>\n"
            f"    <loc>{html.escape(e['loc'])}</loc>\n"
            f"    <lastmod>{e['lastmod']}</lastmod>\n"
            f"    <changefreq>{e['changefreq']}</changefreq>\n"
            f"    <priority>{e['priority']}</priority>\n"
            f"  </url>"
        )

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *sitemap_blocks,
        "</urlset>",
        "",
    ]
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap_lines), encoding="utf-8", newline="\n")
    print(f"Built {len(pages)} HTML pages and updated sitemap.xml ({len(sitemap_entries)} URLs).")


if __name__ == "__main__":
    build()

