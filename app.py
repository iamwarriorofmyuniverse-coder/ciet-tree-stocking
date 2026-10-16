"""
CIET Coimbatore — Enterprise Forest Conservation & Tree Stocking Platform.
Autonomous Computer Vision Airborne Forest Inventory & Crown Stocking Assessment.
"""

from __future__ import annotations

import io
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="CIET Forest Stocking Platform",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply enterprise styling
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }
    .main-header h1 {
        font-size: 26px;
        font-weight: 700;
        margin: 0 0 6px 0;
        color: #f0fdf4;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 14px;
        margin: 0;
        color: #a7f3d0;
        font-weight: 400;
    }
    .badge-ciet {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 10px;
        font-weight: 600;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .metric-card-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
    }
    .metric-card-value {
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .metric-card-sub {
        font-size: 12px;
        color: #10b981;
        margin-top: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Imports from src package
from src.ml.engine import BoundingBox, DetectionResult, TreeDetector
from src.utils.analytics import (
    CanopyStockingReport,
    boxes_to_coordinate_matrix,
    calculate_canopy_coverage,
    generate_canopy_stocking_report,
)
from src.utils.sample_generator import generate_aerial_forest_sample
from src.utils.visualization import render_canopy_overlay


@st.cache_resource(show_spinner="Initializing CIET Tree Detector Model...")
def get_detector(
    model_path: Optional[str] = None,
    conf_threshold: float = 0.45,
    iou_threshold: float = 0.50,
) -> TreeDetector:
    """Cached singleton instance of TreeDetector."""
    return TreeDetector(
        model_path=model_path,
        conf_threshold=conf_threshold,
        iou_threshold=iou_threshold,
    )


def load_uploaded_image(file_payload: io.BytesIO, filename: str) -> np.ndarray:
    """
    Safely ingests and decodes multi-spectral and overhead RGB TIFF and JPG imagery payloads.
    """
    file_bytes = file_payload.read()
    file_payload.seek(0)
    ext = Path(filename).suffix.lower()

    if ext in [".tif", ".tiff"]:
        try:
            import tifffile
            with io.BytesIO(file_bytes) as bio:
                arr = tifffile.imread(bio)
                if arr.ndim == 2:
                    arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)
                elif arr.ndim == 3 and arr.shape[2] >= 3:
                    arr = arr[:, :, :3]
                # Normalize 16-bit to 8-bit if needed
                if arr.dtype == np.uint16:
                    arr = (arr / 256).astype(np.uint8)
                elif arr.dtype != np.uint8:
                    arr = cv2.normalize(arr, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                return arr
        except Exception:
            # Fallback to PIL
            pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            return np.array(pil_img)
    else:
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        return np.array(pil_img)


def main() -> None:
    # 1. Institutional Brand Identity Header
    st.markdown(
        """
        <div class="main-header">
            <h1>CIET Coimbatore — Enterprise Forest Conservation & Tree Stocking Platform</h1>
            <p>Autonomous Computer Vision Airborne Forest Inventory, Crown Stocking & Canopy Density Analytics</p>
            <div class="badge-ciet">Coimbatore Institute of Engineering and Technology (CIET) • Research & Development</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Pipeline Configuration")
        st.markdown("Precision tuning parameters for canopy isolation and overlap suppression.")

        custom_model_path = st.text_input(
            "Model Weights Path",
            value="models/ciet_tree_stock_yolov8.pt",
            help="Custom CIET weights. Programmatic fallback triggers yolov8n.pt if absent.",
        )

        conf_threshold = st.slider(
            "Confidence Floor (Threshold)",
            min_value=0.10,
            max_value=0.95,
            value=0.45,
            step=0.05,
            help="Minimum detection confidence required to register a tree canopy crown.",
        )

        iou_threshold = st.slider(
            "Canopy Suppression IoU (NMS)",
            min_value=0.10,
            max_value=0.90,
            value=0.50,
            step=0.05,
            help="Intersection-over-Union threshold for the overlapping canopy suppression engine.",
        )

        st.markdown("---")
        st.header("🎨 Visualization Aesthetics")

        draw_crown_masks = st.checkbox("Shade Crown Footprints (Masks)", value=True)
        draw_labels = st.checkbox("Display Crown Badges & Confidences", value=True)
        crown_geometry = st.radio(
            "Crown Geometry Calculation",
            options=["Inscribed Ellipse (Realistic Foliage)", "Rectangular Bounding Envelope"],
            index=0,
        )
        use_elliptical = crown_geometry.startswith("Inscribed")

        palette_choice = st.selectbox(
            "Bounding Box Accent Color",
            options=["Emerald Green", "Forest Neon Lime", "Golden Amber", "Cyan Sky"],
            index=0,
        )
        palette_map = {
            "Emerald Green": (34, 197, 94),
            "Forest Neon Lime": (0, 255, 128),
            "Golden Amber": (245, 158, 11),
            "Cyan Sky": (6, 182, 212),
        }
        accent_color_rgb = palette_map[palette_choice]
        # Convert RGB to BGR for OpenCV
        accent_color_bgr = (accent_color_rgb[2], accent_color_rgb[1], accent_color_rgb[0])

        st.markdown("---")
        st.markdown(
            "**System Architecture:**\n"
            "- Engine: Ultralytics YOLOv8\n"
            "- Post-Processor: Custom Spatial NMS\n"
            "- Telemetry: Enterprise Structured Logger"
        )

    # 3. Imagery Ingestion Pipeline
    col_input1, col_input2 = st.columns([2, 1])

    with col_input1:
        uploaded_file = st.file_uploader(
            "Upload Overhead Aerial/Satellite Payload (TIFF, TIF, JPG, PNG)",
            type=["tif", "tiff", "jpg", "jpeg", "png"],
            help="Accepts high-resolution drone ortho-mosaics and aerial reconnaissance imagery.",
        )

    with col_input2:
        st.markdown("**Quick Test Payload**")
        use_sample = st.button("🌲 Load CIET Aerial Forest Benchmark Sample", use_container_width=True)

    input_image_array: Optional[np.ndarray] = None
    source_name = ""

    if uploaded_file is not None:
        try:
            input_image_array = load_uploaded_image(uploaded_file, uploaded_file.name)
            source_name = uploaded_file.name
            st.success(f"Successfully decoded overhead image: `{source_name}` ({input_image_array.shape[1]}x{input_image_array.shape[0]} px)")
        except Exception as err:
            st.error(f"Failed to decode uploaded image payload: {err}")
    elif use_sample or "sample_cached" in st.session_state:
        st.session_state["sample_cached"] = True
        input_image_array = generate_aerial_forest_sample(width=1024, height=1024, num_trees=38, seed=42)
        source_name = "ciet_aerial_forest_benchmark.jpg"
        st.info("Loaded benchmark drone ortho-mosaic simulation (1024x1024 px, CIET Sector-IV).")

    if input_image_array is None:
        st.info("👋 Please upload an aerial image or click **'Load CIET Aerial Forest Benchmark Sample'** to start analysis.")
        return

    # 4. Asynchronous Inference Execution
    with st.spinner("Executing Computer Vision Stocking Pipeline..."):
        try:
            detector = get_detector(
                model_path=custom_model_path,
                conf_threshold=conf_threshold,
                iou_threshold=iou_threshold,
            )
            # Run detection
            detection_result: DetectionResult = detector.detect(
                image_input=input_image_array,
                override_conf=conf_threshold,
                override_iou=iou_threshold,
            )

            # Generate structured analytics report
            report: CanopyStockingReport = generate_canopy_stocking_report(
                boxes=detection_result.boxes,
                image_width=detection_result.image_width,
                image_height=detection_result.image_height,
                inference_latency_ms=detection_result.inference_time_ms,
            )

        except Exception as exc:
            st.error(f"Inference Pipeline Error: {exc}")
            st.exception(exc)
            return

    # 5. Telemetry & Metric Widgets
    st.markdown("### 📊 Forest Inventory & Canopy Stocking Telemetry")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    with m_col1:
        st.metric(
            label="Total Individual Trees",
            value=f"{report.total_trees:,} crowns",
            delta=f"Stocking Density: {'Dense' if report.total_trees > 25 else 'Moderate'}",
        )

    with m_col2:
        density_val = report.crown_footprint_density_pct if use_elliptical else report.canopy_coverage_density_pct
        st.metric(
            label="Canopy Coverage Density",
            value=f"{density_val:.1f}%",
            delta=f"FAO Class: {'Closed Canopy' if density_val >= 40 else 'Open Canopy' if density_val >= 10 else 'Sparse'}",
        )

    with m_col3:
        st.metric(
            label="Inference Computational Latency",
            value=f"{report.inference_latency_ms:.1f} ms",
            delta="SLA Nominal (<500ms)" if report.inference_latency_ms < 500 else "SLA Breach",
            delta_color="normal" if report.inference_latency_ms < 500 else "inverse",
        )

    with m_col4:
        st.metric(
            label="Mean Crown Diameter",
            value=f"{report.average_crown_diameter_px:.1f} px",
            delta=f"Mean Confidence: {report.mean_confidence:.0%}",
        )

    # 6. Visualization & Comparative Tabs
    rendered_overlay = render_canopy_overlay(
        image=input_image_array,
        boxes=detection_result.boxes,
        draw_masks=draw_crown_masks,
        draw_labels=draw_labels,
        box_color_bgr=accent_color_bgr,
    )

    tab_vis, tab_raw, tab_coords, tab_audit = st.tabs([
        "🌿 Canopy Crown Overlay",
        "📷 Raw Aerial Payload",
        "📐 Coordinate Spatial Matrix",
        "🛡️ Quality & Anomaly Audit",
    ])

    with tab_vis:
        st.image(
            rendered_overlay,
            caption=f"Overlaid Crown Detections | Isolated Canopies: {len(detection_result.boxes)} | Density: {density_val:.1f}%",
            use_container_width=True,
        )

    with tab_raw:
        st.image(
            input_image_array,
            caption=f"Source Overhead Image ({detection_result.image_width} x {detection_result.image_height} px)",
            use_container_width=True,
        )

    with tab_coords:
        st.subheader("Spatial Matrix of Identified Tree Crowns")
        if detection_result.boxes:
            rows: List[Dict[str, Any]] = []
            for i, b in enumerate(detection_result.boxes, 1):
                rows.append({
                    "Crown ID": f"#{i:03d}",
                    "X1 (px)": round(b.x1, 1),
                    "Y1 (px)": round(b.y1, 1),
                    "X2 (px)": round(b.x2, 1),
                    "Y2 (px)": round(b.y2, 1),
                    "Width (px)": round(b.width, 1),
                    "Height (px)": round(b.height, 1),
                    "Crown Area (px²)": round(b.area, 1),
                    "Confidence": f"{b.confidence:.2%}",
                    "Class": b.class_name,
                })
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No canopy crowns detected matching current confidence parameters.")

    with tab_audit:
        st.subheader("Structural Anomaly & Precision Audit")
        if report.anomalies_detected > 0:
            st.warning(f"⚠️ {report.anomalies_detected} Spatial Anomaly/Anomalies Detected:")
            for ad in report.anomaly_descriptions:
                st.write(f"- {ad}")
        else:
            st.success("✅ Flawless Structural Integrity: 0 geometric anomalies detected. All crown bounding boxes fall within natural forestry tolerances.")

        st.json({
            "model_metadata": {
                "active_weights": detection_result.model_name,
                "confidence_threshold": conf_threshold,
                "nms_iou_threshold": iou_threshold,
            },
            "telemetry": {
                "total_grid_pixels": report.total_grid_pixels,
                "covered_pixels": report.canopy_covered_pixels,
                "rectangular_density_pct": report.canopy_coverage_density_pct,
                "elliptical_density_pct": report.crown_footprint_density_pct,
                "inference_latency_ms": report.inference_latency_ms,
            }
        })

    # 7. Export Pipeline
    st.markdown("---")
    st.subheader("📥 Export Forest Stocking Inventory Data")
    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        # Buffer for annotated image
        pil_rendered = Image.fromarray(rendered_overlay)
        img_buffer = io.BytesIO()
        pil_rendered.save(img_buffer, format="JPEG", quality=95)
        st.download_button(
            label="💾 Download Annotated Overhead Imagery (JPEG)",
            data=img_buffer.getvalue(),
            file_name=f"ciet_annotated_stocking_{int(time.time())}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )

    with exp_col2:
        report_json = report.model_dump_json(indent=2)
        st.download_button(
            label="📊 Download Stocking Telemetry Report (JSON)",
            data=report_json,
            file_name=f"ciet_stocking_report_{int(time.time())}.json",
            mime="application/json",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
