#!/usr/bin/env python3
"""Generate high-contrast, beautiful favicons, apple touch icons, ICO, and Open Graph card."""

import base64
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent

def create_squircle_icon(size: int = 512, mark_ratio: float = 0.62) -> Image.Image:
    # 1. Load clean mark
    mark_path = ROOT / "assets" / "brand" / "mark-clean-transparent.png"
    mark = Image.open(mark_path)
    w_orig, h_orig = mark.size

    # 2. Gradient canvas (top-left #00E5FF to bottom-right #0072F5)
    grad = Image.new("RGBA", (size, size))
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2.0 * size)
            r = int(0 * (1 - t) + 0 * t)
            g = int(229 * (1 - t) + 114 * t)
            b = int(255 * (1 - t) + 245 * t)
            grad.putpixel((x, y), (r, g, b, 255))

    # 3. Squircle mask (radius ~22%)
    radius = int(size * 0.22)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=255)

    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base.paste(grad, (0, 0), mask)

    # 4. Scale mark
    target_h = int(size * mark_ratio)
    target_w = int(w_orig * (target_h / h_orig))
    scaled_mark = mark.resize((target_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a_ch = scaled_mark.split()

    # 5. Pure white mark
    white_img = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 255))
    white_mark = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    white_mark.paste(white_img, (0, 0), a_ch)

    # 6. Soft drop shadow
    shadow_blur = max(2, int(size * 0.015))
    shadow_mask = a_ch.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    shadow = Image.new("RGBA", (target_w, target_h), (0, 45, 110, 110))

    pos_x = (size - target_w) // 2
    pos_y = (size - target_h) // 2
    offset_y = max(1, int(size * 0.012))

    base.paste(shadow, (pos_x, pos_y + offset_y), shadow_mask)
    base.paste(white_mark, (pos_x, pos_y), a_ch)

    return base


def generate_favicons() -> None:
    icons_dir = ROOT / "assets" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)

    master = create_squircle_icon(512, mark_ratio=0.64)
    master.save(icons_dir / "favicon-512.png")
    master.save(icons_dir / "icon-512.png")

    # Generate various sizes
    pwa_192 = master.resize((192, 192), Image.Resampling.LANCZOS)
    pwa_192.save(icons_dir / "icon-192.png")

    apple_180 = master.resize((180, 180), Image.Resampling.LANCZOS)
    apple_180.save(icons_dir / "apple-touch-icon.png")

    ico_48 = master.resize((48, 48), Image.Resampling.LANCZOS)
    ico_48.save(icons_dir / "favicon-48x48.png")

    ico_32 = master.resize((32, 32), Image.Resampling.LANCZOS)
    ico_32.save(icons_dir / "favicon-32x32.png")
    ico_32.save(icons_dir / "favicon.png")

    ico_16 = master.resize((16, 16), Image.Resampling.LANCZOS)
    ico_16.save(icons_dir / "favicon-16x16.png")

    # Multi-resolution favicon.ico at root
    master.save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    # Generate vector-compatible SVG favicon
    buf = io.BytesIO()
    master.save(buf, format="PNG")
    b64_png = base64.b64encode(buf.getvalue()).decode("ascii")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="rwzGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="100%" stop-color="#0072F5"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="url(#rwzGrad)"/>
  <image href="data:image/png;base64,{b64_png}" x="0" y="0" width="512" height="512"/>
</svg>
'''
    (icons_dir / "favicon.svg").write_text(svg_content, encoding="utf-8")
    print("Favicons (ICO, SVG, PNG 16/32/48/180/192/512) generated successfully.")


def generate_og_image() -> None:
    width, height = 1200, 630
    og = Image.new("RGBA", (width, height), (6, 18, 38, 255))
    draw = ImageDraw.Draw(og)

    # Ambient gradient glow
    for r in range(350, 0, -5):
        alpha = int(45 * (1 - r / 350))
        draw.ellipse(
            [(160 - r, 315 - r), (160 + r, 315 + r)],
            fill=(0, 229, 255, alpha),
        )
    for r in range(450, 0, -8):
        alpha = int(35 * (1 - r / 450))
        draw.ellipse(
            [(950 - r, 200 - r), (950 + r, 200 + r)],
            fill=(0, 114, 245, alpha),
        )

    # Draw border card frame
    draw.rounded_rectangle([(30, 30), (width - 30, height - 30)], radius=32, outline=(30, 60, 105, 200), width=2)

    # Paste squircle icon
    icon = create_squircle_icon(190, mark_ratio=0.64)
    og.paste(icon, (80, 220), icon)

    # Text rendering (try system Arial/Segoe UI, fallback to default)
    def get_font(size: int, bold: bool = False):
        font_candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        ]
        for candidate in font_candidates:
            if Path(candidate).exists():
                try:
                    return ImageFont.truetype(candidate, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    font_brand = get_font(52, bold=True)
    font_badge = get_font(18, bold=True)
    font_title = get_font(34, bold=True)
    font_desc = get_font(22, bold=False)
    font_footer = get_font(18, bold=False)

    text_x = 310

    # Pill badge above title
    badge_text = "OFFICIAL ANDROID APPS DEVELOPER STUDIO"
    draw.rounded_rectangle([(text_x, 150), (text_x + 470, 184)], radius=17, fill=(0, 114, 245, 45), outline=(0, 229, 255, 120), width=1)
    draw.text((text_x + 18, 157), badge_text, fill=(0, 229, 255, 255), font=font_badge)

    # Brand Title
    draw.text((text_x, 200), "Rewiza Tech", fill=(255, 255, 255, 255), font=font_brand)

    # Subtitle / Tagline
    draw.text((text_x, 275), "Solusi Bisnis & Aplikasi Android Offline-First", fill=(240, 246, 255, 255), font=font_title)

    # Description
    desc_line1 = "Pengembang aplikasi kasir toko Kasir Laris POS dan utilitas produktivitas"
    desc_line2 = "dengan fokus pada privasi data lokal, kecepatan, dan tanpa biaya bulanan."
    draw.text((text_x, 335), desc_line1, fill=(160, 185, 220, 255), font=font_desc)
    draw.text((text_x, 370), desc_line2, fill=(160, 185, 220, 255), font=font_desc)

    # App Pill Badges
    pills = ["✓ Kasir Laris POS", "✓ Smart Compress", "✓ 100% Offline-First", "✓ Bebas Langganan"]
    pill_x = text_x
    for p in pills:
        pill_w = len(p) * 11 + 24
        draw.rounded_rectangle([(pill_x, 430), (pill_x + pill_w, 466)], radius=18, fill=(16, 38, 74, 255), outline=(40, 85, 150, 255), width=1)
        draw.text((pill_x + 12, 438), p, fill=(210, 230, 255, 255), font=font_badge)
        pill_x += pill_w + 12

    # Footer domain
    draw.text((text_x, 520), "🌐 https://rewizatech.github.io  •  Google Play Developer", fill=(120, 150, 195, 255), font=font_footer)

    brand_dir = ROOT / "assets" / "brand"
    brand_dir.mkdir(parents=True, exist_ok=True)
    og.save(brand_dir / "og-image.png")
    print("Open Graph image (assets/brand/og-image.png, 1200x630) generated successfully.")


if __name__ == "__main__":
    generate_favicons()
    generate_og_image()
