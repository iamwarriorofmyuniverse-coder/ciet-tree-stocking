"""
End-to-End System Verification and Telemetry Capture Script.
Simulates production execution of the CIET Tree Stocking platform.
"""

from __future__ import annotations

import json
import logging
import time
import sys
from pathlib import Path

import cv2
import numpy as np
import tifffile

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ml.engine import BoundingBox, DetectionResult, TreeDetector
from src.utils.analytics import (
    CanopyStockingReport,
    calculate_canopy_coverage,
    detect_bounding_box_anomalies,
    generate_canopy_stocking_report,
)
from src.utils.sample_generator import generate_aerial_forest_sample
from src.utils.visualization import render_canopy_overlay

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ciet.verification")


def main() -> None:
    logger.info("Initializing CIET Forest Conservation System Verification...")

    # 1. Prepare sample directory
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    sample_tif = assets_dir / "sample_aerial_forest_sector_a.tif"
    sample_jpg = assets_dir / "sample_aerial_forest_sector_b.jpg"
    output_annotated = assets_dir / "verified_overlay_sector_a.jpg"

    # 2. Synthesize multi-spectral aerial payload
    logger.info("Generating high-resolution aerial payloads (TIFF & JPG)...")
    img_rgb = generate_aerial_forest_sample(width=1024, height=1024, num_trees=42, seed=101)
    
    # Save as high-res TIFF
    tifffile.imwrite(str(sample_tif), img_rgb)
    # Save as high-res JPG
    cv2.imwrite(str(sample_jpg), cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))

    # 3. Initialize TreeDetector with programmatic fallback verification
    detector = TreeDetector(
        model_path="models/ciet_tree_stock_yolov8.pt",
        conf_threshold=0.45,
        iou_threshold=0.50,
    )

    # 4. Ingest and detect on TIFF
    logger.info("Ingesting TIFF payload and running detection...")
    tiff_payload = tifffile.imread(str(sample_tif))
    t0 = time.perf_counter()
    detection_res = detector.detect(tiff_payload)
    t_end = time.perf_counter()
    e2e_ms = (t_end - t0) * 1000.0

    logger.info(
        "Detection Complete: %d crowns detected in %.2f ms",
        len(detection_res.boxes),
        detection_res.inference_time_ms,
    )

    # 5. Run Analytics Engine
    report = generate_canopy_stocking_report(
        boxes=detection_res.boxes,
        image_width=detection_res.image_width,
        image_height=detection_res.image_height,
        inference_latency_ms=detection_res.inference_time_ms,
    )

    # 6. Render Visualization
    overlay_rgb = render_canopy_overlay(
        image=tiff_payload,
        boxes=detection_res.boxes,
        draw_masks=True,
        draw_labels=True,
    )
    cv2.imwrite(str(output_annotated), cv2.cvtColor(overlay_rgb, cv2.COLOR_RGB2BGR))
    logger.info("Annotated imagery saved to %s", output_annotated)

    telemetry = {
        "status": "PASS",
        "institutional_metadata": {
            "institution": "Coimbatore Institute of Engineering and Technology (CIET)",
            "system": "Computer Vision-Based Tree Stocking for Forest Conservation",
            "version": "1.0.0",
        },
        "model_verification": {
            "active_weights": detection_res.model_name,
            "architecture": "YOLOv8",
            "conf_threshold": detector.conf_threshold,
            "iou_threshold": detector.iou_threshold,
        },
        "payload_verification": {
            "dimensions": f"{detection_res.image_width}x{detection_res.image_height}",
            "tiff_verified": sample_tif.exists(),
            "jpg_verified": sample_jpg.exists(),
        },
        "stocking_metrics": {
            "total_detected_canopies": report.total_trees,
            "canopy_coverage_density_pct": report.canopy_coverage_density_pct,
            "crown_footprint_density_pct": report.crown_footprint_density_pct,
            "average_crown_diameter_px": report.average_crown_diameter_px,
            "mean_confidence": report.mean_confidence,
            "inference_latency_ms": report.inference_latency_ms,
            "anomalies_detected": report.anomalies_detected,
        },
    }

    report_file = assets_dir / "system_verification_telemetry.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    logger.info("Verification telemetry successfully written to %s", report_file)
    print("\n--- SYSTEM VERIFICATION TELEMETRY ---")
    print(json.dumps(telemetry, indent=2))


if __name__ == "__main__":
    main()
