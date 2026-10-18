"""
Automated Unit and Integration Tests for Inventory, Geolocation, and QR Code Subsystems.
"""

from __future__ import annotations

import io
import json
import pytest
from PIL import Image

from src.inventory.database import TreeInventoryDatabase
from src.inventory.models import BiometricTelemetry, GeoLocation, TreeProfile
from src.inventory.qr_engine import (
    decode_qr_image,
    generate_printable_tree_tag,
    generate_tree_qr_code,
)


def test_geolocation_formatting_and_google_maps() -> None:
    """Verifies GPS coordinate string formatting and navigation URL."""
    loc = GeoLocation(
        latitude=10.999200,
        longitude=76.904500,
        altitude_m=430.0,
        campus_sector="Sector-I: Academic Quadrant",
    )
    assert "10.999200° N" in loc.to_lat_lon_str()
    assert "76.904500° E" in loc.to_lat_lon_str()
    assert "10.9992,76.9045" in loc.google_maps_url()


def test_biometric_carbon_allometric_equation() -> None:
    """Ensures Chave allometric equation calculates non-zero CO2 biomass automatically."""
    bio = BiometricTelemetry(
        height_m=15.0,
        dbh_cm=50.0,
        crown_spread_m2=75.0,
        estimated_age_years=25,
        health_status="Vigorous",
    )
    # Carbon sequestration must be computed automatically (> 0)
    assert bio.carbon_sequestered_kg > 0.0
    # For a 50cm DBH, 15m height tree, biomass CO2 is typically ~ 800 - 2500 kg
    assert 500.0 < bio.carbon_sequestered_kg < 5000.0


def test_tree_profile_geojson_conversion() -> None:
    """Verifies RFC 7946 GeoJSON Feature format conversion."""
    loc = GeoLocation(latitude=10.999, longitude=76.904, altitude_m=428.0)
    bio = BiometricTelemetry(height_m=12.0, dbh_cm=45.0, crown_spread_m2=60.0, estimated_age_years=20)
    profile = TreeProfile(
        tree_id="TEST-TREE-999",
        common_name="Test Neem",
        scientific_name="Azadirachta indica",
        family="Meliaceae",
        location=loc,
        biometrics=bio,
    )
    feat = profile.to_geojson_feature()
    assert feat["type"] == "Feature"
    assert feat["geometry"]["type"] == "Point"
    assert feat["geometry"]["coordinates"] == [76.904, 10.999, 428.0]
    assert feat["properties"]["tree_id"] == "TEST-TREE-999"


def test_qr_code_generation_and_decoding() -> None:
    """End-to-end verification: generates a QR code and decodes it via OpenCV."""
    tree_id = "CIET-TREE-VERIFY"
    png_bytes, b64_str = generate_tree_qr_code(tree_id, base_url="http://localhost:8000")

    assert len(png_bytes) > 0
    assert len(b64_str) > 0

    # Verify PNG header
    pil_img = Image.open(io.BytesIO(png_bytes))
    assert pil_img.format == "PNG"

    # Decode via OpenCV QR detector
    decoded = decode_qr_image(png_bytes)
    assert decoded is not None
    assert tree_id in decoded
    assert "http://localhost:8000/tree/CIET-TREE-VERIFY" in decoded


def test_generate_printable_field_tag() -> None:
    """Verifies generation of printable physical field tag badge."""
    tag_bytes = generate_printable_tree_tag(
        tree_id="CIET-TAG-001",
        common_name="Neem Tree",
        scientific_name="Azadirachta indica",
        location_str="10.999° N, 76.904° E",
        carbon_kg=1250.0,
    )
    assert len(tag_bytes) > 0
    pil_tag = Image.open(io.BytesIO(tag_bytes))
    assert pil_tag.size == (800, 420)


def test_inventory_database_operations() -> None:
    """Validates inventory querying, sector filtering, and GeoJSON/CSV exports."""
    db = TreeInventoryDatabase()
    assert db.count() >= 10

    # Sector filter
    academic_trees = db.list_trees(sector="Sector-I: Academic Quadrant")
    assert len(academic_trees) > 0
    for t in academic_trees:
        assert t.location.campus_sector == "Sector-I: Academic Quadrant"

    # GeoJSON export
    geojson = db.to_geojson()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == db.count()

    # CSV export
    csv_str = db.to_csv()
    assert "Tree ID,Common Name,Scientific Name" in csv_str
    assert "CIET-TREE-001" in csv_str

    # Summary metrics
    metrics = db.get_metrics_summary()
    assert metrics["total_trees"] == db.count()
    assert metrics["total_carbon_sequestered_kg"] > 0.0
    assert metrics["total_canopy_coverage_m2"] > 0.0


def test_species_catalog_aggregation() -> None:
    """Verifies that species catalog correctly aggregates species from tree inventory."""
    db = TreeInventoryDatabase()
    catalog = db.get_species_catalog()
    assert len(catalog) > 0

    neem_entry = next((s for s in catalog if "Azadirachta" in s.scientific_name), None)
    assert neem_entry is not None
    assert neem_entry.total_trees >= 1
    assert neem_entry.species_id.startswith("SP-")
    assert neem_entry.family == "Meliaceae"


def test_multi_year_inspections_and_add_audit() -> None:
    """Verifies multi-year inspection history and adding a new field audit."""
    from src.inventory.models import InspectionRecord

    db = TreeInventoryDatabase()
    tree = db.get_tree("CIET-TREE-001")
    assert tree is not None
    assert len(tree.inspections) >= 3

    # Check inspection ID format and health status
    assert any(ins.inspection_id == "INS-2024-001" for ins in tree.inspections)
    assert any(ins.inspection_id == "INS-2026-001" for ins in tree.inspections)

    # Add a new inspection
    new_audit = InspectionRecord(
        inspection_id="INS-2026-T01-EXTRA",
        inspection_date="2026-10-18",
        health_status="Healthy",
        height_m=14.5,
        dbh_cm=44.0,
        leaf_condition="Vibrant Dark Green",
        trunk_condition="Sound Bark Integrity",
        pest_signs="None observed",
        stress_signs="None",
        observations="Autumn health verification passed",
        inspected_by="CIET Forestry AI Ranger",
    )
    updated_tree = db.add_inspection("CIET-TREE-001", new_audit)
    assert updated_tree is not None
    assert any(ins.inspection_id == "INS-2026-T01-EXTRA" for ins in updated_tree.inspections)


