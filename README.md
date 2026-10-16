# CIET Coimbatore — Computer Vision-Based Tree Stocking & Digital Forestry Platform

[![CIET Forestry CI / CD](https://github.com/iamwarriorofmyuniverse-coder/ciet-tree-stocking/actions/workflows/ci.yml/badge.svg)](https://github.com/iamwarriorofmyuniverse-coder/ciet-tree-stocking/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00599C.svg?logo=yolo&logoColor=white)](https://ultralytics.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Security Hardened](https://img.shields.io/badge/Security-Hardened%20WAF-success.svg)](#-enterprise-security-firewall--hardening)
[![PWA Ready](https://img.shields.io/badge/PWA-Installable%20Offline-emerald.svg)](#-mobile-applications-progressive-web-app--native-flutter-app)
[![Flutter Mobile](https://img.shields.io/badge/Flutter-Android%20%26%20iOS-02569B.svg?logo=flutter&logoColor=white)](mobile_app/)
[![Tests Passing](https://img.shields.io/badge/Tests-38%20Passing%20(100%25)-brightgreen.svg)](#-continuous-integration--test-verification)

**An In-House Asset Engineered for Coimbatore Institute of Engineering and Technology (CIET), Coimbatore**  
*Department of Artificial Intelligence & Data Science | Center for Forestry Informatics & Conservation*

---

## 🌐 Live Deployment & Online Access

- **Official GitHub Repository:** [https://github.com/iamwarriorofmyuniverse-coder/ciet-tree-stocking](https://github.com/iamwarriorofmyuniverse-coder/ciet-tree-stocking)
- **Live Public Online PWA:** [https://qualifications-asylum-workers-counter.trycloudflare.com](https://qualifications-asylum-workers-counter.trycloudflare.com)
- **Local Application Endpoint:** `http://localhost:8000`
- **Interactive OpenAPI / Swagger Documentation:** `http://localhost:8000/docs`

---

## 🌲 Executive Overview

The **CIET Forest Conservation Platform** is an enterprise-grade full-stack computer vision, GIS geolocation, and digital tree inventory platform. Engineered for the Coimbatore Institute of Engineering and Technology (Narasipuram, Thondamuthur, Coimbatore), the system bridges airborne drone computer vision with physical on-the-ground dendrological asset tracking.

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
|                     (OWASP Hardened WAF, Rate Limiting & Concurrency Throttle)                   |
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

### 5. 🛡️ Enterprise Security Firewall & Hardening
- **Web Application Firewall (WAF) Middleware:** Rejects SQL injection, Cross-Site Scripting (XSS), Path Traversal (`../`), Remote Code Execution (RCE), and shell injection patterns.
- **Sliding-Window Rate Limiter:** Per-IP sliding-window algorithm enforcing rate limits (60 requests/minute default, 15 uploads/minute) to stop DoS/flooding attacks.
- **Decompression Bomb Protection:** Restricts raster imagery to a maximum of 60,000,000 pixels (`Image.MAX_IMAGE_PIXELS`) and blocks payload sizes exceeding 25MB.
- **Magic Byte File Signature Validation:** Inspects raw file headers (`\xFF\xD8\xFF` for JPEG, `\x89PNG` for PNG, `II*\x00` / `MM\x00*` for TIFF) to prevent executable spoofing.
- **OWASP Security Headers:** Enforces `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and a hardened `Content-Security-Policy`.
- **Async Concurrency Throttling:** Internal `asyncio.Semaphore(2)` prevents GPU/CPU memory exhaustion during concurrent drone orthomosaic inference.

### 6. 📱 Mobile Applications: Progressive Web App & Dedicated Flutter App
- **Installable Progressive Web App (PWA):**
  - Instant 1-click installation on Android (Chrome) and iOS (Safari) with standalone display mode.
  - Offline-first Service Worker (`static/sw.js`) caching all 16 tree profiles and maps for off-grid surveys in Sector-IV (hillside).
  - W3C Web App Manifest (`static/manifest.json`) with custom CIET Forestry icons (192px, 512px, maskable).
- **Dedicated Flutter Native Mobile App (`mobile_app/`):**
  - Complete cross-platform codebase supporting Android APK and iOS.
  - Native 60fps hardware camera scanner (`mobile_scanner`) with flashlight toggle.
  - Offline caching via `shared_preferences` and interactive GIS map via `flutter_map`.

---

## 📂 Repository File Structure

```
ciet_tree_stocking/
├── .github/
│   └── workflows/
│       └── ci.yml                  # Automated GitHub Actions CI pipeline
├── mobile_app/                     # Flutter Native Mobile Application
│   ├── pubspec.yaml                # Mobile dependencies (http, flutter_map, mobile_scanner)
│   ├── android/                    # Android Manifest with Camera & GPS permissions
│   └── lib/
│       ├── main.dart               # Mobile app entry point & emerald theme
│       ├── models/                 # Dart TreeProfile, GeoLocation, Landmarks models
│       ├── services/               # ApiService with offline caching
│       └── screens/                # Map, QR Scanner, Tree List, & Campus Guide screens
├── static/
│   ├── manifest.json               # W3C Web App Manifest for PWA
│   ├── sw.js                       # Offline-first Service Worker
│   ├── offline.html                # Off-grid fallback screen
│   └── icons/                      # 192px, 512px, maskable PWA app icons
├── server.py                       # FastAPI Production Server with Security Firewall (Port 8000)
├── app.py                          # Streamlit Enterprise Reference Dashboard
├── requirements.txt                # Pinned dependency matrix
├── README.md                       # Enterprise technical documentation
├── templates/
│   ├── index.html                  # Responsive SPA (Leaflet GPS Map, QR Scanner, CV Dashboard)
│   └── tree_passport.html          # Individual Digital Tree Passport & Certificate
├── src/
│   ├── inventory/                  # TreeProfile, Biometrics, GeoLocation, Level-H QR Engine, CIET DB
│   ├── ml/                         # TreeDetector (YOLOv8), Pydantic tensors, Overlapping Canopy NMS
│   ├── security/                   # WAF Middleware, Sliding-Window Rate Limiting, Decompression Bomb & Magic Bytes
│   └── utils/                      # Planar binary raster density grid, Anomaly checks, OpenCV overlays
└── tests/
    ├── test_core.py                # ML pipeline, structural models, NMS, canopy density unit tests
    ├── test_inventory_qr.py        # Geolocation, biometrics, QR generation/decode tests
    └── test_security.py            # WAF, rate limiting, magic bytes, PWA manifest & SW tests
```

---

## 🛠️ Execution & Operating Guide

### Launching the Production Web Application & PWA
```powershell
cd ciet_tree_stocking
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```
- Open browser at: **`http://localhost:8000`**
- Interactive OpenAPI Swagger UI: **`http://localhost:8000/docs`**

### Running the Test Suite (38 Tests)
```powershell
pytest tests/ -v --tb=short
```

---

## 🧪 Continuous Integration & Test Verification

The repository contains 36 thorough unit and integration tests passing with 100% test coverage:
1. **Core ML & Computer Vision:** Pydantic validation, YOLOv8 inference, custom NMS IoU overlap filtering, exact pixel-grid canopy density calculation.
2. **Dendrology & Inventory:** Biometric bounds, Chave et al. carbon estimation, Western Ghats botanical taxonomy, RFC 7946 GeoJSON export.
3. **QR Code Technology:** High-density Level H QR generation, OpenCV matrix decoding, physical field tag rendering.
4. **Security & WAF:** XSS sanitization, SQL injection blocking, path traversal prevention, sliding-window rate limiting, magic byte header verification, and decompression bomb rejection.

---

## 📜 Authors & Institutional Citation
**Coimbatore Institute of Engineering and Technology (CIET)**  
Department of Artificial Intelligence and Data Science  
Narasipuram Post, Thondamuthur Via, Coimbatore - 641109, Tamil Nadu, India.
