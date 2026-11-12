#!/usr/bin/env python3
"""Automated static QA verifier for Rewiza Tech website."""

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {"antigravity", "github-pages-root", "source-reference", "website-project-source", "src", "scripts", ".git", ".github"}


def resolve_local_target(source_file: Path, raw_url: str) -> Path | None:
    if raw_url.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
        return None
    clean = raw_url.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None
    if clean.startswith("/"):
        candidate = ROOT / clean.lstrip("/")
    else:
        candidate = source_file.parent / clean
    if candidate.is_dir():
        return candidate / "index.html"
    return candidate


def collect_html_files() -> list[Path]:
    files = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in EXCLUDE_DIRS:
            continue
        files.append(p)
    return sorted(files)


def main() -> int:
    errors: list[str] = []

    # 1. Validate JSON files
    for jf in ("manifest.json", "data/apps.json", "src/pages.json"):
        try:
            json.loads((ROOT / jf).read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid JSON in {jf}: {exc}")

    # 2. Validate sitemap.xml
    sitemap_urls: list[str] = []
    try:
        tree = ET.parse(ROOT / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in tree.findall(".//sm:loc", ns):
            url = (loc.text or "").strip()
            sitemap_urls.append(url)
            rel_path = url.replace("https://rewizatech.github.io", "", 1) or "/"
            target = resolve_local_target(ROOT / "index.html", rel_path)
            if not target or not target.exists():
                errors.append(f"Sitemap URL missing on disk: {url}")
    except Exception as exc:
        errors.append(f"Invalid sitemap.xml: {exc}")

    # 3. Validate all HTML files, links, SEO, and encoding
    html_files = collect_html_files()
    linked_paths: set[str] = set()
    attr_re = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')

    for hf in html_files:
        rel = "/" + hf.relative_to(ROOT).as_posix()
        text = hf.read_text(encoding="utf-8")

        for bad in ("â€”", "â†’", "â†—", "â—", "ðŸ", "Â©"):
            if bad in text:
                errors.append(f"Mojibake sequence '{bad}' found in {rel}")

        for match in attr_re.finditer(text):
            val = match.group(1)
            target = resolve_local_target(hf, val)
            if target is not None:
                if not target.exists():
                    errors.append(f"Broken link in {rel}: {val} -> {target}")
                else:
                    norm = "/" + target.relative_to(ROOT).as_posix()
                    if norm.endswith("/index.html"):
                        norm = norm[: -len("index.html")]
                    elif norm == "/index.html":
                        norm = "/"
                    linked_paths.add(norm)

        if not rel.startswith("/privacy/"):
            if not re.search(r"<title>.+</title>", text):
                errors.append(f"Missing <title> in {rel}")
            if 'name="description"' not in text:
                errors.append(f"Missing meta description in {rel}")
            if 'name="keywords"' not in text:
                errors.append(f"Missing meta keywords in {rel}")
            if 'property="og:site_name"' not in text:
                errors.append(f"Missing og:site_name in {rel}")
            if 'assets/icons/favicon.svg' not in text:
                errors.append(f"Missing SVG favicon link in {rel}")
            if 'rel="canonical"' not in text:
                errors.append(f"Missing canonical link in {rel}")
            if "localStorage.getItem('rwz-theme')" not in text:
                errors.append(f"Missing anti-FOUT head script in {rel}")
            if "data-back-to-top" not in text:
                errors.append(f"Missing back-to-top button in {rel}")
            h1_count = len(re.findall(r"<h1\b", text))
            if h1_count != 1:
                errors.append(f"Expected exactly 1 <h1> in {rel}, found {h1_count}")

    # 4. Check orphan pages from sitemap
    for url in sitemap_urls:
        rel_path = url.replace("https://rewizatech.github.io", "", 1) or "/"
        if rel_path != "/" and rel_path not in linked_paths:
            errors.append(f"Orphan page in sitemap (no internal links point to it): {rel_path}")

    # 5. Check sw.js CORE files exist
    for sw_rel in ("sw.js", "js/sw.js"):
        sw_text = (ROOT / sw_rel).read_text(encoding="utf-8")
        core_match = re.search(r"const\s+CORE\s*=\s*\[(.*?)\];", sw_text, re.S)
        if not core_match:
            errors.append(f"Could not parse CORE array in {sw_rel}")
        else:
            for item in re.findall(r"['\"]([^'\"]+)['\"]", core_match.group(1)):
                target = resolve_local_target(ROOT / "index.html", item)
                if not target or not target.exists():
                    errors.append(f"Missing CORE cache asset in {sw_rel}: {item}")

    # 6. Check Google Play compliance on kasir-laris privacy policy
    pp_kasir = (ROOT / "privacy-policy" / "kasir-laris.html").read_text(encoding="utf-8")
    if "Belum merupakan kebijakan final" in pp_kasir:
        errors.append("Draft notice still present in privacy-policy/kasir-laris.html")
    if "BLUETOOTH_CONNECT" in pp_kasir:
        errors.append("Unverified BLUETOOTH_CONNECT claim in privacy-policy/kasir-laris.html")
    if "Penghapusan Data" not in pp_kasir:
        errors.append("Missing Data Deletion section in privacy-policy/kasir-laris.html")

    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print(f" - {e}")
        return 1

    print(
        f"VERIFICATION PASSED: {len(html_files)} HTML pages, "
        f"{len(sitemap_urls)} sitemap URLs, 0 broken links, 0 orphan pages."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

