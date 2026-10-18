"""
Autonomous Photogrammetry Drone Mission Planner & Synthetic Multispectral Inversion.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).

Capabilities:
- Sub-centimeter GSD photogrammetric lawnmower flight path generator.
- Mission duration, battery consumption, and photo count estimation.
- Export to genuine ArduPilot / Pixhawk (.waypoints) and DJI Pilot / Google Earth (.kml).
- Synthetic multispectral vegetation health decomposition (NDVI, NDRE, CWSI).
"""

from __future__ import annotations

import io
import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from pydantic import BaseModel, Field

# Defined Campus Sectors for CIET Autonomous Aerial Surveys
CIET_SECTOR_BOUNDS = {
    "Sector-A": {
        "name": "Academic & Research Quadrant",
        "center_lat": 10.9956, "center_lon": 76.7733,
        "lat_min": 10.9950, "lat_max": 10.9962,
        "lon_min": 76.7728, "lon_max": 76.7739,
        "area_m2": 21500.0,
    },
    "Sector-B": {
        "name": "Western Boundary & Botanical Reserve",
        "center_lat": 10.9960, "center_lon": 76.7726,
        "lat_min": 10.9952, "lat_max": 10.9968,
        "lon_min": 76.7720, "lon_max": 76.7730,
        "area_m2": 24800.0,
    },
    "Sector-C": {
        "name": "Sports Arena & Agro-Forestry Eco-Park",
        "center_lat": 10.9948, "center_lon": 76.7740,
        "lat_min": 10.9942, "lat_max": 10.9954,
        "lon_min": 76.7732, "lon_max": 76.7748,
        "area_m2": 26500.0,
    },
}


class DroneWaypoint(BaseModel):
    """3D Autonomous Waypoint for drone telemetry."""
    index: int
    lat: float
    lon: float
    alt_m: float
    action: str  # TAKEOFF, SURVEY_LEG, TURN, RTL
    speed_mps: float = 5.0


class PhotogrammetryPlan(BaseModel):
    """Complete flight plan metadata and photogrammetric parameters."""
    sector_id: str
    sector_name: str
    altitude_m: float
    gsd_cm_px: float
    front_overlap_pct: float
    side_overlap_pct: float
    flight_speed_mps: float
    total_waypoints: int
    flight_distance_m: float
    estimated_duration_min: float
    estimated_photo_count: int
    battery_consumed_pct: float
    waypoints: List[DroneWaypoint]
    kml_available: bool = True
    waypoints_file_available: bool = True


class MultispectralDecomposition(BaseModel):
    """Synthetic vegetation index analytics decomposed from aerial sensors."""
    mean_ndvi: float = Field(..., description="Normalized Difference Vegetation Index (0.0 to 1.0)")
    mean_ndre: float = Field(..., description="Red Edge Chlorophyll Saturation Index")
    mean_cwsi: float = Field(..., description="Canopy Water Stress Index (0.0 = Hydrated, 1.0 = Severe Stress)")
    vegetation_vigor_category: str
    chlorophyll_spad_equivalent: float
    water_stress_status: str
    prescription: str


