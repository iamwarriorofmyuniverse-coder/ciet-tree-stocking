"""
Reusable Analytics Engine for Tree Stocking and Forest Conservation.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).
"""

from __future__ import annotations

import logging
import math
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from pydantic import BaseModel, Field

from src.ml.engine import BoundingBox

# Configure enterprise logger for analytics and system telemetry
logger = logging.getLogger("ciet.utils.analytics")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class CanopyStockingReport(BaseModel):
    """
    Comprehensive structured analytical report for forest stocking and canopy density.
    """

    total_trees: int = Field(..., ge=0, description="Total individual tree crowns detected")
    canopy_coverage_density_pct: float = Field(
        ..., ge=0.0, le=100.0, description="Exact bounding box union canopy coverage density percentage"
    )
    crown_footprint_density_pct: float = Field(
        ..., ge=0.0, le=100.0, description="Inscribed circular/elliptical crown footprint density percentage"
    )
    total_grid_pixels: int = Field(..., gt=0, description="Total pixels evaluated in imagery payload")
    canopy_covered_pixels: int = Field(..., ge=0, description="Unique pixels covered by canopy union")
    average_crown_diameter_px: float = Field(
        ..., ge=0.0, description="Mean equivalent diameter of detected tree crowns in pixels"
    )
    mean_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Mean detection confidence across all validated crowns"
    )
    inference_latency_ms: float = Field(
        ..., ge=0.0, description="Model inference runtime latency in milliseconds"
    )
    anomalies_detected: int = Field(
        default=0, ge=0, description="Count of bounding box geometric/scale anomalies detected"
    )
    anomaly_descriptions: List[str] = Field(
        default_factory=list, description="Descriptive log messages for detected anomalies"
    )


def boxes_to_coordinate_matrix(boxes: List[BoundingBox]) -> np.ndarray:
    """
    Converts list of BoundingBox objects into an (N, 4) NumPy coordinate matrix.

    Args:
        boxes: List of BoundingBox models.

    Returns:
        NumPy array of shape (N, 4) with columns [x1, y1, x2, y2].
    """
    if not boxes:
        return np.empty((0, 4), dtype=np.float32)
    coords = [[b.x1, b.y1, b.x2, b.y2] for b in boxes]
    return np.array(coords, dtype=np.float32)


def boxes_to_centroids_matrix(boxes: List[BoundingBox]) -> np.ndarray:
    """
    Extracts an (N, 2) NumPy matrix containing canopy crown centroids (cx, cy).

    Args:
        boxes: List of BoundingBox models.

    Returns:
        NumPy array of shape (N, 2) with columns [cx, cy].
    """
    if not boxes:
        return np.empty((0, 2), dtype=np.float32)
    centroids = [b.center for b in boxes]
    return np.array(centroids, dtype=np.float32)


