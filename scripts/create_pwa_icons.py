"""
Generate high-fidelity PWA App Icons for CIET Forestry & Tree Stocking Platform.
Produces 192x192, 512x512, and maskable PNG app icons.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

STATIC_ICONS_DIR = Path(__file__).resolve().parent.parent / "static" / "icons"
STATIC_ICONS_DIR.mkdir(parents=True, exist_ok=True)


def draw_ciet_icon(size: int, output_path: Path) -> None:
    # 1. Create Canvas
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2. Draw Rounded Dark Emerald Shield / Background
    padding = int(size * 0.05)
    corner_radius = int(size * 0.22)
    bg_box = [padding, padding, size - padding, size - padding]
    
    # Gradient or solid deep forest emerald
    draw.rounded_rectangle(bg_box, radius=corner_radius, fill=(6, 78, 59, 255), outline=(16, 185, 129, 255), width=int(size * 0.025))

    # Inner subtle glow ring
    inner_padding = int(size * 0.1)
    inner_box = [inner_padding, inner_padding, size - inner_padding, size - inner_padding]
    draw.rounded_rectangle(inner_box, radius=int(corner_radius * 0.7), outline=(52, 211, 153, 90), width=int(size * 0.015))

    center_x = size // 2
    center_y = int(size * 0.48)

    # 3. Draw Stylized Sacred Forest Canopy Tree
    # Trunk
    trunk_width = int(size * 0.08)
    trunk_height = int(size * 0.24)
    trunk_box = [
        center_x - trunk_width // 2,
        center_y + int(size * 0.08),
        center_x + trunk_width // 2,
        center_y + int(size * 0.08) + trunk_height
    ]
    draw.rounded_rectangle(trunk_box, radius=int(trunk_width * 0.3), fill=(180, 83, 9, 255))

    # Layered Tree Foliage Triangles / Crowns
    # Tier 3 (Bottom crown)
    tier3 = [
        (center_x, center_y - int(size * 0.02)),
        (center_x - int(size * 0.28), center_y + int(size * 0.14)),
        (center_x + int(size * 0.28), center_y + int(size * 0.14))
    ]
    draw.polygon(tier3, fill=(16, 185, 129, 255))

    # Tier 2 (Middle crown)
    tier2 = [
        (center_x, center_y - int(size * 0.14)),
        (center_x - int(size * 0.22), center_y + int(size * 0.03)),
        (center_x + int(size * 0.22), center_y + int(size * 0.03))
    ]
    draw.polygon(tier2, fill=(52, 211, 153, 255))

    # Tier 1 (Top crown)
    tier1 = [
        (center_x, center_y - int(size * 0.26)),
        (center_x - int(size * 0.16), center_y - int(size * 0.08)),
        (center_x + int(size * 0.16), center_y - int(size * 0.08))
    ]
    draw.polygon(tier1, fill=(110, 231, 183, 255))

    # 4. QR Code Symbol Accent in bottom right of tree
    qr_size = int(size * 0.14)
    qr_x = center_x + int(size * 0.15)
    qr_y = center_y + int(size * 0.12)
    draw.rounded_rectangle([qr_x, qr_y, qr_x + qr_size, qr_y + qr_size], radius=int(qr_size * 0.2), fill=(255, 255, 255, 240), outline=(6, 78, 59, 255), width=2)
    # Inner QR dot pattern
    dot_margin = int(qr_size * 0.22)
    draw.rectangle([qr_x + dot_margin, qr_y + dot_margin, qr_x + qr_size - dot_margin, qr_y + qr_size - dot_margin], fill=(6, 78, 59, 255))

    # 5. Label Banner "CIET" at bottom
    banner_y = int(size * 0.82)
    # Approximate text rendering using rectangles if font not found, or default
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.11))
        draw.text((center_x, banner_y), "CIET", fill=(255, 255, 255, 255), anchor="mm", font=font)
    except Exception:
        # Fallback text
        draw.text((center_x - int(size * 0.14), banner_y - int(size * 0.06)), "CIET", fill=(255, 255, 255, 255))

    img.save(output_path, "PNG")
    print(f"Generated {output_path} ({size}x{size})")


if __name__ == "__main__":
    draw_ciet_icon(192, STATIC_ICONS_DIR / "icon-192.png")
    draw_ciet_icon(512, STATIC_ICONS_DIR / "icon-512.png")
    draw_ciet_icon(512, STATIC_ICONS_DIR / "icon-maskable.png")
    print("All PWA icons generated successfully.")
