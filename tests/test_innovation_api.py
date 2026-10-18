"""
Integration HTTP endpoint tests for the Innovation API routes.
"""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient
from server import app

client = TestClient(app)


def test_api_digital_twin_endpoint():
    resp = client.get("/api/innovation/digital-twin/CIET-TREE-001?target_year=2038")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tree_id"] == "CIET-TREE-001"
    assert data["target_year"] == 2038
    assert "projections" in data
    assert len(data["projections"]) > 0
    assert "infrastructure_risks" in data
    assert "solar_cooling" in data


def test_api_sonic_tomography_endpoint():
    resp = client.get("/api/innovation/tomography/CIET-TREE-001?wind_speed_kmh=80.0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tree_id"] == "CIET-TREE-001"
    assert "grid" in data
    assert len(data["grid"]) == 16
    assert "hazard_report" in data
    assert data["hazard_report"]["wind_speed_kmh"] == 80.0


def test_api_drone_plan_endpoint():
    resp = client.get("/api/innovation/drone-plan?sector_id=Sector-A&altitude_m=50.0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sector_id"] == "Sector-A"
    assert "waypoints" in data
    assert len(data["waypoints"]) > 0


def test_api_drone_export_endpoints():
    resp_wp = client.get("/api/innovation/drone-export/waypoints?sector_id=Sector-A")
    assert resp_wp.status_code == 200
    assert "QGC WPL 110" in resp_wp.text

    resp_kml = client.get("/api/innovation/drone-export/kml?sector_id=Sector-A")
    assert resp_kml.status_code == 200
    assert "<?xml" in resp_kml.text


def test_api_multispectral_endpoint():
    resp = client.get("/api/innovation/multispectral?health_baseline=0.88")
    assert resp.status_code == 200
    data = resp.json()
    assert "mean_ndvi" in data
    assert "mean_cwsi" in data
    assert "chlorophyll_spad_equivalent" in data


def test_api_esg_ledger_endpoint():
    resp = client.get("/api/innovation/esg-ledger")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "block_hash" in data[0]
    assert "serial_number" in data[0]


def test_api_esg_certificate_endpoint():
    resp = client.get("/api/innovation/esg-certificate/CIET-TREE-001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tree_id"] == "CIET-TREE-001"
    assert "certificate_id" in data
    assert "verification_hash" in data


def test_api_biodiversity_endpoint():
    resp = client.get("/api/innovation/biodiversity")
    assert resp.status_code == 200
    data = resp.json()
    assert "shannon_wiener_index_h" in data
    assert "campus_faunal_support_quotient_fsq" in data
    assert "profiles" in data


def test_api_species_catalog():
    resp = client.get("/api/species")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "species_id" in data[0]
    assert "common_name" in data[0]
    assert "total_trees" in data[0]


def test_api_tree_inspections():
    resp = client.get("/api/trees/CIET-TREE-001/inspections")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    assert data[0]["inspection_id"].startswith("INS-")
    assert "health_status" in data[0]


def test_api_add_tree_inspection():
    payload = {
        "inspection_id": "INS-2026-TEST-99",
        "inspection_date": "2026-10-18",
        "health_status": "Healthy",
        "height_m": 15.2,
        "dbh_cm": 45.5,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Automated verification test audit",
        "inspected_by": "CIET AI Test Suite"
    }
    resp = client.post("/api/trees/CIET-TREE-001/inspections", json=payload)
    assert resp.status_code == 200
    tree_data = resp.json()
    assert any(i["inspection_id"] == "INS-2026-TEST-99" for i in tree_data["inspections"])

