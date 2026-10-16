"""
Enterprise Unit and Regression Test Suite for CIET Tree Stocking Platform.
Validates structural data models, NMS overlapping canopy suppression,
canopy density math, anomaly detection, telemetry logging, and model inference.
"""

from __future__ import annotations

import logging
from typing import List

import numpy as np
import pytest
from pydantic import ValidationError

from src.ml.engine import (
    BoundingBox,
    DetectionResult,
    TreeDetector,
    compute_iou,
    non_maximum_suppression,
)
from src.utils.analytics import (
    boxes_to_coordinate_matrix,
    calculate_canopy_coverage,
    detect_bounding_box_anomalies,
    generate_canopy_stocking_report,
    log_inference_metrics,
)
from src.utils.visualization import render_canopy_overlay


# ============================================================================
# 1. Pydantic Structural Data Model Tests
# ============================================================================


def test_bounding_box_valid_initialization() -> None:
    """Verifies that a valid BoundingBox instantiates with correct geometric properties."""
    box = BoundingBox(
        x1=10.0,
        y1=20.0,
        x2=110.0,
        y2=120.0,
        confidence=0.88,
        class_id=0,
        class_name="tree_crown",
    )
    assert box.width == 100.0
    assert box.height == 100.0
    assert box.area == 10000.0
    assert box.center == (60.0, 70.0)
    assert box.confidence == 0.88
    assert box.class_name == "tree_crown"


def test_bounding_box_invalid_inversion_coordinates() -> None:
    """Ensures inverted coordinate ranges (x2 < x1 or y2 < y1) trigger validation errors."""
    with pytest.raises(ValueError, match="Invalid horizontal coordinates"):
        BoundingBox(x1=100.0, y1=20.0, x2=50.0, y2=120.0, confidence=0.75)

    with pytest.raises(ValueError, match="Invalid vertical coordinates"):
        BoundingBox(x1=10.0, y1=150.0, x2=50.0, y2=120.0, confidence=0.75)


def test_bounding_box_confidence_range_enforcement() -> None:
    """Ensures out-of-range confidence scores raise Pydantic ValidationError."""
    with pytest.raises(ValidationError):
        BoundingBox(x1=0.0, y1=0.0, x2=10.0, y2=10.0, confidence=1.5)

    with pytest.raises(ValidationError):
        BoundingBox(x1=0.0, y1=0.0, x2=10.0, y2=10.0, confidence=-0.1)


def test_detection_result_synchronization() -> None:
    """Validates that DetectionResult auto-synchronizes total_detections count."""
    boxes = [
        BoundingBox(x1=10.0, y1=10.0, x2=50.0, y2=50.0, confidence=0.9),
        BoundingBox(x1=60.0, y1=60.0, x2=100.0, y2=100.0, confidence=0.85),
    ]
    result = DetectionResult(
        boxes=boxes,
        image_width=640,
        image_height=480,
        inference_time_ms=18.4,
        model_name="ciet_yolov8_test",
    )
    assert result.total_detections == 2
    summary = result.to_dict_summary()
    assert summary["total_detections"] == 2
    assert summary["image_dimensions"] == "640x480"
    assert summary["inference_time_ms"] == 18.4


# ============================================================================
# 2. Overlapping Canopy Suppression Engine (Custom NMS) Tests
# ============================================================================


def test_compute_iou_known_geometries() -> None:
    """Verifies IoU math for distinct, identical, and partially overlapping rectangles."""
    box_a = np.array([0.0, 0.0, 100.0, 100.0])
    # Identical box -> IoU = 1.0
    assert pytest.approx(compute_iou(box_a, box_a), 1e-4) == 1.0

    # Completely disjoint box -> IoU = 0.0
    box_disjoint = np.array([200.0, 200.0, 300.0, 300.0])
    assert compute_iou(box_a, box_disjoint) == 0.0

    # 50% horizontal overlap: width 100, x ranges [0, 100] and [50, 150]
    # intersection: 50 * 100 = 5000; union: 10000 + 10000 - 5000 = 15000 -> IoU = 1/3
    box_overlap = np.array([50.0, 0.0, 150.0, 100.0])
    assert pytest.approx(compute_iou(box_a, box_overlap), 1e-4) == 5000.0 / 15000.0


