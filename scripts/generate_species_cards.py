"""
Generate rich, high-resolution botanical species visual cards for all 16 CIET trees.
Each card features custom botanical color grading, species canopy silhouette, Tamil typography,
and conservation badge.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SPECIES_DIR = Path(__file__).resolve().parent.parent / "static" / "species"
SPECIES_DIR.mkdir(parents=True, exist_ok=True)

SPECIES_METADATA = [
    {
        "id": "CIET-TREE-001",
        "name": "Neem (Margosa)",
        "tamil": "வேப்பமரம்",
        "sci": "Azadirachta indica",
        "family": "Meliaceae",
        "accent": (16, 185, 129),
        "bg": (6, 78, 59),
        "canopy_shape": "oval",
        "tag": "Medicinal • Air Purifier"
    },
    {
        "id": "CIET-TREE-002",
        "name": "Heritage Banyan Tree",
        "tamil": "ஆலமரம் (75 Yrs)",
        "sci": "Ficus benghalensis",
        "family": "Moraceae",
        "accent": (52, 211, 153),
        "bg": (2, 44, 34),
        "canopy_shape": "massive_spreading",
        "tag": "Keystone Species • 380m²"
    },
    {
        "id": "CIET-TREE-003",
        "name": "Sacred Fig (Peepal)",
        "tamil": "அரசமரம்",
        "sci": "Ficus religiosa",
        "family": "Moraceae",
        "accent": (110, 231, 183),
        "bg": (6, 78, 59),
        "canopy_shape": "heart_canopy",
        "tag": "Sacred Grove • High Oxygen"
    },
    {
        "id": "CIET-TREE-004",
        "name": "Indian Rosewood",
        "tamil": "ஈட்டிமரம்",
        "sci": "Dalbergia latifolia",
        "family": "Fabaceae",
        "accent": (245, 158, 11),
        "bg": (69, 26, 3),
        "canopy_shape": "tall_timber",
        "tag": "IUCN Vulnerable • Timber"
    },
    {
        "id": "CIET-TREE-005",
        "name": "Red Sandalwood",
        "tamil": "செஞ்சந்தனம்",
        "sci": "Pterocarpus santalinus",
        "family": "Fabaceae",
        "accent": (239, 68, 68),
        "bg": (69, 10, 10),
        "canopy_shape": "dense_round",
        "tag": "IUCN Endangered • Rare"
    },
    {
        "id": "CIET-TREE-006",
        "name": "Teak Tree",
        "tamil": "தேக்குமரம்",
        "sci": "Tectona grandis",
        "family": "Lamiaceae",
        "accent": (217, 119, 6),
        "bg": (41, 37, 36),
        "canopy_shape": "tall_timber",
        "tag": "High Biomass • 24.1m"
    },
    {
        "id": "CIET-TREE-007",
        "name": "Jamun (Black Plum)",
        "tamil": "நாவல் மரம்",
        "sci": "Syzygium cumini",
        "family": "Myrtaceae",
        "accent": (147, 51, 234),
        "bg": (59, 7, 100),
        "canopy_shape": "oval",
        "tag": "Riparian Buffer • Fruit"
    },
    {
        "id": "CIET-TREE-008",
        "name": "Arjun Tree",
        "tamil": "மருதமரம்",
        "sci": "Terminalia arjuna",
        "family": "Combretaceae",
        "accent": (6, 182, 212),
        "bg": (8, 51, 68),
        "canopy_shape": "buttressed",
        "tag": "Riparian Guard • Ayurvedic"
    },
    {
        "id": "CIET-TREE-009",
        "name": "Pongamia (Indian Beech)",
        "tamil": "புங்கமரம்",
        "sci": "Pongamia pinnata",
        "family": "Fabaceae",
        "accent": (16, 185, 129),
        "bg": (6, 78, 59),
        "canopy_shape": "dense_round",
        "tag": "Biofuel • Nitrogen Fixer"
    },
    {
        "id": "CIET-TREE-010",
        "name": "Mahua Tree",
        "tamil": "இலுப்பை மரம்",
        "sci": "Madhuca longifolia",
        "family": "Sapotaceae",
        "accent": (245, 158, 11),
        "bg": (67, 56, 202),
        "canopy_shape": "spreading",
        "tag": "Near Threatened • Nectar"
    },
    {
        "id": "CIET-TREE-011",
        "name": "Tamarind Tree",
        "tamil": "புளியமரம்",
        "sci": "Tamarindus indica",
        "family": "Fabaceae",
        "accent": (234, 88, 12),
        "bg": (67, 20, 7),
        "canopy_shape": "umbrella",
        "tag": "Culinary Heritage • 45 Yrs"
    },
    {
        "id": "CIET-TREE-012",
        "name": "Rain Tree (Thoongu Moonji)",
        "tamil": "தூங்குமூஞ்சி மரம்",
        "sci": "Samanea saman",
        "family": "Fabaceae",
        "accent": (16, 185, 129),
        "bg": (2, 44, 34),
        "canopy_shape": "parasol",
        "tag": "Thermal Shield • 290m²"
    },
    {
        "id": "CIET-TREE-013",
        "name": "Indian Gooseberry (Amla)",
        "tamil": "நெல்லி மரம்",
        "sci": "Phyllanthus emblica",
        "family": "Phyllanthaceae",
        "accent": (132, 204, 22),
        "bg": (26, 46, 5),
        "canopy_shape": "feathery",
        "tag": "Ayurvedic • Vitamin C"
    },
    {
        "id": "CIET-TREE-014",
        "name": "Gulmohar (Royal Poinciana)",
        "tamil": "செம்மயிர்க்கொன்றை",
        "sci": "Delonix regia",
        "family": "Fabaceae",
        "accent": (239, 68, 68),
        "bg": (69, 10, 10),
        "canopy_shape": "parasol",
        "tag": "Scarlet Blooms • Avenue"
    },
    {
        "id": "CIET-TREE-015",
        "name": "Cannonball (Nagalingam)",
        "tamil": "நாகலிங்க மரம்",
        "sci": "Couroupita guianensis",
        "family": "Lecythidaceae",
        "accent": (234, 179, 8),
        "bg": (66, 32, 6),
        "canopy_shape": "cauliflorous",
        "tag": "Sacred Blooms • Fragrant"
    },
    {
        "id": "CIET-TREE-016",
        "name": "Indian Sandalwood",
        "tamil": "சந்தனமரம்",
        "sci": "Santalum album",
        "family": "Santalaceae",
        "accent": (245, 158, 11),
        "bg": (41, 37, 36),
        "canopy_shape": "dense_round",
        "tag": "IUCN Vulnerable • Santalol"
    },
]


def render_card(spec: dict) -> None:
    width, height = 640, 420
    img = Image.new("RGBA", (width, height), (*spec["bg"], 255))
    draw = ImageDraw.Draw(img)

    # 1. Subtle Radial / Gradient Glow overlay
    accent = spec["accent"]
    for r in range(width // 2, 0, -10):
        alpha = int(35 * (1 - r / (width // 2)))
        draw.ellipse([width - r, -r, width + r, r], outline=(*accent, alpha), width=8)

    # 2. Outer Border & Inner HUD Grid Lines
    draw.rectangle([12, 12, width - 12, height - 12], outline=(*accent, 90), width=2)
    # Technical Corner Brackets
    corner_len = 24
    draw.line([(12, 12 + corner_len), (12, 12), (12 + corner_len, 12)], fill=(*accent, 255), width=3)
    draw.line([(width - 12 - corner_len, 12), (width - 12, 12), (width - 12, 12 + corner_len)], fill=(*accent, 255), width=3)
    draw.line([(12, height - 12 - corner_len), (12, height - 12), (12 + corner_len, height - 12)], fill=(*accent, 255), width=3)
    draw.line([(width - 12 - corner_len, height - 12), (width - 12, height - 12), (width - 12 - corner_len, height - 12)], fill=(*accent, 255), width=3)

    # 3. Botanical Tree Canopy Silhouette
    center_x = int(width * 0.72)
    center_y = int(height * 0.52)

    # Trunk
    draw.rounded_rectangle([center_x - 12, center_y + 20, center_x + 12, center_y + 110], radius=4, fill=(120, 53, 15, 255))
    # Canopy Circles/Ellipses with layered opacity
    draw.ellipse([center_x - 100, center_y - 90, center_x + 100, center_y + 40], fill=(*accent, 70))
    draw.ellipse([center_x - 85, center_y - 80, center_x + 85, center_y + 30], fill=(*accent, 120))
    draw.ellipse([center_x - 70, center_y - 70, center_x + 70, center_y + 20], fill=(*accent, 190))

    # Leaf/Floral Accent Star on Canopy
    draw.ellipse([center_x - 16, center_y - 30, center_x + 16, center_y + 2], fill=(255, 255, 255, 230))

    # 4. Typography & Information Left Column
    try:
        font_large = ImageFont.truetype("arial.ttf", 26)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_mono = ImageFont.truetype("consola.ttf", 13)
    except Exception:
        font_large = font_medium = font_small = font_mono = ImageFont.load_default()

    # Specimen ID Pill
    draw.rounded_rectangle([32, 32, 180, 60], radius=6, fill=(*accent, 40), outline=(*accent, 160), width=1)
    draw.text((44, 38), spec["id"], fill=(255, 255, 255, 255), font=font_mono)

    # Institutional Header
    draw.text((32, 78), "CIET BOTANICAL HERBARIUM", fill=(*accent, 220), font=font_small)

    # Common Name
    draw.text((32, 102), spec["name"], fill=(255, 255, 255, 255), font=font_large)

    # Tamil Name & Scientific Name
    draw.text((32, 142), f"{spec['tamil']}  |  {spec['sci']}", fill=(203, 213, 225, 255), font=font_medium)

    # Family
    draw.text((32, 172), f"Family: {spec['family']}", fill=(148, 163, 184, 255), font=font_small)

    # Characteristic Tag Pill
    draw.rounded_rectangle([32, 210, 310, 242], radius=8, fill=(0, 0, 0, 140), outline=(*accent, 140), width=1)
    draw.text((44, 218), f"🌿 {spec['tag']}", fill=(*accent, 255), font=font_small)

    # Western Ghats Micro-Telemetry
    draw.line([(32, 268), (320, 268)], fill=(255, 255, 255, 40), width=1)
    draw.text((32, 282), "GEOLOCATION ANCHOR: CIET COIMBATORE", fill=(100, 116, 139, 255), font=font_small)
    draw.text((32, 302), "GPS: 10.999° N, 76.904° E | WGS84", fill=(148, 163, 184, 255), font=font_mono)
    draw.text((32, 324), "PAN-TROPICAL ALLOMETRIC SEQUESTRATION", fill=(100, 116, 139, 255), font=font_small)
    draw.text((32, 344), "STATUS: DIGITAL PASSPORT VERIFIED", fill=(16, 185, 129, 255), font=font_mono)

    output_path = SPECIES_DIR / f"{spec['id']}.png"
    img.save(output_path, "PNG")


if __name__ == "__main__":
    for s in SPECIES_METADATA:
        render_card(s)
    print(f"Rendered {len(SPECIES_METADATA)} botanical visual cards in static/species/.")
