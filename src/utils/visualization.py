"""
High-Fidelity Visualization Subsystem for Overhead Canopy Crown Inspection.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).
"""

from __future__ import annotations

from typing import List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image

from src.ml.engine import BoundingBox


def render_canopy_overlay(
    image: Union[np.ndarray, Image.Image],
    boxes: List[BoundingBox],
    draw_masks: bool = True,
    draw_labels: bool = True,
    box_color_bgr: Tuple[int, int, int] = (34, 197, 94),  # Vibrant Forest Emerald Green
    mask_alpha: float = 0.22,
) -> np.ndarray:
    """
    Renders high-definition bounding boxes, canopy crown masks, and telemetry badges
    over an aerial forest image payload.

    Args:
        image: Source image as RGB numpy array or PIL Image.
        boxes: List of validated BoundingBox instances.
        draw_masks: Whether to shade the crown interior with a semi-transparent tint.
        draw_labels: Whether to render confidence and identifier pill badges.
        box_color_bgr: Primary BGR color for bounding outlines.
        mask_alpha: Alpha blending weight for the interior canopy mask.

    Returns:
        RGB NumPy array formatted for Streamlit or disk export.
    """
    if isinstance(image, Image.Image):
        np_img = np.array(image.convert("RGB"))
    else:
        np_img = image.copy()

    # Convert RGB to BGR for OpenCV drawing
    bgr_canvas = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    overlay = bgr_canvas.copy()

    for idx, box in enumerate(boxes, start=1):
        x1, y1 = int(round(box.x1)), int(round(box.y1))
        x2, y2 = int(round(box.x2)), int(round(box.y2))

        # 1. Semi-transparent canopy crown fill
        if draw_masks and (x2 > x1) and (y2 > y1):
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            rx = max(1, (x2 - x1) // 2)
            ry = max(1, (y2 - y1) // 2)
            cv2.ellipse(
                overlay,
                (cx, cy),
                (rx, ry),
                angle=0,
                startAngle=0,
                endAngle=360,
                color=box_color_bgr,
                thickness=-1,
            )

    # Blend transparent mask
    if draw_masks and boxes:
        cv2.addWeighted(overlay, mask_alpha, bgr_canvas, 1.0 - mask_alpha, 0, bgr_canvas)

    # 2. Draw crisp bounding boxes and badges
    for idx, box in enumerate(boxes, start=1):
        x1, y1 = int(round(box.x1)), int(round(box.y1))
        x2, y2 = int(round(box.x2)), int(round(box.y2))

        # Dynamic outline thickness scaled to image dimensions
        img_h, img_w = bgr_canvas.shape[:2]
        thickness = max(2, int(round(min(img_h, img_w) / 450.0)))

        # Draw outer bounding box
        cv2.rectangle(bgr_canvas, (x1, y1), (x2, y2), box_color_bgr, thickness)

        # Draw subtle corner markers for high visual precision
        corner_len = max(6, int(round(min(x2 - x1, y2 - y1) * 0.2)))
        accent_color = (255, 255, 255)
        # Top-left corner
        cv2.line(bgr_canvas, (x1, y1), (x1 + corner_len, y1), accent_color, thickness)
        cv2.line(bgr_canvas, (x1, y1), (x1, y1 + corner_len), accent_color, thickness)
        # Bottom-right corner
        cv2.line(bgr_canvas, (x2, y2), (x2 - corner_len, y2), accent_color, thickness)
        cv2.line(bgr_canvas, (x2, y2), (x2, y2 - corner_len), accent_color, thickness)

        if draw_labels:
            label_text = f"#{idx} | {box.confidence:.0%}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = max(0.4, min(img_w, img_h) / 1200.0)
            text_thickness = max(1, int(round(font_scale * 2.0)))

            (txt_w, txt_h), baseline = cv2.getTextSize(label_text, font, font_scale, text_thickness)
            badge_y1 = max(0, y1 - txt_h - 6)
            badge_y2 = y1
            badge_x2 = min(img_w, x1 + txt_w + 8)

            # Draw badge background
            cv2.rectangle(bgr_canvas, (x1, badge_y1), (badge_x2, badge_y2), (20, 20, 20), -1)
            cv2.rectangle(bgr_canvas, (x1, badge_y1), (badge_x2, badge_y2), box_color_bgr, 1)

            # Draw text inside badge
            cv2.putText(
                bgr_canvas,
                label_text,
                (x1 + 4, badge_y2 - 3),
                font,
                font_scale,
                (255, 255, 255),
                text_thickness,
                lineType=cv2.LINE_AA,
            )

    # Convert back to RGB for Streamlit/PIL consumption
    return cv2.cvtColor(bgr_canvas, cv2.COLOR_BGR2RGB)