def calculate_canopy_coverage(
    boxes: List[BoundingBox],
    image_width: int,
    image_height: int,
    use_elliptical_crowns: bool = False,
    downscale_limit: int = 2048,
) -> Tuple[float, int, int]:
    """
    Calculates exact canopy coverage density percentage against the total pixel area grid.
    Utilizes a binary occupancy grid to prevent double-counting overlapping canopies.

    Args:
        boxes: List of validated BoundingBox instances.
        image_width: Total image width in pixels.
        image_height: Total image height in pixels.
        use_elliptical_crowns: If True, rasterizes elliptical crown footprints instead of rectangles.
        downscale_limit: Max grid dimension for fast rasterization of extreme high-res aerial payloads.

    Returns:
        Tuple of (canopy_coverage_pct, covered_pixels, total_pixels).
    """
    if image_width <= 0 or image_height <= 0:
        raise ValueError(f"Invalid image dimensions: {image_width}x{image_height}")

    total_pixels = image_width * image_height
    if not boxes:
        return 0.0, 0, total_pixels

    # Scale factor for ultra-high-resolution aerial TIFF images to ensure constant-time sub-millisecond grid operations
    scale = 1.0
    max_dim = max(image_width, image_height)
    if max_dim > downscale_limit:
        scale = downscale_limit / float(max_dim)

    grid_w = max(1, int(round(image_width * scale)))
    grid_h = max(1, int(round(image_height * scale)))

    # Allocate binary occupancy grid
    occupancy_grid = np.zeros((grid_h, grid_w), dtype=np.uint8)

    for box in boxes:
        gx1 = max(0, min(int(round(box.x1 * scale)), grid_w))
        gy1 = max(0, min(int(round(box.y1 * scale)), grid_h))
        gx2 = max(gx1, min(int(round(box.x2 * scale)), grid_w))
        gy2 = max(gy1, min(int(round(box.y2 * scale)), grid_h))

        if gx2 <= gx1 or gy2 <= gy1:
            continue

        if use_elliptical_crowns:
            center_x = (gx1 + gx2) // 2
            center_y = (gy1 + gy2) // 2
            axes_x = max(1, (gx2 - gx1) // 2)
            axes_y = max(1, (gy2 - gy1) // 2)
            cv2.ellipse(
                occupancy_grid,
                (center_x, center_y),
                (axes_x, axes_y),
                angle=0,
                startAngle=0,
                endAngle=360,
                color=1,
                thickness=-1,
            )
        else:
            occupancy_grid[gy1:gy2, gx1:gx2] = 1

    covered_grid_pixels = int(np.count_nonzero(occupancy_grid))
    total_grid_pixels = grid_w * grid_h

    density_pct = (covered_grid_pixels / float(total_grid_pixels)) * 100.0
    clamped_density_pct = max(0.0, min(100.0, float(density_pct)))

    # Map covered pixels back to native resolution for telemetry
    estimated_native_covered = int(round((clamped_density_pct / 100.0) * total_pixels))

    return round(clamped_density_pct, 2), estimated_native_covered, total_pixels


def detect_bounding_box_anomalies(
    boxes: List[BoundingBox],
    image_width: int,
    image_height: int,
    max_box_area_ratio: float = 0.50,
    min_box_area_ratio: float = 0.00005,
    max_aspect_ratio: float = 4.0,
) -> Tuple[int, List[str]]:
    """
    Inspects bounding boxes for spatial anomalies, such as unrealistic giant canopies,
    extreme aspect ratios (slivers), or microscopic noise artifacts.

    Logs system warnings whenever bounding box metrics exceed anomaly tolerances.

    Args:
        boxes: List of BoundingBox objects to inspect.
        image_width: Width of image payload.
        image_height: Height of image payload.
        max_box_area_ratio: Max plausible ratio of single box area to total image area.
        min_box_area_ratio: Min plausible ratio of single box area to total image area.
        max_aspect_ratio: Max allowable ratio between width and height.

    Returns:
        Tuple of (anomalies_count, list_of_warning_descriptions).
    """
    total_image_area = float(image_width * image_height)
    anomalies: List[str] = []

    for i, box in enumerate(boxes):
        box_area = box.area
        area_ratio = box_area / total_image_area if total_image_area > 0 else 0.0

        # Check for abnormally large bounding box (likely background ground false positive)
        if area_ratio > max_box_area_ratio:
            desc = (
                f"Box #{i} (class '{box.class_name}', conf {box.confidence:.2f}) "
                f"covers {area_ratio*100:.1f}% of image, exceeding max area ratio of "
                f"{max_box_area_ratio*100:.1f}%."
            )
            anomalies.append(desc)
            logger.warning("[ANOMALY-LARGE-BOX] %s", desc)

        # Check for microscopic noise
        if area_ratio < min_box_area_ratio:
            desc = (
                f"Box #{i} covers only {area_ratio*100:.4f}% of image, "
                f"below minimum area ratio of {min_box_area_ratio*100:.4f}%."
            )
            anomalies.append(desc)
            logger.warning("[ANOMALY-MICRO-BOX] %s", desc)

        # Check for abnormal aspect ratio (distorted sliver)
        w, h = box.width, box.height
        if h > 0 and w > 0:
            aspect = max(w / h, h / w)
            if aspect > max_aspect_ratio:
                desc = (
                    f"Box #{i} exhibits abnormal aspect ratio of {aspect:.2f}:1 "
                    f"(w={w:.1f}px, h={h:.1f}px), exceeding threshold of {max_aspect_ratio:.1f}:1."
                )
                anomalies.append(desc)
                logger.warning("[ANOMALY-ASPECT-RATIO] %s", desc)

    return len(anomalies), anomalies


def log_inference_metrics(
    latency_ms: float,
    detection_count: int,
    canopy_density: float,
    threshold_warning_ms: float = 500.0,
) -> None:
    """
    Automated telemetry logging engine that tracks runtime inference latency
    and emits system warnings when latency or bounding box metrics breach operational budgets.

    Args:
        latency_ms: Measured end-to-end inference latency in milliseconds.
        detection_count: Total individual trees detected in payload.
        canopy_density: Calculated canopy density percentage.
        threshold_warning_ms: Maximum allowable SLA latency before triggering warning.
    """
    logger.info(
        "Inference Telemetry: latency=%.2fms | detections=%d | canopy_density=%.2f%%",
        latency_ms,
        detection_count,
        canopy_density,
    )

    if latency_ms > threshold_warning_ms:
        logger.warning(
            "[PERFORMANCE WARNING] Inference latency of %.2fms exceeded latency SLA threshold (%.2fms). "
            "Consider reducing input tile resolution or utilizing GPU acceleration.",
            latency_ms,
            threshold_warning_ms,
        )


def generate_canopy_stocking_report(
    boxes: List[BoundingBox],
    image_width: int,
    image_height: int,
    inference_latency_ms: float,
    latency_warning_threshold_ms: float = 500.0,
) -> CanopyStockingReport:
    """
    End-to-end analytics workflow: computes exact rectangular and elliptical canopy coverages,
    detects geometric anomalies, records telemetry metrics, and packages a structured report.

    Args:
        boxes: Validated bounding boxes.
        image_width: Width of image.
        image_height: Height of image.
        inference_latency_ms: Measured runtime latency in milliseconds.
        latency_warning_threshold_ms: Latency threshold for warning issuance.

    Returns:
        CanopyStockingReport Pydantic data model.
    """
    # 1. Exact rectangular bounding box union coverage
    box_density_pct, covered_pixels, total_pixels = calculate_canopy_coverage(
        boxes=boxes,
        image_width=image_width,
        image_height=image_height,
        use_elliptical_crowns=False,
    )

    # 2. Inscribed circular/elliptical crown footprint coverage
    crown_density_pct, _, _ = calculate_canopy_coverage(
        boxes=boxes,
        image_width=image_width,
        image_height=image_height,
        use_elliptical_crowns=True,
    )

    # 3. Geometric anomaly scan
    anomaly_count, anomaly_descs = detect_bounding_box_anomalies(
        boxes=boxes,
        image_width=image_width,
        image_height=image_height,
    )

    # 4. Telemetry logging
    log_inference_metrics(
        latency_ms=inference_latency_ms,
        detection_count=len(boxes),
        canopy_density=box_density_pct,
        threshold_warning_ms=latency_warning_threshold_ms,
    )

    # 5. Average diameter and mean confidence
    if boxes:
        equivalent_diameters = [2.0 * math.sqrt(b.area / math.pi) for b in boxes]
        avg_diameter = float(np.mean(equivalent_diameters))
        mean_conf = float(np.mean([b.confidence for b in boxes]))
    else:
        avg_diameter = 0.0
        mean_conf = 0.0

    return CanopyStockingReport(
        total_trees=len(boxes),
        canopy_coverage_density_pct=box_density_pct,
        crown_footprint_density_pct=crown_density_pct,
        total_grid_pixels=total_pixels,
        canopy_covered_pixels=covered_pixels,
        average_crown_diameter_px=round(avg_diameter, 2),
        mean_confidence=round(mean_conf, 3),
        inference_latency_ms=round(inference_latency_ms, 2),
        anomalies_detected=anomaly_count,
        anomaly_descriptions=anomaly_descs,
    )
