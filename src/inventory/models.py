"""
Structural Domain Models for Tree Biometrics, Geolocation, and Digital QR Passports.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class GeoLocation(BaseModel):
    """
    Precision GPS coordinate model for individual tree crowns on the CIET campus.
    """

    latitude: float = Field(..., ge=-90.0, le=90.0, description="WGS84 Latitude coordinate")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="WGS84 Longitude coordinate")
    altitude_m: float = Field(default=430.0, description="Elevation above mean sea level in meters")
    gps_accuracy_m: float = Field(default=0.8, ge=0.0, description="Differential GPS accuracy radius in meters")
    campus_sector: str = Field(
        default="Sector-I: Academic Quadrant",
        description="Designated campus land-use sector or ecological plot",
    )
    landmarks: str = Field(
        default="Adjacent to Main Academic Block & Herbal Garden",
        description="Field reference cues for physical ground navigation",
    )

    def to_lat_lon_str(self) -> str:
        """Formatted human-readable DMS/decimal representation."""
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        return f"{abs(self.latitude):.6f}° {lat_dir}, {abs(self.longitude):.6f}° {lon_dir}"

    def google_maps_url(self) -> str:
        """Direct link for satellite navigation on mobile devices."""
        return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"


class BiometricTelemetry(BaseModel):
    """
    Dendrological and ecological metrics for carbon accounting and forestry conservation.
    """

    height_m: float = Field(..., gt=0.0, description="Total vertical height in meters")
    dbh_cm: float = Field(..., gt=0.0, description="Diameter at Breast Height (1.37m above ground) in cm")
    crown_spread_m2: float = Field(..., gt=0.0, description="Projected planar canopy footprint area in m²")
    estimated_age_years: int = Field(..., ge=1, description="Estimated tree age in years")
    carbon_sequestered_kg: float = Field(
        default=0.0, ge=0.0, description="Estimated total lifetime biomass CO2 sequestration in kg"
    )
    health_status: str = Field(
        default="Vigorous",
        description="Health rating: 'Vigorous', 'Healthy', 'Requires Pruning', 'Distressed'",
    )
    canopy_condition: str = Field(
        default="Full Foliage",
        description="Foliage condition: 'Full Foliage', 'Partial Defoliation', 'Flowering', 'Fruiting'",
    )

    @model_validator(mode="after")
    def calculate_carbon_if_zero(self) -> BiometricTelemetry:
        """
        Calculates allometric above-ground biomass carbon sequestration using standard
        Chave et al. tropical pan-forestry allometric equation if not explicitly provided.
        """
        if self.carbon_sequestered_kg <= 0.0:
            # Approximate Above Ground Biomass (AGB) in kg: AGB = 0.0673 * (wood_density * (dbh^2) * height)^0.976
            # Mean tropical wood specific gravity ~ 0.60 g/cm^3. Carbon content ~ 47.5%. Carbon to CO2 = 3.67.
            wood_density = 0.62
            agb_kg = 0.0673 * ((wood_density * (self.dbh_cm ** 2) * self.height_m) ** 0.976)
            total_biomass_kg = agb_kg * 1.26  # Include below-ground root biomass ratio (26%)
            carbon_kg = total_biomass_kg * 0.475
            co2_kg = carbon_kg * 3.67
            object.__setattr__(self, "carbon_sequestered_kg", round(co2_kg, 2))
        return self


class InspectionRecord(BaseModel):
    """
    Physical field inspection and health history observation.
    Captures temporal tree growth, health transitions, and pest/stress signs.
    """
    inspection_id: str = Field(..., description="Unique inspection audit ID, e.g., INS-2026-001")
    inspection_date: str = Field(..., description="ISO date of inspection (YYYY-MM-DD)")
    health_status: str = Field(default="Healthy", description="Healthy, Needs Attention, Poor, Critical")
    height_m: float = Field(..., gt=0.0, description="Measured height at inspection in meters")
    dbh_cm: float = Field(..., gt=0.0, description="Diameter at breast height in cm")
    leaf_condition: str = Field(default="Good", description="Leaf foliage health: Good, Sparse, Chlorosis, Vigorous")
    trunk_condition: str = Field(default="Sound", description="Bark/wood condition: Sound, Minor Fissures, Cavity Healing, Termite Resistance")
    pest_signs: str = Field(default="None observed", description="Observed pest infestations or pathogen symptoms")
    stress_signs: str = Field(default="None", description="Hydrological or thermal stress observations")
    observations: str = Field(default="Healthy growth", description="Field notes and remedial forestry recommendations")
    inspected_by: str = Field(default="CIET Center for Forestry Informatics", description="Surveyor or arborist name")
    photo_url: Optional[str] = Field(default=None, description="Optional photo URL taken during inspection")


class SpeciesSummary(BaseModel):
    """
    Aggregated botanical species catalog entry.
    """
    species_id: str
    common_name: str
    scientific_name: str
    family: str
    iucn_status: str
    total_trees: int
    native_region: str
    medicinal_uses: str


class TreeProfile(BaseModel):
    """
    Complete Digital Passport for an individual tree specimen.
    """

    tree_id: str = Field(..., description="Unique institutional identifier (e.g., CIET-TREE-001)")
    common_name: str = Field(..., description="Common vernacular name (e.g., Neem, Teak, Banyan)")
    scientific_name: str = Field(..., description="Botanical binomial nomenclature (e.g., Azadirachta indica)")
    family: str = Field(..., description="Botanical family (e.g., Meliaceae)")
    iucn_status: str = Field(
        default="Least Concern",
        description="IUCN Red List Conservation status (e.g., Least Concern, Near Threatened, Vulnerable)",
    )
    native_region: str = Field(default="Western Ghats & Peninsular India", description="Ecological endemic origin")
    medicinal_uses: str = Field(
        default="Traditional Ayurvedic applications and antimicrobial properties.",
        description="Ethnobotanical significance",
    )
    location: GeoLocation = Field(..., description="GPS coordinates and campus plot sector")
    biometrics: BiometricTelemetry = Field(..., description="Dendrological measurements and carbon storage")
    planted_date: str = Field(default="2012-07-15", description="Historical planting or germination date")
    last_inspected: str = Field(default="2026-09-20", description="Date of most recent physical drone/ground audit")
    inspector: str = Field(default="CIET Forestry Division", description="Certifying surveyor or research authority")
    qr_code_url: str = Field(default="", description="Target URI encoded in physical tree tag QR code")
    qr_code_base64: Optional[str] = Field(default=None, description="Pre-computed Base64 PNG QR code tag")
    tags: List[str] = Field(default_factory=list, description="Categorical tags for filtering")
    inspections: List[InspectionRecord] = Field(
        default_factory=list, description="Historical timeline of physical field audits and growth tracking"
    )

    def to_geojson_feature(self) -> Dict[str, Any]:
        """Converts profile to GeoJSON Feature for GIS and mapping applications."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.location.longitude, self.location.latitude, self.location.altitude_m],
            },
            "properties": {
                "tree_id": self.tree_id,
                "common_name": self.common_name,
                "scientific_name": self.scientific_name,
                "family": self.family,
                "iucn_status": self.iucn_status,
                "height_m": self.biometrics.height_m,
                "dbh_cm": self.biometrics.dbh_cm,
                "crown_spread_m2": self.biometrics.crown_spread_m2,
                "estimated_age_years": self.biometrics.estimated_age_years,
                "carbon_sequestered_kg": self.biometrics.carbon_sequestered_kg,
                "health_status": self.biometrics.health_status,
                "campus_sector": self.location.campus_sector,
                "qr_code_url": self.qr_code_url,
                "google_maps_url": self.location.google_maps_url(),
            },
        }
