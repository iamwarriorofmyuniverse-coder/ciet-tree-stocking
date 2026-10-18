"""
Unit & Integration Tests for Next-Level Innovation Modules:
- 4D Digital Twin Simulator
- Non-Destructive Acoustic Sonic Tomography & Wind Hazard Failure
- Autonomous Photogrammetry Drone Mission Planner & Multispectral Inversion
- Cryptographic ESG Carbon Credit Tokenizer & Verra VM0007 Ledger
- Western Ghats Biodiversity Symbiosis & FSQ Engine
"""

from __future__ import annotations

import pytest
from src.innovation.digital_twin import simulate_tree_growth
from src.innovation.sonic_tomography import compute_sonic_tomography
from src.innovation.drone_planner import (
    compute_drone_mission,
    generate_ardupilot_waypoints_text,
    generate_dji_kml_text,
    compute_synthetic_multispectral_indices,
)
from src.innovation.esg_ledger import (
    generate_carbon_ledger,
    generate_esg_certificate_for_tree,
    compute_sha256_hash,
)
from src.innovation.biodiversity import compute_campus_biodiversity


def test_digital_twin_forward_projection():
    """Verifies Chapman-Richards allometric growth simulation over a 15-year horizon."""
    sim = simulate_tree_growth(
        tree_id="CIET-TREE-001",
        scientific_name="Azadirachta indica",
        current_height=12.5,
        current_dbh=38.0,
        current_crown_spread=45.0,
        current_age=14,
        tree_lat=10.9992,
        tree_lon=76.9045,
        target_year=2040,
        base_year=2026,
    )
    assert sim.tree_id == "CIET-TREE-001"
    assert sim.years_simulated == 14
    assert len(sim.projections) >= 2
    # Check that growth is strictly non-decreasing
    assert sim.projections[-1].height_m >= sim.projections[0].height_m
    assert sim.projections[-1].dbh_cm >= sim.projections[0].dbh_cm
    assert sim.projections[-1].carbon_sequestered_kg >= sim.projections[0].carbon_sequestered_kg
    # Solar cooling metrics must be positive
    assert sim.solar_cooling.annual_cooling_energy_saved_kwh > 0
    assert len(sim.infrastructure_risks) > 0


def test_sonic_tomography_and_wind_failure():
    """Verifies acoustic velocity cross-section and Mattheck wind-throw calculations."""
    res = compute_sonic_tomography(
        tree_id="CIET-TREE-002",
        species_name="Ficus religiosa",
        dbh_cm=65.0,
        height_m=18.0,
        crown_spread_m2=95.0,
        health_status="Vigorous",
        test_wind_speed_kmh=75.0,
        grid_dim=16,
    )
    assert res.tree_id == "CIET-TREE-002"
    assert len(res.sensors) == 12
    assert len(res.grid) == 16
    assert len(res.grid[0]) == 16
    assert res.sound_wood_pct + res.incipient_decay_pct + res.cavity_pct == pytest.approx(100.0, abs=1.0)
    # Check Mattheck report
    report = res.hazard_report
    assert report.wind_speed_kmh == 75.0
    assert report.mattheck_t_r_ratio > 0.0
    assert report.structural_safety_factor > 0.0
    assert report.wind_threshold_failure_kmh > 0.0


def test_drone_mission_planner_and_exports():
    """Verifies autonomous flight grid generation and QGC/KML exports."""
    plan = compute_drone_mission(
        sector_id="Sector-A",
        altitude_m=50.0,
        front_overlap=80.0,
        side_overlap=75.0,
    )
    assert plan.sector_id == "Sector-A"
    assert plan.total_waypoints >= 4
    assert plan.gsd_cm_px > 0.0
    assert plan.estimated_photo_count > 0
    assert plan.battery_consumed_pct > 0.0

    # Test ArduPilot waypoints output
    wp_text = generate_ardupilot_waypoints_text(plan)
    assert "QGC WPL 110" in wp_text
    assert str(plan.altitude_m) in wp_text

    # Test DJI KML output
    kml_text = generate_dji_kml_text(plan)
    assert "<?xml version=" in kml_text
    assert "<coordinates>" in kml_text


def test_synthetic_multispectral_indices():
    """Verifies NDVI, NDRE, and CWSI calculation."""
    decomp = compute_synthetic_multispectral_indices(health_baseline=0.85)
    assert 0.0 <= decomp.mean_ndvi <= 1.0
    assert 0.0 <= decomp.mean_ndre <= 1.0
    assert 0.0 <= decomp.mean_cwsi <= 1.0
    assert decomp.chlorophyll_spad_equivalent > 0


def test_esg_carbon_ledger_cryptography():
    """Verifies SHA-256 tamper-evident chaining in carbon credit ledger."""
    sample_trees = [
        {
            "tree_id": "CIET-TREE-001",
            "scientific_name": "Azadirachta indica",
            "common_name": "Neem",
            "location": {"latitude": 10.9992, "longitude": 76.9045},
            "biometrics": {"carbon_sequestered_kg": 94.5},
        },
        {
            "tree_id": "CIET-TREE-002",
            "scientific_name": "Ficus religiosa",
            "common_name": "Peepal",
            "location": {"latitude": 10.9995, "longitude": 76.9048},
            "biometrics": {"carbon_sequestered_kg": 240.0},
        },
    ]
    ledger = generate_carbon_ledger(sample_trees)
    assert len(ledger) == 2
    # Verify Genesis block prev_hash is 64 zeros
    assert ledger[0].prev_hash == "0" * 64
    # Verify cryptographic block link
    assert ledger[1].prev_hash == ledger[0].block_hash
    assert len(ledger[0].block_hash) == 64

    # Test ESG certificate generation
    cert = generate_esg_certificate_for_tree(sample_trees[0])
    assert cert.certificate_id.startswith("CIET-ESG-2026-")
    assert len(cert.verification_hash) == 64
    assert cert.vcu_equivalent_tonnes > 0


def test_campus_biodiversity_matrix():
    """Verifies Shannon-Wiener diversity index and faunal support quotient."""
    sample_trees = [
        {"tree_id": "CIET-TREE-001", "scientific_name": "Azadirachta indica"},
        {"tree_id": "CIET-TREE-002", "scientific_name": "Ficus religiosa"},
        {"tree_id": "CIET-TREE-003", "scientific_name": "Pongamia pinnata"},
    ]
    summary = compute_campus_biodiversity(sample_trees)
    assert summary.total_trees == 3
    assert summary.total_distinct_species == 3
    assert summary.shannon_wiener_index_h > 0.0
    assert summary.campus_faunal_support_quotient_fsq > 70.0
    assert len(summary.profiles) == 3
