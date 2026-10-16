# CIET Coimbatore — Computer Vision-Based Tree Stocking & Digital Forestry Platform

**An In-House Asset Engineered for Coimbatore Institute of Engineering and Technology (CIET), Coimbatore**  
*Department of Artificial Intelligence & Data Science | Center for Forestry Informatics & Conservation*

---

## 🌲 Executive Overview

The **CIET Forest Conservation Platform** is an enterprise-grade full-stack computer vision, GIS geolocation, and digital tree inventory platform. Engineered for Coimbatore Institute of Engineering and Technology (Narasipuram, Thondamuthur, Coimbatore), the system bridges airborne drone computer vision with physical on-the-ground dendrological asset tracking.

```
+--------------------------------------------------------------------------------------------------+
|                                    CIET AIRBORNE & GROUND PIPELINE                                |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   [ Overhead Drone Ortho-Mosaics ]       [ Field Foresters / Rangers (Smartphones) ]             |
|                  |                                                 |                             |
|                  v                                                 v                             |
|      (YOLOv8 Tree Crown Engine)                      (Live HTML5/Camera QR Tag Scanner)          |
|                  |                                                 |                             |
|                  v                                                 v                             |
|      (Spatial NMS Overlap Filter)                    (OpenCV cv2.QRCodeDetector Engine)          |
|                  |                                                 |                             |
|                  v                                                 v                             |
|      (Planar Raster Occupancy Grid)                  [ Direct Digital Tree Passport ]            |
|                  |                                                 |                             |
|                  +------------------------+------------------------+                             |
|                                           |                                                      |
|                                           v                                                      |
|                   [ FastAPI Enterprise REST & Web Engine (Port 8000) ]                           |
|                                           |                                                      |
|         +---------------------------------+--------------------------------+                    |
|         |                                 |                                |                    |
|         v                                 v                                v                    |
|  [ Leaflet GPS Satellite Map ]   [ Chave Carbon Accounting ]   [ RFC 7946 GeoJSON / CSV Export ] |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

---

## 🚀 Key Architectural Capabilities

### 1. Complete Dendrological Profiles & Carbon Accounting
- Complete biological data models ([`src/inventory/models.py`](file:///C:/Users/shine.DESKTOP-HU962IE/.gemini/antigravity/scratch/ciet_tree_stocking/src/inventory/models.py)):
  - **Botanical Taxonomy:** Common Name, Scientific Binomial Nomenclature, Family, IUCN Conservation Status, Native Region, Ethnobotanical/Medicinal Significance.
  - **Dendrological Biometrics:** Diameter at Breast Height (DBH in cm), Total Tree Height (m), Planar Canopy Spread ($m^2$), Estimated Age (Years), Health Status, Foliage State.
  - **Carbon Sequestration:** Automated Chave et al. pan-tropical allometric equation estimating total lifetime biomass $CO_2$ sequestration in kg and metric tonnes.

### 2. High-Precision GPS Geolocation & Interactive Satellite Map
- Anchored to the **CIET Coimbatore Campus** (10.9992° N, 76.9045° E, Narasipuram, Thondamuthur).
- Monitored plots across four institutional sectors:
  - *Sector-I: Academic Quadrant & Herbal Garden*
  - *Sector-II: Botanical Reserve & Arboretum*
  - *Sector-III: Sports Complex Buffer*
  - *Sector-IV: Western Ghats Eco-Corridor & Hillside Reserve*
- Interactive **Leaflet.js** map with satellite and street layers, sector filtering, and color-coded status pins.
- Direct **Google Maps navigation links** for instant mobile field navigation.

### 3. QR Code Technology: In-Field Tagging & Instant Scanning
- **High-Density QR Code Generator:** Embeds digital passport URLs (`/tree/{tree_id}`) with Level H error correction.
- **Physical Field Tags:** Programmatically renders printable, weather-resistant field tags with the CIET emblem, species name, GPS coordinates, and QR matrix.
- **Dual Scanner Engine:**
  - In-browser live camera scanner utilizing `html5-qrcode` for field rangers using smartphones.
  - Server-side image decoding endpoint (`/api/scan-qr`) utilizing OpenCV `cv2.QRCodeDetector`.

### 4. Aerial Drone Computer Vision Inference Engine
- Built with **YOLOv8** and strict Pydantic parsing ([`src/ml/engine.py`](file:///C:/Users/shine.DESKTOP-HU962IE/.gemini/antigravity/scratch/ciet_tree_stocking/src/ml/engine.py)).
- Targets fine-tuned institutional weights (`models/ciet_tree_stock_yolov8.pt`) with zero-downtime programmatic fallback to official `yolov8n.pt`.
- Vectorized Non-Maximum Suppression (`non_maximum_suppression`) eliminates duplicate counts in dense tree clumps.
- **Binary Occupancy Grid Analytics** calculates exact canopy coverage density (%) without over-counting.

---

## 📂 Repository File Structure

```
ciet_tree_stocking/
├── server.py                       # FastAPI Production Server (Port 8000)
├── requirements.txt                # Pinned dependency matrix
├── README.md                       # Enterprise technical documentation
├── templates/
│   ├── index.html                  # Responsive SPA (Leaflet GPS Map, QR Scanner, CV Dashboard)
│   └── tree_passport.html          # Individual Digital Tree Passport & Certificate
├── src/
│   ├── inventory/
│   │   ├── __init__.py             # Inventory module exports
│   │   ├── models.py               # TreeProfile, GeoLocation, BiometricTelemetry
│   │   ├── qr_engine.py            # QR code generation, OpenCV decode, printable field tag
│   │   └── database.py             # In-memory database, CIET seed data, GeoJSON/CSV export
│   ├── ml/
│   │   ├── __init__.py             # ML module exports
│   │   └── engine.py               # TreeDetector, BoundingBox, DetectionResult, NMS
│   └── utils/
│       ├── __init__.py             # Utils exports
│       ├── analytics.py            # Exact canopy density, anomaly scanner, telemetry logger
│       ├── sample_generator.py     # Synthetic aerial forest ortho-mosaic generator
│       └── visualization.py        # Custom-colored crown overlays, masks, badges
└── tests/
    ├── __init__.py                 # Test module init
    ├── test_core.py                # ML pipeline, models, NMS, canopy density unit tests
    └── test_inventory_qr.py        # Geolocation, biometrics, QR generation/decode tests
```

---

## 🛠️ Execution & Operating Guide

### Launching the Production Web Application
```powershell
cd C:\Users\shine.DESKTOP-HU962IE\.gemini\antigravity\scratch\ciet_tree_stocking
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```
- Open browser at: **`http://localhost:8000`**
- Interactive OpenAPI Swagger UI: **`http://localhost:8000/docs`**

### Running the Test Suite (24 Tests)
```powershell
pytest tests/ -v --tb=short
```

---

## 📜 Authors & Institutional Citation
**Coimbatore Institute of Engineering and Technology (CIET)**  
Department of Artificial Intelligence and Data Science  
Narasipuram Post, Thondamuthur Via, Coimbatore - 641109, Tamil Nadu, India.
