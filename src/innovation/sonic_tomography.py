"""
Non-Destructive Acoustic Sonic Tomography & Wind Load Failure Physics Engine.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).

Scientific Foundations:
- Stress-wave velocity impulse propagation across trunk radial cross-sections.
- Claus Mattheck's Visual Tree Assessment (VTA) and biological safety rule (t/R > 0.30).
- Aerodynamic wind moment overturning stress during monsoon squalls.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class TomographySensor(BaseModel):
    """Virtual sonic sensor placed on the trunk circumference."""
    sensor_id: int
    angle_deg: float
    x: float
    y: float
    frequency_khz: float = 78.5


class TomographyCell(BaseModel):
    """Grid pixel in the internal trunk sonic tomogram."""
    x_idx: int
    y_idx: int
    rel_x: float
    rel_y: float
    velocity_mps: float
    tissue_state: str  # SOUND_WOOD, INCIPIENT_DECAY, CAVITY_DECAY, BARK_EXTERIOR
    color_hex: str


class MattheckHazardReport(BaseModel):
    """Wind-load failure and structural stem breakage engineering assessment."""
    wind_speed_kmh: float
    wind_speed_mps: float
    aerodynamic_drag_force_n: float
    overturning_bending_moment_nm: float
    bending_stress_mpa: float
    wood_failure_strength_mpa: float
    residual_wall_thickness_t_cm: float
    trunk_radius_r_cm: float
    mattheck_t_r_ratio: float
    structural_safety_factor: float
    risk_category: str  # NEGLIGIBLE, ELEVATED, CRITICAL_FAILURE
    wind_threshold_failure_kmh: float
    remedial_prescription: str


class SonicTomographyResult(BaseModel):
    """Complete Non-Destructive Acoustic Tomography & Structural Integrity Report."""
    tree_id: str
    species_name: str
    dbh_cm: float
    height_m: float
    grid_resolution: int
    sound_wood_pct: float
    incipient_decay_pct: float
    cavity_pct: float
    sensors: List[TomographySensor]
    grid: List[List[TomographyCell]]
    hazard_report: MattheckHazardReport


def compute_sonic_tomography(
    tree_id: str,
    species_name: str,
    dbh_cm: float,
    height_m: float,
    crown_spread_m2: float,
    health_status: str = "Vigorous",
    test_wind_speed_kmh: float = 65.0,
    grid_dim: int = 16,
) -> SonicTomographyResult:
    """
    Computes an acoustic sonic velocity cross-section and Mattheck wind-failure analysis.
    """
    radius_cm = dbh_cm / 2.0
    r_m = radius_cm / 100.0

    # Determine simulated cavity radius based on tree health rating
    if "Distressed" in health_status or "Pruning" in health_status:
        cavity_ratio = 0.52  # Significant internal heartwood fungal decay
        sound_v_base = 1350.0
    elif "Healthy" in health_status:
        cavity_ratio = 0.18  # Minor natural aging core
        sound_v_base = 1550.0
    else:  # Vigorous
        cavity_ratio = 0.08  # Solid intact heartwood
        sound_v_base = 1680.0

    # 1. Generate Virtual 12-Sensor Circumference Array
    num_sensors = 12
    sensors: List[TomographySensor] = []
    for i in range(num_sensors):
        angle = (360.0 / num_sensors) * i
        rad = math.radians(angle)
        sx = round(math.cos(rad) * radius_cm, 2)
        sy = round(math.sin(rad) * radius_cm, 2)
        sensors.append(TomographySensor(sensor_id=i + 1, angle_deg=round(angle, 1), x=sx, y=sy))

    # 2. Synthesize 2D Internal Cross-Section Velocity Field
    grid: List[List[TomographyCell]] = []
    sound_count = 0
    decay_count = 0
    cavity_count = 0
    total_wood_cells = 0

    cavity_center_x = 0.15 * (radius_cm if "Pruning" in health_status else 0.0)
    cavity_center_y = -0.10 * (radius_cm if "Pruning" in health_status else 0.0)

    for yi in range(grid_dim):
        row: List[TomographyCell] = []
        rel_y = (1.0 - (2.0 * yi / (grid_dim - 1))) * radius_cm
        for xi in range(grid_dim):
            rel_x = ((2.0 * xi / (grid_dim - 1)) - 1.0) * radius_cm
            dist_to_center = math.sqrt(rel_x ** 2 + rel_y ** 2)

            if dist_to_center > radius_cm:
                # Outside trunk bark boundary
                row.append(
                    TomographyCell(
                        x_idx=xi,
                        y_idx=yi,
                        rel_x=round(rel_x, 2),
                        rel_y=round(rel_y, 2),
                        velocity_mps=0.0,
                        tissue_state="BARK_EXTERIOR",
                        color_hex="#070a10",
                    )
                )
            else:
                total_wood_cells += 1
                # Distance to simulated fungal rot pocket
                dist_to_cavity = math.sqrt((rel_x - cavity_center_x) ** 2 + (rel_y - cavity_center_y) ** 2)
                cavity_threshold = radius_cm * cavity_ratio

                if dist_to_cavity < cavity_threshold:
                    # Decay / hollow cavity (< 1000 m/s)
                    v = 650.0 + (dist_to_cavity / max(0.1, cavity_threshold)) * 300.0
                    state = "CAVITY_DECAY"
                    color = "#ef4444"  # Red
                    cavity_count += 1
                elif dist_to_cavity < cavity_threshold * 1.5:
                    # Incipient fungal decay / microcracks (1000 - 1350 m/s)
                    v = 1000.0 + ((dist_to_cavity - cavity_threshold) / max(0.1, cavity_threshold * 0.5)) * 350.0
                    state = "INCIPIENT_DECAY"
                    color = "#f59e0b"  # Amber
                    decay_count += 1
                else:
                    # Solid sound lignified wood (1400 - 1800 m/s)
                    v = sound_v_base - (dist_to_center / radius_cm) * 120.0
                    state = "SOUND_WOOD"
                    color = "#10b981"  # Emerald
                    sound_count += 1

                row.append(
                    TomographyCell(
                        x_idx=xi,
                        y_idx=yi,
                        rel_x=round(rel_x, 2),
                        rel_y=round(rel_y, 2),
                        velocity_mps=round(v, 1),
                        tissue_state=state,
                        color_hex=color,
                    )
                )
        grid.append(row)

    wood_total = max(1, total_wood_cells)
    sound_pct = round((sound_count / wood_total) * 100.0, 1)
    incipient_pct = round((decay_count / wood_total) * 100.0, 1)
    cavity_pct = round((cavity_count / wood_total) * 100.0, 1)

    # 3. Mattheck VTA Mechanical Wind-Failure Analysis
    v_mps = test_wind_speed_kmh / 3.6
    rho_air = 1.225  # kg/m^3 air density at 430m CIET elevation
    cd = 0.35  # aerodynamic crown drag coefficient
    # Frontal projected crown area: elliptical projection from spread
    crown_radius_m = math.sqrt(crown_spread_m2 / math.pi)
    crown_frontal_area = 2.0 * crown_radius_m * (height_m * 0.55)

    # Aerodynamic Drag Force: F = 0.5 * rho * Cd * A * v^2
    drag_force = 0.5 * rho_air * cd * crown_frontal_area * (v_mps ** 2)

    # Overturning Bending Moment: M = F * h_cop (center of wind pressure ~ 60% tree height)
    h_cop = height_m * 0.60
    bending_moment = drag_force * h_cop

    # Mattheck t/R ratio: t = residual wall thickness
    residual_wall_t_cm = max(1.0, radius_cm * (1.0 - cavity_ratio))
    t_r_ratio = residual_wall_t_cm / radius_cm

    # Section Modulus Z for hollow cylinder: Z = (pi / (4 * R)) * (R^4 - R_in^4)
    r_in_m = (radius_cm * cavity_ratio) / 100.0
    z_modulus = (math.pi / (4.0 * r_m)) * (max(0.0001, (r_m ** 4) - (r_in_m ** 4)))

    # Maximum Bending Stress: sigma = M / Z (Pascals -> MPa)
    stress_pa = bending_moment / z_modulus
    stress_mpa = stress_pa / 1_000_000.0

    # Wood species modulus of rupture (MOR in green condition ~ 50 - 75 MPa for tropical hardwoods)
    wood_mor_mpa = 62.0
    safety_factor = wood_mor_mpa / max(0.1, stress_mpa)

    # Wind speed causing structural failure (safety_factor = 1.0)
    # Since stress is proportional to v^2: v_fail = v_current * sqrt(safety_factor)
    v_fail_mps = v_mps * math.sqrt(max(0.01, safety_factor))
    v_fail_kmh = v_fail_mps * 3.6

    if t_r_ratio < 0.28 or safety_factor < 1.2:
        risk_cat = "CRITICAL_FAILURE"
        action = (
            "EMERGENCY: Immediate crown reduction and hazard zone cordon required. High risk of wind-throw collapse."
        )
    elif t_r_ratio < 0.38 or safety_factor < 2.0:
        risk_cat = "ELEVATED"
        action = (
            "Perform selective end-weight branch thinning and install dynamic cable bracing before monsoon."
        )
    else:
        risk_cat = "NEGLIGIBLE"
        action = "Tree meets Claus Mattheck structural biomechanical threshold (t/R > 0.35). No hazard."

    hazard_report = MattheckHazardReport(
        wind_speed_kmh=round(test_wind_speed_kmh, 1),
        wind_speed_mps=round(v_mps, 2),
        aerodynamic_drag_force_n=round(drag_force, 1),
        overturning_bending_moment_nm=round(bending_moment, 1),
        bending_stress_mpa=round(stress_mpa, 2),
        wood_failure_strength_mpa=wood_mor_mpa,
        residual_wall_thickness_t_cm=round(residual_wall_t_cm, 1),
        trunk_radius_r_cm=round(radius_cm, 1),
        mattheck_t_r_ratio=round(t_r_ratio, 3),
        structural_safety_factor=round(safety_factor, 2),
        risk_category=risk_cat,
        wind_threshold_failure_kmh=round(v_fail_kmh, 1),
        remedial_prescription=action,
    )

    return SonicTomographyResult(
        tree_id=tree_id,
        species_name=species_name,
        dbh_cm=dbh_cm,
        height_m=height_m,
        grid_resolution=grid_dim,
        sound_wood_pct=sound_pct,
        incipient_decay_pct=incipient_pct,
        cavity_pct=cavity_pct,
        sensors=sensors,
        grid=grid,
        hazard_report=hazard_report,
    )
