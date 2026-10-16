"""
Synthetic Aerial Forest Imagery Generator.
Produces realistic multi-spectral overhead canopy payloads for testing and offline CIET demos.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


def generate_aerial_forest_sample(
    width: int = 1024,
    height: int = 1024,
    num_trees: int = 35,
    seed: int = 42,
) -> np.ndarray:
    """
    Generates a realistic overhead drone/aerial RGB canopy image with varying crown sizes,
    dense cluster overlaps, forest floor textures, and shadowing.

    Args:
        width: Output image width.
        height: Output image height.
        num_trees: Number of tree crowns to synthesize.
        seed: Random seed for deterministic generation.

    Returns:
        RGB NumPy array representing high-resolution aerial forest terrain.
    """
    rng = np.random.RandomState(seed)

    # 1. Base forest floor (earthy brownish-green terrain with natural Perlin-like noise)
    base_terrain = np.zeros((height, width, 3), dtype=np.uint8)
    base_terrain[:, :, 0] = rng.randint(45, 65, size=(height, width), dtype=np.uint8)   # Red (earthy)
    base_terrain[:, :, 1] = rng.randint(70, 95, size=(height, width), dtype=np.uint8)   # Green (undergrowth)
    base_terrain[:, :, 2] = rng.randint(30, 45, size=(height, width), dtype=np.uint8)   # Blue

    # Apply soft blur for smooth terrain variation
    base_terrain = cv2.GaussianBlur(base_terrain, (21, 21), 0)

    # 2. Add ground texture variation (patches of brushwood and shadows)
    for _ in range(8):
        px = rng.randint(0, width)
        py = rng.randint(0, height)
        radius = rng.randint(60, 200)
        color = (
            int(rng.randint(35, 55)),
            int(rng.randint(60, 85)),
            int(rng.randint(25, 40)),
        )
        cv2.circle(base_terrain, (px, py), radius, color, -1)

    canvas = cv2.GaussianBlur(base_terrain, (35, 35), 0)

    # 3. Synthesize individual overhead tree crowns with realistic canopy foliage texture
    # Create cluster centers to mimic natural forest clump distributions
    num_clusters = 5
    cluster_centers = [
        (rng.randint(150, width - 150), rng.randint(150, height - 150))
        for _ in range(num_clusters)
    ]

    for i in range(num_trees):
        # Choose a cluster center or random position
        if rng.rand() < 0.75:
            c_center = cluster_centers[rng.randint(0, num_clusters)]
            tx = int(np.clip(c_center[0] + rng.normal(0, 110), 60, width - 60))
            ty = int(np.clip(c_center[1] + rng.normal(0, 110), 60, height - 60))
        else:
            tx = rng.randint(80, width - 80)
            ty = rng.randint(80, height - 80)

        crown_radius_x = rng.randint(25, 65)
        crown_radius_y = int(crown_radius_x * rng.uniform(0.85, 1.15))
        angle = rng.randint(0, 180)

        # Draw soft canopy shadow on terrain
        shadow_offset_x = 12
        shadow_offset_y = 16
        shadow_color = (
            int(canvas[ty, tx, 0] * 0.45),
            int(canvas[ty, tx, 1] * 0.45),
            int(canvas[ty, tx, 2] * 0.45),
        )
        cv2.ellipse(
            canvas,
            (tx + shadow_offset_x, ty + shadow_offset_y),
            (crown_radius_x, crown_radius_y),
            angle=angle,
            startAngle=0,
            endAngle=360,
            color=shadow_color,
            thickness=-1,
        )

        # Draw multi-layer canopy foliage (outer leaves to inner bright canopy crest)
        layers = 4
        for l in range(layers):
            layer_frac = 1.0 - (l * 0.22)
            rx = max(3, int(crown_radius_x * layer_frac))
            ry = max(3, int(crown_radius_y * layer_frac))

            # Realistic green spectral variations
            green_val = int(min(240, 110 + (l * 28) + rng.randint(-10, 10)))
            red_val = int(max(10, 30 + (l * 12) + rng.randint(-5, 5)))
            blue_val = int(max(5, 15 + (l * 8) + rng.randint(-5, 5)))
            foliage_color = (red_val, green_val, blue_val)

            cv2.ellipse(
                canvas,
                (tx, ty),
                (rx, ry),
                angle=angle,
                startAngle=0,
                endAngle=360,
                color=foliage_color,
                thickness=-1,
            )

        # Highlight crest specular reflections
        crest_x = tx - int(crown_radius_x * 0.2)
        crest_y = ty - int(crown_radius_y * 0.2)
        cv2.circle(
            canvas,
            (crest_x, crest_y),
            max(2, int(crown_radius_x * 0.2)),
            (red_val + 20, min(255, green_val + 25), blue_val + 10),
            -1,
        )

    return canvas


def ensure_sample_assets_exist(output_dir: Path) -> Path:
    """
    Saves a high-resolution benchmark aerial sample image to disk.

    Args:
        output_dir: Directory where sample images are persisted.

    Returns:
        Path to generated sample image file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_file = output_dir / "ciet_forest_aerial_benchmark.jpg"
    if not sample_file.exists():
        sample_img = generate_aerial_forest_sample(width=1024, height=1024, num_trees=40)
        # Convert RGB to BGR for cv2 imwrite
        bgr = cv2.cvtColor(sample_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(sample_file), bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    return sample_file
