# CIET Forestry & Tree Stocking — Flutter Mobile App

**Enterprise In-Field Ranger & Drone Geolocation Android & iOS Application**  
*Engineered for Coimbatore Institute of Engineering and Technology (CIET), Coimbatore*  
*Department of Artificial Intelligence & Data Science*

---

## 📱 Mobile Architecture & Capabilities

The **CIET Trees Mobile Application** is designed for on-the-ground dendrologists, student researchers, and field foresters walking the campus grounds (Narasipuram, Thondamuthur):

1. **Hardware-Accelerated QR Tag Scanner:**
   - Powered by `mobile_scanner` with native 60fps camera feed.
   - Built-in torch/flashlight toggle for shaded canopies and dusk surveys.
   - Instantly decodes tree bark tags and opens the digital tree passport.

2. **Offline-First Resilience:**
   - Automatically caches tree profiles, biometric calculations, and sector metadata in local device memory (`SharedPreferences`).
   - Field foresters can navigate and scan in deep Western Ghats hillside zones (Sector-IV) where cellular signal is intermittent.

3. **High-Precision GIS Satellite Map:**
   - Integrated with `flutter_map` (OpenStreetMap / Satellite tiles).
   - Centered on CIET Campus (`10.995556° N, 76.773333° E`).
   - Color-coded crown spread pins and 12 campus facility markers.

4. **Chave Pan-Tropical Carbon Accounting:**
   - Real-time display of total lifetime $CO_2$ sequestration and equivalent passenger car kilometers offset.

---

## 🏗️ Codebase Structure

```
mobile_app/
├── pubspec.yaml                  # Flutter dependencies (http, flutter_map, mobile_scanner)
├── android/
│   └── app/src/main/
│       └── AndroidManifest.xml   # Camera, GPS & network permissions
└── lib/
    ├── main.dart                 # App entry point & emerald theme configuration
    ├── models/
    │   ├── tree_model.dart       # TreeProfile, GeoLocation, Biometrics models
    │   └── campus_landmark.dart  # 12 CIET Campus landmarks & facilities
    ├── services/
    │   └── api_service.dart      # HTTP client with offline caching strategy
    └── screens/
        ├── home_navigation_screen.dart # Bottom navigation bar controller
        ├── campus_map_screen.dart      # Interactive GPS satellite campus map
        ├── qr_scanner_screen.dart      # Hardware camera QR barcode scanner
        ├── tree_list_screen.dart       # Searchable tree inventory directory
        ├── tree_detail_screen.dart     # Digital passport & carbon gauge
        └── campus_directory_screen.dart # Inside CIET Campus directory
```

---

## 🚀 Execution & Build Instructions

### Prerequisites
- Flutter SDK 3.0+
- Android Studio / Android SDK (API Level 34)

### 1. Install Dependencies
```bash
cd mobile_app
flutter pub get
```

### 2. Run on Connected Phone or Emulator
```bash
flutter run
```

### 3. Build Production Android APK
```bash
flutter build apk --release
```
The compiled APK will be located at:
`mobile_app/build/app/outputs/flutter-apk/app-release.apk`