def test_nms_suppresses_duplicate_overlapping_canopies() -> None:
    """Ensures duplicate or heavily overlapping detections are suppressed, retaining highest confidence."""
    # Box 0: Higher confidence crown (conf=0.92)
    # Box 1: Near duplicate overlapping crown (conf=0.75, IoU > 0.8)
    # Box 2: Disjoint separate tree crown (conf=0.88)
    boxes = np.array(
        [
            [10.0, 10.0, 60.0, 60.0],
            [12.0, 11.0, 62.0, 59.0],
            [120.0, 120.0, 180.0, 180.0],
        ],
        dtype=np.float32,
    )
    scores = np.array([0.92, 0.75, 0.88], dtype=np.float32)

    kept = non_maximum_suppression(boxes, scores, iou_threshold=0.5, conf_threshold=0.45)
    assert 0 in kept
    assert 2 in kept
    assert 1 not in kept  # Box 1 suppressed by Box 0
    assert len(kept) == 2


def test_nms_filters_sub_threshold_confidence() -> None:
    """Ensures candidates below confidence threshold are strictly eliminated."""
    boxes = np.array([[10.0, 10.0, 50.0, 50.0], [60.0, 60.0, 90.0, 90.0]], dtype=np.float32)
    scores = np.array([0.40, 0.25], dtype=np.float32)

    kept = non_maximum_suppression(boxes, scores, iou_threshold=0.5, conf_threshold=0.45)
    assert len(kept) == 0


def test_nms_handles_empty_inputs_safely() -> None:
    """Ensures empty candidate inputs return empty list without throwing errors."""
    empty_boxes = np.empty((0, 4), dtype=np.float32)
    empty_scores = np.empty((0,), dtype=np.float32)
    assert non_maximum_suppression(empty_boxes, empty_scores) == []


# ============================================================================
# 3. Canopy Coverage Density Math & Matrix Analytics Tests
# ============================================================================


def test_canopy_coverage_zero_detections() -> None:
    """Zero tree detections must yield exactly 0.0% coverage."""
    coverage_pct, covered_px, total_px = calculate_canopy_coverage(
        boxes=[], image_width=500, image_height=500
    )
    assert coverage_pct == 0.0
    assert covered_px == 0
    assert total_px == 250000


def test_canopy_coverage_exact_half_grid() -> None:
    """A box covering exactly 50% of the image grid must yield 50.0% density."""
    box = BoundingBox(x1=0.0, y1=0.0, x2=200.0, y2=100.0, confidence=0.9)
    # Image is 200 x 200 -> total 40000; box area = 200 * 100 = 20000 (50%)
    coverage_pct, covered_px, total_px = calculate_canopy_coverage(
        boxes=[box], image_width=200, image_height=200
    )
    assert pytest.approx(coverage_pct, abs=0.5) == 50.0


def test_canopy_coverage_prevents_double_counting_overlapping_canopies() -> None:
    """
    Crucial forestry invariant: two identical overlapping boxes must NOT double count
    to 100%; they must yield exactly 50%.
    """
    box1 = BoundingBox(x1=0.0, y1=0.0, x2=200.0, y2=100.0, confidence=0.95)
    box2 = BoundingBox(x1=0.0, y1=0.0, x2=200.0, y2=100.0, confidence=0.80)

    coverage_pct, _, _ = calculate_canopy_coverage(
        boxes=[box1, box2], image_width=200, image_height=200
    )
    assert pytest.approx(coverage_pct, abs=0.5) == 50.0


def test_boxes_to_coordinate_matrices() -> None:
    """Verifies conversion of BoundingBox objects to NumPy coordinate and centroid matrices."""
    b1 = BoundingBox(x1=10.0, y1=20.0, x2=30.0, y2=40.0, confidence=0.9)
    b2 = BoundingBox(x1=50.0, y1=60.0, x2=70.0, y2=80.0, confidence=0.85)

    matrix = boxes_to_coordinate_matrix([b1, b2])
    assert matrix.shape == (2, 4)
    assert np.allclose(matrix[0], [10.0, 20.0, 30.0, 40.0])

    empty_mat = boxes_to_coordinate_matrix([])
    assert empty_mat.shape == (0, 4)


# ============================================================================
# 4. Anomaly Detection and Telemetry Warnings Tests
# ============================================================================