def compute_drone_mission(
    sector_id: str = "Sector-A",
    altitude_m: float = 45.0,
    front_overlap: float = 80.0,
    side_overlap: float = 75.0,
    flight_speed_mps: float = 5.0,
) -> PhotogrammetryPlan:
    """
    Generates a flight plan with lawnmower grid waypoints for the chosen campus sector.
    """
    sector = CIET_SECTOR_BOUNDS.get(sector_id, CIET_SECTOR_BOUNDS["Sector-A"])

    # Sensor Optics: 1/2.3" to 4/3" sensor (focal length 8.8mm, sensor width 13.2mm, 5472 px)
    focal_length_mm = 8.8
    sensor_width_mm = 13.2
    image_width_px = 5472.0

    # GSD (cm/pixel) = (Altitude_m * 100 * sensor_width_mm) / (focal_length_mm * image_width_px)
    gsd_cm = (altitude_m * 100.0 * sensor_width_mm) / (focal_length_mm * image_width_px)

    # Ground Footprint:
    ground_w_m = (image_width_px * gsd_cm) / 100.0
    ground_h_m = (3648.0 * gsd_cm) / 100.0

    # Line Spacing (Sidelap):
    line_spacing_m = ground_w_m * (1.0 - (side_overlap / 100.0))
    photo_interval_m = ground_h_m * (1.0 - (front_overlap / 100.0))

    # Convert line spacing to latitude degrees (~111,000 meters per degree lat)
    m_per_deg_lat = 111132.0
    m_per_deg_lon = 111132.0 * math.cos(math.radians(sector["center_lat"]))

    lat_step = line_spacing_m / m_per_deg_lat

    waypoints: List[DroneWaypoint] = []
    # Waypoint 0: Home / Takeoff
    home_lat = sector["center_lat"] - 0.0003
    home_lon = sector["center_lon"] - 0.0003
    waypoints.append(
        DroneWaypoint(index=0, lat=round(home_lat, 6), lon=round(home_lon, 6), alt_m=altitude_m, action="TAKEOFF")
    )

    curr_lat = sector["lat_min"]
    sweep_idx = 0
    total_dist_m = 35.0  # Takeoff climb distance

    prev_lat = home_lat
    prev_lon = home_lon

    while curr_lat <= sector["lat_max"]:
        sweep_idx += 1
        if sweep_idx % 2 == 1:
            # West to East
            p1_lon = sector["lon_min"]
            p2_lon = sector["lon_max"]
        else:
            # East to West
            p1_lon = sector["lon_max"]
            p2_lon = sector["lon_min"]

        # Add start of flight leg
        leg_start = DroneWaypoint(
            index=len(waypoints),
            lat=round(curr_lat, 6),
            lon=round(p1_lon, 6),
            alt_m=altitude_m,
            action="SURVEY_LEG",
        )
        waypoints.append(leg_start)

        # Distance calculation
        d1 = math.hypot((curr_lat - prev_lat) * m_per_deg_lat, (p1_lon - prev_lon) * m_per_deg_lon)
        total_dist_m += d1

        # Add end of flight leg
        leg_end = DroneWaypoint(
            index=len(waypoints),
            lat=round(curr_lat, 6),
            lon=round(p2_lon, 6),
            alt_m=altitude_m,
            action="SURVEY_LEG",
        )
        waypoints.append(leg_end)

        d2 = math.hypot(0.0, (p2_lon - p1_lon) * m_per_deg_lon)
        total_dist_m += d2

        prev_lat = curr_lat
        prev_lon = p2_lon

        curr_lat += lat_step

    # Return To Launch Waypoint
    waypoints.append(
        DroneWaypoint(index=len(waypoints), lat=round(home_lat, 6), lon=round(home_lon, 6), alt_m=0.0, action="RTL")
    )
    total_dist_m += math.hypot((home_lat - prev_lat) * m_per_deg_lat, (home_lon - prev_lon) * m_per_deg_lon)

    duration_sec = total_dist_m / flight_speed_mps
    duration_min = duration_sec / 60.0

    photo_count = max(12, int(total_dist_m / max(5.0, photo_interval_m)))

    # Drone battery drain model (standard 5000mAh 4S LiPo: ~4.5% per minute of flight)
    battery_pct = min(95.0, round(duration_min * 4.6 + 8.0, 1))

    return PhotogrammetryPlan(
        sector_id=sector_id,
        sector_name=sector["name"],
        altitude_m=altitude_m,
        gsd_cm_px=round(gsd_cm, 2),
        front_overlap_pct=front_overlap,
        side_overlap_pct=side_overlap,
        flight_speed_mps=flight_speed_mps,
        total_waypoints=len(waypoints),
        flight_distance_m=round(total_dist_m, 1),
        estimated_duration_min=round(duration_min, 1),
        estimated_photo_count=photo_count,
        battery_consumed_pct=battery_pct,
        waypoints=waypoints,
    )


