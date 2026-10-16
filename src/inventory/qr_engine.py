"""
QR Code Technology Subsystem for Physical Tree Tagging and Mobile In-Field Scanning.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).
"""

from __future__ import annotations

import base64
import io
import logging
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H

logger = logging.getLogger("ciet.inventory.qr_engine")


def generate_tree_qr_code(
    tree_id: str,
    base_url: str = "http://localhost:8000",
    box_size: int = 10,
    border: int = 2,
) -> Tuple[bytes, str]:
    """
    Generates a high-density, scannable QR code for an individual tree digital passport.

    Args:
        tree_id: Unique tree identifier (e.g., CIET-TREE-001).
        base_url: Domain base URL serving the digital passport.
        box_size: Pixel size of each QR module square.
        border: Quiet zone border module thickness.

    Returns:
        Tuple of (png_bytes, base64_encoded_png_string).
    """
    target_url = f"{base_url.rstrip('/')}/tree/{tree_id}"

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#064e3b", back_color="#ffffff")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    png_bytes = buffer.getvalue()
    b64_str = base64.b64encode(png_bytes).decode("utf-8")

    return png_bytes, b64_str


def decode_qr_image(image_bytes: bytes) -> Optional[str]:
    """
    Decodes a QR code from an uploaded image payload or camera frame using OpenCV.

    Args:
        image_bytes: Raw binary image payload.

    Returns:
        Decoded string content (e.g. tree passport URL or ID), or None if not detected.
    """
    try:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            return None

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            return str(data)

        # Multi-scale pre-processing fallback if initial attempt didn't lock
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        data_gray, _, _ = detector.detectAndDecode(blurred)
        if data_gray:
            return str(data_gray)

        return None
    except Exception as exc:
        logger.warning("QR decoding error: %s", exc)
        return None


def generate_printable_tree_tag(
    tree_id: str,
    common_name: str,
    scientific_name: str,
    location_str: str,
    carbon_kg: float,
    base_url: str = "http://localhost:8000",
) -> bytes:
    """
    Renders an all-weather printable field tag badge for physical tree bark attachment.
    Combines CIET institutional branding, digital QR code, GPS coordinates, and carbon metrics.

    Returns:
        PNG binary bytes of the physical field badge.
    """
    tag_width = 800
    tag_height = 420
    tag_img = Image.new("RGB", (tag_width, tag_height), color="#ffffff")
    draw = ImageDraw.Draw(tag_img)

    # 1. Header Banner
    draw.rectangle([(0, 0), (tag_width, 80)], fill="#064e3b")
    draw.text((25, 18), "CIET COIMBATORE — TREE CONSERVATION TAG", fill="#f0fdf4")
    draw.text((25, 48), "Autonomous Digital Forest Stocking & Carbon Inventory", fill="#a7f3d0")

    # 2. Border
    draw.rectangle([(0, 0), (tag_width - 1, tag_height - 1)], outline="#064e3b", width=3)

    # 3. Generate QR Code
    png_bytes, _ = generate_tree_qr_code(tree_id, base_url=base_url, box_size=6, border=1)
    qr_pil = Image.open(io.BytesIO(png_bytes)).resize((260, 260))
    tag_img.paste(qr_pil, (25, 110))

    # 4. Dendrological Details Text
    x_offset = 310
    draw.text((x_offset, 110), f"TREE ID: {tree_id}", fill="#0f172a")
    draw.text((x_offset, 145), f"Common Name: {common_name}", fill="#1e293b")
    draw.text((x_offset, 175), f"Botanical: {scientific_name}", fill="#047857")
    draw.text((x_offset, 210), f"GPS Coordinates: {location_str}", fill="#475569")
    draw.text((x_offset, 245), f"Lifetime CO2 Sequestered: {carbon_kg:,.1f} kg", fill="#059669")
    draw.text((x_offset, 280), "Scan QR tag via smartphone to access live passport.", fill="#64748b")

    # 5. Footer
    draw.rectangle([(0, tag_height - 35), (tag_width, tag_height)], fill="#f1f5f9")
    draw.text((25, tag_height - 25), "Coimbatore Institute of Engineering and Technology | Narasipuram, Coimbatore", fill="#64748b")

    buf = io.BytesIO()
    tag_img.save(buf, format="PNG")
    return buf.getvalue()
