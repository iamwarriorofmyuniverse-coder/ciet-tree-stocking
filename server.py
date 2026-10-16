"""
Enterprise Web Application and REST API Subsystem.
Engineered with FastAPI for Coimbatore Institute of Engineering and Technology (CIET).
Features full security hardening, WAF protection, rate limiting, input sanitization, and DoS prevention.
"""

from __future__ import annotations

import asyncio
import base64
import io
import logging
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
from PIL import Image
import tifffile
from fastapi import FastAPI, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.inventory.database import TreeInventoryDatabase, get_inventory_db
from src.inventory.models import TreeProfile
from src.inventory.qr_engine import (
    decode_qr_image,
    generate_printable_tree_tag,
    generate_tree_qr_code,
)
from src.ml.engine import DetectionResult, TreeDetector
from src.security.firewall import (
    FileValidator,
    InputSanitizer,
    RateLimiter,
    SecurityFirewallMiddleware,
)
from src.utils.analytics import generate_canopy_stocking_report
from src.utils.sample_generator import generate_aerial_forest_sample
from src.utils.visualization import render_canopy_overlay

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ciet.server")

# Base directory setup
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Active public tunnel domain
PUBLIC_ONLINE_URL = os.environ.get(
    "PUBLIC_URL", "https://qualifications-asylum-workers-counter.trycloudflare.com"
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# FastAPI application instance
app = FastAPI(
    title="CIET Forest Conservation & Tree Stocking Platform",
    description="Enterprise API and Geolocation Service for Drone Tree Stocking, Biometrics, and QR Tagging.",
    version="2.1.0",
)

# 1. Attach Enterprise Security Firewall & Rate Limiting WAF Middleware
rate_limiter = RateLimiter()
app.add_middleware(SecurityFirewallMiddleware, rate_limiter=rate_limiter)

# 2. Configure Controlled CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 3. Mount Static Assets Directory (Icons, PWA Manifest, Service Worker)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.api_route("/manifest.json", methods=["GET", "HEAD"], include_in_schema=False)
async def get_pwa_manifest() -> FileResponse:
    """Serves W3C Progressive Web App manifest."""
    manifest_path = STATIC_DIR / "manifest.json"
    return FileResponse(manifest_path, media_type="application/manifest+json")


@app.api_route("/sw.js", methods=["GET", "HEAD"], include_in_schema=False)
async def get_service_worker() -> FileResponse:
    """Serves root-scoped Service Worker with permissive header."""
    sw_path = STATIC_DIR / "sw.js"
    return FileResponse(
        sw_path,
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"},
    )


# Concurrency throttle: limits concurrent YOLO inference executions on CPU
INFERENCE_SEMAPHORE = asyncio.Semaphore(2)


def get_db() -> TreeInventoryDatabase:
    """Helper retrieving inventory database configured with active public domain."""
    return get_inventory_db(base_url=PUBLIC_ONLINE_URL)


# Singleton ML Detector
_DETECTOR: Optional[TreeDetector] = None


def get_detector() -> TreeDetector:
    """Lazy loader for singleton TreeDetector."""
    global _DETECTOR
    if _DETECTOR is None:
        logger.info("Initializing baseline TreeDetector engine...")
        _DETECTOR = TreeDetector(
            model_path="models/ciet_tree_stock_yolov8.pt",
            conf_threshold=0.45,
            iou_threshold=0.50,
        )
    return _DETECTOR


# ============================================================================
# Global Sanitized Error Boundary Handler
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches unhandled exceptions safely without leaking internal stack traces."""
    incident_id = str(uuid.uuid4())[:8]
    logger.error(
        "[SECURITY INCIDENT-%s] Unhandled exception on path '%s': %s",
        incident_id,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": "An internal server error occurred. Telemetry has been recorded.",
            "incident_id": incident_id,
        },
    )


# ============================================================================
# 1. Frontend Web Views
# ============================================================================


@app.get("/", response_class=HTMLResponse)
async def home_dashboard(request: Request) -> Response:
    """Renders the interactive modern Single Page Application dashboard."""
    db = get_db()
    summary = db.get_metrics_summary()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"summary": summary, "total_trees": db.count()},
    )


@app.get("/tree/{tree_id}", response_class=HTMLResponse)
async def tree_passport_view(request: Request, tree_id: str) -> Response:
    """Renders the official Digital Tree Passport for a specific cataloged tree."""
    clean_id = InputSanitizer.sanitize_tree_id(tree_id)
    db = get_db()
    tree = db.get_tree(clean_id)
    if not tree:
        raise HTTPException(
            status_code=404,
            detail=f"Tree ID '{clean_id}' was not found in the CIET registry.",
        )
    return templates.TemplateResponse(
        request=request,
        name="tree_passport.html",
        context={"tree": tree},
    )


# ============================================================================
# 2. REST API: Inventory & Geolocation
# ============================================================================


@app.get("/api/trees", response_model=List[TreeProfile])
async def list_trees(
    sector: Optional[str] = None,
    iucn_status: Optional[str] = None,
    search: Optional[str] = None,
) -> List[TreeProfile]:
    """Retrieves all registered trees with optional query filters."""
    clean_sector = InputSanitizer.sanitize_string(sector)
    clean_iucn = InputSanitizer.sanitize_string(iucn_status)
    clean_search = InputSanitizer.sanitize_string(search)

    db = get_db()
    return db.list_trees(sector=clean_sector, iucn_status=clean_iucn, search_query=clean_search)


@app.get("/api/trees/{tree_id}", response_model=TreeProfile)
async def get_tree_details(tree_id: str) -> TreeProfile:
    """Retrieves complete biometric profile, coordinates, and telemetry for a single tree."""
    clean_id = InputSanitizer.sanitize_tree_id(tree_id)
    db = get_db()
    tree = db.get_tree(clean_id)
    if not tree:
        raise HTTPException(status_code=404, detail=f"Tree ID '{clean_id}' does not exist.")
    return tree


@app.get("/api/trees/{tree_id}/qr")
async def get_tree_qr_png(tree_id: str) -> Response:
    """Returns high-resolution PNG QR code for direct scanning or embedding."""
    clean_id = InputSanitizer.sanitize_tree_id(tree_id)
    png_bytes, _ = generate_tree_qr_code(tree_id=clean_id, base_url=PUBLIC_ONLINE_URL)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/trees/{tree_id}/tag")
async def get_printable_field_tag(tree_id: str) -> Response:
    """Renders all-weather printable laminated physical tag badge."""
    clean_id = InputSanitizer.sanitize_tree_id(tree_id)
    db = get_db()
    tree = db.get_tree(clean_id)
    if not tree:
        raise HTTPException(status_code=404, detail=f"Tree ID '{clean_id}' not found.")

    tag_bytes = generate_printable_tree_tag(
        tree_id=tree.tree_id,
        common_name=tree.common_name,
        scientific_name=tree.scientific_name,
        location_str=f"{tree.location.latitude:.5f}° N, {tree.location.longitude:.5f}° E",
        carbon_kg=tree.biometrics.carbon_sequestered_kg,
        base_url=PUBLIC_ONLINE_URL,
    )
    return Response(
        content=tag_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f"inline; filename={clean_id}_field_tag.png"},
    )


# ============================================================================
# 3. REST API: QR Code Decoding & Scanning
# ============================================================================


@app.post("/api/scan-qr")
async def scan_qr_tag(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Decodes a physical tree tag QR code from an uploaded field photo using OpenCV.
    Enforces payload size and magic byte verification.
    """
    content = await file.read()
    filename = Path(file.filename or "upload.jpg").name

    # Validate file integrity and size
    FileValidator.validate_file_payload(filename=filename, content=content, is_aerial=False)

    try:
        decoded_text = decode_qr_image(content)
        if not decoded_text:
            return {"status": "FAILED", "message": "No scannable QR code detected in image."}

        # Extract tree ID
        tree_id = decoded_text
        if "/tree/" in decoded_text:
            tree_id = decoded_text.split("/tree/")[-1].strip()

        clean_id = InputSanitizer.sanitize_tree_id(tree_id)
        db = get_db()
        tree = db.get_tree(clean_id)

        return {
            "status": "SUCCESS",
            "decoded_content": decoded_text,
            "tree_id": clean_id,
            "tree_exists": tree is not None,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("QR decode error: %s", exc)
        return {"status": "ERROR", "message": "Failed to decode QR code payload."}


# ============================================================================
# 4. REST API: Aerial Drone Computer Vision & Stocking
# ============================================================================


@app.post("/api/detect")
async def run_aerial_detection(
    file: Optional[UploadFile] = File(None),
    use_benchmark: Optional[bool] = Form(False),
) -> Dict[str, Any]:
    """
    Executes high-performance tree canopy detection on an aerial TIFF/JPG payload.
    Guarded by file validation and concurrency semaphore against CPU/RAM exhaustion.
    """
    detector = get_detector()
    img_array: Optional[np.ndarray] = None

    if use_benchmark or file is None:
        logger.info("Using simulated aerial forest benchmark...")
        img_array = generate_aerial_forest_sample(width=1024, height=1024, num_trees=40, seed=42)
    else:
        file_bytes = await file.read()
        filename = Path(file.filename or "uploaded.jpg").name

        # Enforce aerial payload size limits and magic byte check
        FileValidator.validate_file_payload(filename=filename, content=file_bytes, is_aerial=True)

        ext = Path(filename).suffix.lower()

        if ext in [".tif", ".tiff"]:
            try:
                with io.BytesIO(file_bytes) as bio:
                    arr = tifffile.imread(bio)
                    if arr.ndim == 2:
                        arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)
                    elif arr.ndim == 3 and arr.shape[2] >= 3:
                        arr = arr[:, :, :3]
                    if arr.dtype != np.uint8:
                        arr = cv2.normalize(arr, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                    img_array = arr
            except Exception as tiff_err:
                logger.warning("tifffile fallback triggered: %s", tiff_err)
                pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                img_array = np.array(pil_img)
        else:
            pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            img_array = np.array(pil_img)

    if img_array is None:
        raise HTTPException(status_code=400, detail="Failed to parse incoming aerial image payload.")

    # Guard ML inference with concurrency throttle
    async with INFERENCE_SEMAPHORE:
        det_res: DetectionResult = detector.detect(img_array)

    # Compute canopy analytics
    report = generate_canopy_stocking_report(
        boxes=det_res.boxes,
        image_width=det_res.image_width,
        image_height=det_res.image_height,
        inference_latency_ms=det_res.inference_time_ms,
    )

    # Render visual overlay
    overlay = render_canopy_overlay(
        image=img_array,
        boxes=det_res.boxes,
        draw_masks=True,
        draw_labels=True,
    )

    # Encode rendered JPEG as base64
    pil_overlay = Image.fromarray(overlay)
    buf = io.BytesIO()
    pil_overlay.save(buf, format="JPEG", quality=90)
    overlay_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return {
        "status": "SUCCESS",
        "total_crowns_detected": len(det_res.boxes),
        "canopy_density_pct": report.crown_footprint_density_pct,
        "rectangular_coverage_pct": report.canopy_coverage_density_pct,
        "inference_latency_ms": report.inference_latency_ms,
        "mean_crown_diameter_px": report.average_crown_diameter_px,
        "mean_confidence": report.mean_confidence,
        "anomalies_detected": report.anomalies_detected,
        "annotated_image_base64": overlay_b64,
        "boxes": [b.model_dump() for b in det_res.boxes],
    }


# ============================================================================
# 5. REST API: Telemetry, GeoJSON & CSV Export
# ============================================================================


@app.get("/api/metrics/summary")
async def metrics_summary() -> Dict[str, Any]:
    """Returns high-level carbon sequestration and stocking indicators."""
    db = get_db()
    return db.get_metrics_summary()


@app.get("/api/export/geojson")
async def export_geojson() -> JSONResponse:
    """Exports entire campus tree inventory as standard RFC 7946 GeoJSON."""
    db = get_db()
    return JSONResponse(
        content=db.to_geojson(),
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=ciet_campus_trees.geojson"},
    )


@app.get("/api/export/csv")
async def export_csv() -> PlainTextResponse:
    """Exports full tabular inventory with GPS coordinates and QR links as CSV."""
    db = get_db()
    return PlainTextResponse(
        content=db.to_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ciet_tree_inventory.csv"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
