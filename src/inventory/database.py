"""
Enterprise Tree Inventory Database and Geolocation Repository.
Populated with native Western Ghats dendrological taxa for CIET Coimbatore Campus.
"""

from __future__ import annotations

import csv
import io
import json
import logging
from typing import Any, Dict, List, Optional

from src.inventory.models import BiometricTelemetry, GeoLocation, TreeProfile
from src.inventory.qr_engine import generate_tree_qr_code

logger = logging.getLogger("ciet.inventory.database")


class TreeInventoryDatabase:
    """
    High-performance in-memory inventory store with GIS GeoJSON export,
    filtering, and QR code tokenization.
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url
        self._trees: Dict[str, TreeProfile] = {}
        self._initialize_ciet_campus_seed_data()

    def _initialize_ciet_campus_seed_data(self) -> None:
        """Seeds authentic CIET Coimbatore campus inventory records."""
        # CIET Campus coordinates anchor: ~10.999200 N, 76.904500 E (Thondamuthur / Narasipuram, Coimbatore)
        seed_specs = [
            {
                "tree_id": "CIET-TREE-001",
                "common_name": "Neem (Margosa Tree)",
                "scientific_name": "Azadirachta indica",
                "family": "Meliaceae",
                "iucn_status": "Least Concern",
                "native_region": "Western Ghats Foothills & Peninsular India",
                "medicinal_uses": "Broad-spectrum antibacterial, antifungal, air purification, and bio-pesticide.",
                "lat": 10.999245,
                "lon": 76.904312,
                "altitude": 428.5,
                "sector": "Sector-I: Academic Quadrant",
                "landmarks": "North-West lawn adjacent to Main Administrative Block",
                "height": 14.8,
                "dbh": 54.2,
                "crown_spread": 72.0,
                "age": 28,
                "health": "Vigorous",
                "canopy": "Full Foliage",
                "planted": "1998-06-05",
                "tags": ["Medicinal", "Air Purifying", "Campus Landmark"],
            },
            {
                "tree_id": "CIET-TREE-002",
                "common_name": "Heritage Banyan Tree",
                "scientific_name": "Ficus benghalensis",
                "family": "Moraceae",
                "iucn_status": "Least Concern",
                "native_region": "Indian Subcontinent & Western Ghats",
                "medicinal_uses": "Bark tonic for diabetes, latex used for joint inflammation.",
                "lat": 10.998980,
                "lon": 76.904850,
                "altitude": 431.0,
                "sector": "Sector-II: Botanical Reserve",
                "landmarks": "Central Eco-Pavilion and Cultural Quadrangle",
                "height": 22.5,
                "dbh": 142.0,
                "crown_spread": 380.0,
                "age": 75,
                "health": "Vigorous",
                "canopy": "Full Foliage",
                "planted": "1951-08-15",
                "tags": ["Heritage", "Keystone Species", "Ecological Anchor"],
            },
            {
                "tree_id": "CIET-TREE-003",
                "common_name": "Sacred Fig (Peepal Tree)",
                "scientific_name": "Ficus religiosa",
                "family": "Moraceae",
                "iucn_status": "Least Concern",
                "native_region": "Western Ghats & Tropical Asia",
                "medicinal_uses": "High 24-hr oxygen release, respiratory remedies, cardiovascular support.",
                "lat": 10.999610,
                "lon": 76.904120,
                "altitude": 427.0,
                "sector": "Sector-I: Academic Quadrant",
                "landmarks": "Near Library Entrance and Meditation Circle",
                "height": 18.2,
                "dbh": 86.5,
                "crown_spread": 145.0,
                "age": 42,
                "health": "Healthy",
                "canopy": "Full Foliage",
                "planted": "1984-07-22",
                "tags": ["Sacred Grove", "Oxygen Rich", "Shade"],
            },
            {
                "tree_id": "CIET-TREE-004",
                "common_name": "Indian Rosewood (Sissoo)",
                "scientific_name": "Dalbergia latifolia",
                "family": "Fabaceae",
                "iucn_status": "Vulnerable",
                "native_region": "Western Ghats Deciduous Ecosystems",
                "medicinal_uses": "High-density nitrogen fixing legume, soil regeneration, premium timber.",
                "lat": 11.000150,
                "lon": 76.905200,
                "altitude": 434.0,
                "sector": "Sector-IV: Western Ghats Eco-Corridor",
                "landmarks": "Eastern Hillside Boundary Plot #12",
                "height": 19.4,
                "dbh": 68.0,
                "crown_spread": 95.0,
                "age": 35,
                "health": "Healthy",
                "canopy": "Full Foliage",
                "planted": "1991-03-12",
                "tags": ["Vulnerable IUCN", "Nitrogen Fixing", "Timber"],
            },
            {
                "tree_id": "CIET-TREE-005",
                "common_name": "Red Sandalwood",
                "scientific_name": "Pterocarpus santalinus",
                "family": "Fabaceae",
                "iucn_status": "Endangered",
                "native_region": "Southern Eastern/Western Ghats Endemic",
                "medicinal_uses": "Cooling therapeutics, rare flavonoid dye, protected biodiversity specimen.",
                "lat": 10.998720,
                "lon": 76.903890,
                "altitude": 429.5,
                "sector": "Sector-II: Botanical Reserve",
                "landmarks": "Rare & Endangered Botanical Conservation Plot",
                "height": 11.2,
                "dbh": 38.5,
                "crown_spread": 42.0,
                "age": 20,
                "health": "Vigorous",
                "canopy": "Full Foliage",
                "planted": "2006-11-14",
                "tags": ["Endangered IUCN", "High Conservation Value", "Botanical Vault"],
            },
            {
                "tree_id": "CIET-TREE-006",
                "common_name": "Teak Tree",
                "scientific_name": "Tectona grandis",
                "family": "Lamiaceae",
                "iucn_status": "Least Concern",
                "native_region": "Western Ghats Moist Deciduous Forests",
                "medicinal_uses": "High tensile biomass, termite resistant, durable carbon sink.",
                "lat": 11.000450,
                "lon": 76.904720,
                "altitude": 435.5,
                "sector": "Sector-IV: Western Ghats Eco-Corridor",
                "landmarks": "North Eco-Corridor Buffer Ridge",
                "height": 24.1,
                "dbh": 74.0,
                "crown_spread": 88.0,
                "age": 38,
                "health": "Vigorous",
                "canopy": "Full Foliage",
                "planted": "1988-09-01",
                "tags": ["Carbon Sink", "High Biomass"],
            },
            {
                "tree_id": "CIET-TREE-007",
                "common_name": "Jamun (Black Plum)",
                "scientific_name": "Syzygium cumini",
                "family": "Myrtaceae",
                "iucn_status": "Least Concern",
                "native_region": "Western Ghats Riparian Zones",
                "medicinal_uses": "Antidiabetic polyphenols, avian food sanctuary, monsoon water retention.",
                "lat": 10.999450,
                "lon": 76.905620,
                "altitude": 432.0,
                "sector": "Sector-III: Sports Complex Buffer",
                "landmarks": "Rainwater Harvesting Swale Border",
                "height": 16.5,
                "dbh": 59.0,
                "crown_spread": 105.0,
                "age": 31,
                "health": "Healthy",
                "canopy": "Flowering",
                "planted": "1995-04-18",
                "tags": ["Fruit Bearing", "Avian Sanctuary", "Riparian"],
            },
            {
                "tree_id": "CIET-TREE-008",
                "common_name": "Arjun Tree",
                "scientific_name": "Terminalia arjuna",
                "family": "Combretaceae",
                "iucn_status": "Least Concern",
                "native_region": "Western Ghats Stream Banks",
                "medicinal_uses": "Cardiovascular inotropic bark extract, riverbank soil stabilization.",
                "lat": 10.998410,
                "lon": 76.904450,
                "altitude": 426.0,
                "sector": "Sector-II: Botanical Reserve",
                "landmarks": "South Eco-Pond Riparian Strip",
                "height": 17.8,
                "dbh": 64.5,
                "crown_spread": 115.0,
                "age": 29,
                "health": "Vigorous",
                "canopy": "Full Foliage",
                "planted": "1997-10-02",
                "tags": ["Riparian Guard", "Ayurvedic Cardiac"],
            },
            {
                "tree_id": "CIET-TREE-009",
                "common_name": "Pongamia (Indian Beech)",
                "scientific_name": "Pongamia pinnata",
                "family": "Fabaceae",
                "iucn_status": "Least Concern",
                "native_region": "Western Ghats & Tamil Nadu Native",
                "medicinal_uses": "Biofuel seed oil, intense nitrogen fixing root nodules, drought resilience.",
                "lat": 10.999880,
                "lon": 76.903750,
                "altitude": 428.0,
                "sector": "Sector-I: Academic Quadrant",
                "landmarks": "Department of Mechanical Engineering Courtyard",
                "height": 13.5,
                "dbh": 46.0,
                "crown_spread": 68.0,
                "age": 22,
                "health": "Healthy",
                "canopy": "Full Foliage",
                "planted": "2004-06-25",
                "tags": ["Biofuel", "Nitrogen Fixer", "Drought Resilient"],
            },
            {
                "tree_id": "CIET-TREE-010",
                "common_name": "Mahua Tree",
                "scientific_name": "Madhuca longifolia",
                "family": "Sapotaceae",
                "iucn_status": "Near Threatened",
                "native_region": "Western Ghats Indigenous Forests",
                "medicinal_uses": "Edible floral nectar, seed oil for cutaneous medicine, pollinator haven.",
                "lat": 11.000620,
                "lon": 76.905450,
                "altitude": 436.0,
                "sector": "Sector-IV: Western Ghats Eco-Corridor",
                "landmarks": "Hill Slope Biodiversity Transect #4",
                "height": 15.2,
                "dbh": 58.0,
                "crown_spread": 85.0,
                "age": 34,
                "health": "Healthy",
                "canopy": "Full Foliage",
                "planted": "1992-08-10",
                "tags": ["Near Threatened", "Pollinator Sanctuary", "Ethnobotanical"],
            },
        ]

        for s in seed_specs:
            loc = GeoLocation(
                latitude=s["lat"],
                longitude=s["lon"],
                altitude_m=s["altitude"],
                gps_accuracy_m=0.8,
                campus_sector=s["sector"],
                landmarks=s["landmarks"],
            )
            bio = BiometricTelemetry(
                height_m=s["height"],
                dbh_cm=s["dbh"],
                crown_spread_m2=s["crown_spread"],
                estimated_age_years=s["age"],
                health_status=s["health"],
                canopy_condition=s["canopy"],
            )

            _, b64_qr = generate_tree_qr_code(s["tree_id"], base_url=self.base_url)

            tree = TreeProfile(
                tree_id=s["tree_id"],
                common_name=s["common_name"],
                scientific_name=s["scientific_name"],
                family=s["family"],
                iucn_status=s["iucn_status"],
                native_region=s["native_region"],
                medicinal_uses=s["medicinal_uses"],
                location=loc,
                biometrics=bio,
                planted_date=s["planted"],
                last_inspected="2026-09-20",
                inspector="CIET Center for Forestry Informatics",
                qr_code_url=f"{self.base_url}/tree/{s['tree_id']}",
                qr_code_base64=b64_qr,
                tags=s["tags"],
            )
            self._trees[tree.tree_id] = tree

        logger.info("Initialized CIET Tree Inventory Database with %d verified seed trees.", len(self._trees))

    def list_trees(
        self,
        sector: Optional[str] = None,
        iucn_status: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[TreeProfile]:
        """Filters and lists tree profiles."""
        results = list(self._trees.values())

        if sector:
            results = [t for t in results if t.location.campus_sector.lower() == sector.lower()]

        if iucn_status:
            results = [t for t in results if t.iucn_status.lower() == iucn_status.lower()]

        if search_query:
            q = search_query.lower()
            results = [
                t for t in results
                if q in t.tree_id.lower()
                or q in t.common_name.lower()
                or q in t.scientific_name.lower()
                or q in t.family.lower()
                or any(q in tag.lower() for tag in t.tags)
            ]

        return results

    def get_tree(self, tree_id: str) -> Optional[TreeProfile]:
        """Retrieves single tree profile by its unique ID."""
        return self._trees.get(tree_id)

    def add_tree(self, tree: TreeProfile) -> TreeProfile:
        """Adds a newly cataloged or drone-detected tree profile with generated QR code."""
        if not tree.qr_code_base64:
            _, b64_qr = generate_tree_qr_code(tree.tree_id, base_url=self.base_url)
            tree.qr_code_base64 = b64_qr
            tree.qr_code_url = f"{self.base_url}/tree/{tree.tree_id}"

        self._trees[tree.tree_id] = tree
        logger.info("Cataloged new tree specimen %s (%s)", tree.tree_id, tree.scientific_name)
        return tree

    def count(self) -> int:
        """Returns total registered tree count."""
        return len(self._trees)

    def to_geojson(self) -> Dict[str, Any]:
        """Generates RFC 7946 compliant GeoJSON FeatureCollection for GIS visualization."""
        features = [t.to_geojson_feature() for t in self._trees.values()]
        return {
            "type": "FeatureCollection",
            "metadata": {
                "organization": "Coimbatore Institute of Engineering and Technology (CIET)",
                "generated_at": "2026-10-16",
                "total_features": len(features),
            },
            "features": features,
        }

    def to_csv(self) -> str:
        """Exports tabular inventory dataset as CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Tree ID", "Common Name", "Scientific Name", "Family", "IUCN Status",
            "Latitude", "Longitude", "Altitude (m)", "Sector", "Height (m)",
            "DBH (cm)", "Crown Spread (m2)", "Age (Years)", "Carbon Sequestered (kg CO2)",
            "Health", "Planted Date", "QR URL"
        ])
        for t in self._trees.values():
            writer.writerow([
                t.tree_id, t.common_name, t.scientific_name, t.family, t.iucn_status,
                t.location.latitude, t.location.longitude, t.location.altitude_m,
                t.location.campus_sector, t.biometrics.height_m, t.biometrics.dbh_cm,
                t.biometrics.crown_spread_m2, t.biometrics.estimated_age_years,
                t.biometrics.carbon_sequestered_kg, t.biometrics.health_status,
                t.planted_date, t.qr_code_url,
            ])
        return output.getvalue()

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Calculates macro ecological and carbon accounting indicators."""
        total_trees = len(self._trees)
        if total_trees == 0:
            return {"total_trees": 0, "total_carbon_kg": 0.0, "total_canopy_m2": 0.0}

        total_co2 = sum(t.biometrics.carbon_sequestered_kg for t in self._trees.values())
        total_canopy_m2 = sum(t.biometrics.crown_spread_m2 for t in self._trees.values())
        avg_age = sum(t.biometrics.estimated_age_years for t in self._trees.values()) / float(total_trees)
        endangered_count = sum(1 for t in self._trees.values() if t.iucn_status in ["Endangered", "Vulnerable", "Near Threatened"])

        return {
            "total_trees": total_trees,
            "total_carbon_sequestered_kg": round(total_co2, 2),
            "total_carbon_sequestered_tonnes": round(total_co2 / 1000.0, 3),
            "total_canopy_coverage_m2": round(total_canopy_m2, 2),
            "average_tree_age_years": round(avg_age, 1),
            "high_conservation_species_count": endangered_count,
            "sectors_monitored": len(set(t.location.campus_sector for t in self._trees.values())),
        }


# Singleton database instance
_DB_INSTANCE: Optional[TreeInventoryDatabase] = None


def get_inventory_db(base_url: str = "http://localhost:8000") -> TreeInventoryDatabase:
    """Returns singleton instance of TreeInventoryDatabase."""
    global _DB_INSTANCE
    if _DB_INSTANCE is None:
        _DB_INSTANCE = TreeInventoryDatabase(base_url=base_url)
    return _DB_INSTANCE