def test_detect_bounding_box_anomalies_giant_box(caplog: pytest.LogCaptureFixture) -> None:
    """Verifies that abnormally large boxes trigger logging warnings and anomaly alerts."""
    caplog.set_level(logging.WARNING, logger="ciet.utils.analytics")
    # Image 1000x1000 = 1,000,000. Box 900x900 = 810,000 (81% > 50% threshold)
    giant_box = BoundingBox(x1=50.0, y1=50.0, x2=950.0, y2=950.0, confidence=0.9)

    count, descs = detect_bounding_box_anomalies(
        boxes=[giant_box], image_width=1000, image_height=1000, max_box_area_ratio=0.5
    )
    assert count == 1
    assert "exceeding max area ratio" in descs[0]
    assert any("ANOMALY-LARGE-BOX" in record.message for record in caplog.records)


def test_detect_bounding_box_anomalies_aspect_ratio_sliver() -> None:
    """Verifies that extreme aspect ratios (e.g. 10:1 slivers) trigger anomaly detection."""
    sliver_box = BoundingBox(x1=10.0, y1=10.0, x2=210.0, y2=20.0, confidence=0.8)
    # Width 200, height 10 -> aspect ratio 20:1
    count, descs = detect_bounding_box_anomalies(
        boxes=[sliver_box], image_width=1000, image_height=1000, max_aspect_ratio=4.0
    )
    assert count == 1
    assert "abnormal aspect ratio" in descs[0]


def test_log_inference_metrics_sla_warning(caplog: pytest.LogCaptureFixture) -> None:
    """Verifies that exceeding SLA latency threshold triggers a system performance warning."""
    caplog.set_level(logging.WARNING, logger="ciet.utils.analytics")
    log_inference_metrics(
        latency_ms=750.0,
        detection_count=42,
        canopy_density=35.5,
        threshold_warning_ms=500.0,
    )
    assert any("PERFORMANCE WARNING" in record.message for record in caplog.records)


def test_generate_canopy_stocking_report() -> None:
    """Validates complete CanopyStockingReport aggregation."""
    boxes = [
        BoundingBox(x1=10.0, y1=10.0, x2=60.0, y2=60.0, confidence=0.92),
        BoundingBox(x1=70.0, y1=70.0, x2=120.0, y2=120.0, confidence=0.88),
    ]
    report = generate_canopy_stocking_report(
        boxes=boxes,
        image_width=500,
        image_height=500,
        inference_latency_ms=120.5,
    )
    assert report.total_trees == 2
    assert report.canopy_coverage_density_pct > 0.0
    assert report.crown_footprint_density_pct > 0.0
    assert report.mean_confidence == 0.90
    assert report.inference_latency_ms == 120.5


# ============================================================================
# 5. Visualization and Inference Pipeline Integration Tests
# ============================================================================


def test_render_canopy_overlay_output_shape() -> None:
    """Verifies that render_canopy_overlay produces correct RGB image dimensions."""
    canvas = np.zeros((300, 400, 3), dtype=np.uint8)
    boxes = [BoundingBox(x1=20.0, y1=20.0, x2=80.0, y2=80.0, confidence=0.95)]

    rendered = render_canopy_overlay(canvas, boxes, draw_masks=True, draw_labels=True)
    assert isinstance(rendered, np.ndarray)
    assert rendered.shape == (300, 400, 3)
    assert rendered.dtype == np.uint8


def test_tree_detector_initialization_and_fallback() -> None:
    """
    Tests resilient model loading: when custom weights are absent,
    the pipeline securely initializes the fallback YOLO baseline architecture.
    """
    detector = TreeDetector(
        model_path="models/non_existent_ciet_custom_weights.pt",
        conf_threshold=0.45,
        iou_threshold=0.5,
    )
    assert detector.model is not None
    assert "yolov8n" in detector.active_weights_path.lower()

    # Test inference over synthetic overhead tree image
    synthetic_image = np.ones((256, 256, 3), dtype=np.uint8) * 128
    result = detector.detect(synthetic_image)

    assert isinstance(result, DetectionResult)
    assert result.image_width == 256
    assert result.image_height == 256
    assert result.inference_time_ms >= 0.0
    assert isinstance(result.boxes, list)