def generate_ardupilot_waypoints_text(plan: PhotogrammetryPlan) -> str:
    """
    Renders ArduPilot / Pixhawk standard QGC WPL 110 mission file text.
    Can be imported directly into QGroundControl or Mission Planner.
    """
    lines = ["QGC WPL 110"]
    for wp in plan.waypoints:
        # Standard format: <INDEX> <CURRENT_WP> <COORD_FRAME> <COMMAND> <PARAM1> <PARAM2> <PARAM3> <PARAM4> <LAT> <LON> <ALT> <AUTOCONTINUE>
        # Command 16 = MAV_CMD_NAV_WAYPOINT, Command 22 = MAV_CMD_NAV_TAKEOFF, Command 20 = MAV_CMD_NAV_RETURN_TO_LAUNCH
        cmd = 16
        if wp.action == "TAKEOFF":
            cmd = 22
        elif wp.action == "RTL":
            cmd = 20

        is_current = 1 if wp.index == 0 else 0
        line = f"{wp.index}\t{is_current}\t3\t{cmd}\t0.000000\t0.000000\t0.000000\t0.000000\t{wp.lat:.6f}\t{wp.lon:.6f}\t{wp.alt_m:.2f}\t1"
        lines.append(line)
    return "\n".join(lines)


def generate_dji_kml_text(plan: PhotogrammetryPlan) -> str:
    """
    Renders standard KML file compatible with DJI Pilot, Google Earth, and GIS viewers.
    """
    coords_str = " ".join([f"{wp.lon},{wp.lat},{wp.alt_m}" for wp in plan.waypoints])
    kml = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>CIET Drone Mission: {plan.sector_name}</name>
    <description>Autonomous Photogrammetric Survey Grid (Altitude: {plan.altitude_m}m, GSD: {plan.gsd_cm_px}cm/px)</description>
    <Style id="flightPathStyle">
      <LineStyle>
        <color>ff10b981</color>
        <width>3</width>
      </LineStyle>
    </Style>
    <Placemark>
      <name>Survey Grid Trajectory</name>
      <styleUrl>#flightPathStyle</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>"""
    return kml


def compute_synthetic_multispectral_indices(health_baseline: float = 0.82) -> MultispectralDecomposition:
    """
    Evaluates synthetic multi-band vegetation indices (NDVI, NDRE, CWSI).
    """
    ndvi = round(min(0.95, max(0.20, health_baseline + 0.04)), 3)
    ndre = round(min(0.85, max(0.15, ndvi * 0.88)), 3)
    # CWSI is inverse: lower water stress means high hydration
    cwsi = round(max(0.05, min(0.90, 1.0 - (ndvi * 1.05))), 3)

    spad = round(ndvi * 52.0 + 4.5, 1)

    if ndvi >= 0.75:
        vigor = "Vigorous / High Biomass Canopy"
    elif ndvi >= 0.55:
        vigor = "Healthy / Moderate Foliage Density"
    else:
        vigor = "Stressed / Defoliated Canopy"

    if cwsi <= 0.25:
        stress_status = "Optimal Soil & Foliar Hydration"
        prescription = "No irrigation intervention required. Sub-canopy moisture retention is optimal."
    elif cwsi <= 0.45:
        stress_status = "Mild Evapotranspirative Deficit"
        prescription = "Schedule drip irrigation pulse (25L/tree) during early morning non-evaporative window."
    else:
        stress_status = "Severe Cellular Water Stress Detected"
        prescription = "URGENT: Deep root irrigation and soil compaction relief required in Sector root zone."

    return MultispectralDecomposition(
        mean_ndvi=ndvi,
        mean_ndre=ndre,
        mean_cwsi=cwsi,
        vegetation_vigor_category=vigor,
        chlorophyll_spad_equivalent=spad,
        water_stress_status=stress_status,
        prescription=prescription,
    )
