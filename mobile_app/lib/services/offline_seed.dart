// Auto-generated offline seed data for CIET trees
import 'dart:convert';
import '../models/tree_model.dart';

class OfflineSeed {
  static const String rawJson = r'''[
  {
    "tree_id": "CIET-TREE-001",
    "common_name": "Neem (Margosa Tree)",
    "scientific_name": "Azadirachta indica",
    "family": "Meliaceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats Foothills & Peninsular India",
    "medicinal_uses": "Broad-spectrum antibacterial, antifungal, air purification, and bio-pesticide.",
    "location": {
      "latitude": 10.99568,
      "longitude": 76.77312,
      "altitude_m": 485.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-I: Academic Quadrant",
      "landmarks": "North-West lawn adjacent to Main Administrative Block"
    },
    "biometrics": {
      "height_m": 14.8,
      "dbh_cm": 54.2,
      "crown_spread_m2": 72.0,
      "estimated_age_years": 28,
      "carbon_sequestered_kg": 3119.33,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1998-06-05",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-001",
    "qr_code_base64": "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",
    "tags": [
      "Medicinal",
      "Air Purifying",
      "Campus Landmark"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-001",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 13.0,
        "dbh_cm": 48.8,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Neem (Margosa Tree). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-001",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 13.9,
        "dbh_cm": 51.5,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.9m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-001",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 14.8,
        "dbh_cm": 54.2,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-002",
    "common_name": "Heritage Banyan Tree",
    "scientific_name": "Ficus benghalensis",
    "family": "Moraceae",
    "iucn_status": "Least Concern",
    "native_region": "Indian Subcontinent & Western Ghats",
    "medicinal_uses": "Bark tonic for diabetes, latex used for joint inflammation.",
    "location": {
      "latitude": 10.99522,
      "longitude": 76.77352,
      "altitude_m": 486.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-II: Botanical Reserve",
      "landmarks": "Central Eco-Pavilion and Cultural Quadrangle"
    },
    "biometrics": {
      "height_m": 22.5,
      "dbh_cm": 142.0,
      "crown_spread_m2": 380.0,
      "estimated_age_years": 75,
      "carbon_sequestered_kg": 30769.23,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1951-08-15",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-002",
    "qr_code_base64": "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",
    "tags": [
      "Heritage",
      "Keystone Species",
      "Ecological Anchor"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-002",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 19.8,
        "dbh_cm": 127.8,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Heritage Banyan Tree. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-002",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 21.1,
        "dbh_cm": 134.9,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.3m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-002",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 22.5,
        "dbh_cm": 142.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-003",
    "common_name": "Sacred Fig (Peepal Tree)",
    "scientific_name": "Ficus religiosa",
    "family": "Moraceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats & Tropical Asia",
    "medicinal_uses": "High 24-hr oxygen release, respiratory remedies, cardiovascular support.",
    "location": {
      "latitude": 10.99542,
      "longitude": 76.77298,
      "altitude_m": 484.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-I: Academic Quadrant",
      "landmarks": "Near Library Entrance and Meditation Circle"
    },
    "biometrics": {
      "height_m": 18.2,
      "dbh_cm": 86.5,
      "crown_spread_m2": 145.0,
      "estimated_age_years": 42,
      "carbon_sequestered_kg": 9506.15,
      "health_status": "Healthy",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1984-07-22",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-003",
    "qr_code_base64": "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",
    "tags": [
      "Sacred Grove",
      "Oxygen Rich",
      "Shade"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-003",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 16.0,
        "dbh_cm": 77.9,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Sacred Fig (Peepal Tree). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-003",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 17.1,
        "dbh_cm": 82.2,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.1m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-003",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 18.2,
        "dbh_cm": 86.5,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-004",
    "common_name": "Indian Rosewood (Sissoo)",
    "scientific_name": "Dalbergia latifolia",
    "family": "Fabaceae",
    "iucn_status": "Vulnerable",
    "native_region": "Western Ghats Deciduous Ecosystems",
    "medicinal_uses": "High-density nitrogen fixing legume, soil regeneration, premium timber.",
    "location": {
      "latitude": 10.99665,
      "longitude": 76.77365,
      "altitude_m": 489.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-IV: Western Ghats Eco-Corridor",
      "landmarks": "Eastern Hillside Boundary Plot #12"
    },
    "biometrics": {
      "height_m": 19.4,
      "dbh_cm": 68.0,
      "crown_spread_m2": 95.0,
      "estimated_age_years": 35,
      "carbon_sequestered_kg": 6325.16,
      "health_status": "Healthy",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1991-03-12",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-004",
    "qr_code_base64": "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",
    "tags": [
      "Vulnerable IUCN",
      "Nitrogen Fixing",
      "Timber"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-004",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 17.1,
        "dbh_cm": 61.2,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Indian Rosewood (Sissoo). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-004",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 18.2,
        "dbh_cm": 64.6,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.1m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-004",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 19.4,
        "dbh_cm": 68.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-005",
    "common_name": "Red Sandalwood",
    "scientific_name": "Pterocarpus santalinus",
    "family": "Fabaceae",
    "iucn_status": "Endangered",
    "native_region": "Southern Eastern/Western Ghats Endemic",
    "medicinal_uses": "Cooling therapeutics, rare flavonoid dye, protected biodiversity specimen.",
    "location": {
      "latitude": 10.99632,
      "longitude": 76.77272,
      "altitude_m": 486.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-II: Botanical Reserve",
      "landmarks": "Rare & Endangered Botanical Conservation Plot"
    },
    "biometrics": {
      "height_m": 11.2,
      "dbh_cm": 38.5,
      "crown_spread_m2": 42.0,
      "estimated_age_years": 20,
      "carbon_sequestered_kg": 1218.92,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "2006-11-14",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-005",
    "qr_code_base64": "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",
    "tags": [
      "Endangered IUCN",
      "High Conservation Value",
      "Botanical Vault"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-005",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 9.9,
        "dbh_cm": 34.6,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Red Sandalwood. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-005",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 10.5,
        "dbh_cm": 36.6,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.6m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-005",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 11.2,
        "dbh_cm": 38.5,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-006",
    "common_name": "Teak Tree",
    "scientific_name": "Tectona grandis",
    "family": "Lamiaceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats Moist Deciduous Forests",
    "medicinal_uses": "High tensile biomass, termite resistant, durable carbon sink.",
    "location": {
      "latitude": 10.99645,
      "longitude": 76.77352,
      "altitude_m": 488.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-IV: Western Ghats Eco-Corridor",
      "landmarks": "North Eco-Corridor Buffer Ridge"
    },
    "biometrics": {
      "height_m": 24.1,
      "dbh_cm": 74.0,
      "crown_spread_m2": 88.0,
      "estimated_age_years": 38,
      "carbon_sequestered_kg": 9219.52,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1988-09-01",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-006",
    "qr_code_base64": "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",
    "tags": [
      "Carbon Sink",
      "High Biomass"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-006",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 21.2,
        "dbh_cm": 66.6,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Teak Tree. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-006",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 22.7,
        "dbh_cm": 70.3,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.5m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-006",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 24.1,
        "dbh_cm": 74.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-007",
    "common_name": "Jamun (Black Plum)",
    "scientific_name": "Syzygium cumini",
    "family": "Myrtaceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats Riparian Zones",
    "medicinal_uses": "Antidiabetic polyphenols, avian food sanctuary, monsoon water retention.",
    "location": {
      "latitude": 10.99468,
      "longitude": 76.77378,
      "altitude_m": 483.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-III: Sports Complex Buffer",
      "landmarks": "Rainwater Harvesting Swale Border"
    },
    "biometrics": {
      "height_m": 16.5,
      "dbh_cm": 59.0,
      "crown_spread_m2": 105.0,
      "estimated_age_years": 31,
      "carbon_sequestered_kg": 4093.43,
      "health_status": "Healthy",
      "canopy_condition": "Flowering"
    },
    "planted_date": "1995-04-18",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-007",
    "qr_code_base64": "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",
    "tags": [
      "Fruit Bearing",
      "Avian Sanctuary",
      "Riparian"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-007",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 14.5,
        "dbh_cm": 53.1,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Jamun (Black Plum). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-007",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 15.5,
        "dbh_cm": 56.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.0m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-007",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 16.5,
        "dbh_cm": 59.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-008",
    "common_name": "Arjun Tree",
    "scientific_name": "Terminalia arjuna",
    "family": "Combretaceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats Stream Banks",
    "medicinal_uses": "Cardiovascular inotropic bark extract, riverbank soil stabilization.",
    "location": {
      "latitude": 10.99455,
      "longitude": 76.77358,
      "altitude_m": 483.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-II: Botanical Reserve",
      "landmarks": "South Eco-Pond Riparian Strip"
    },
    "biometrics": {
      "height_m": 17.8,
      "dbh_cm": 64.5,
      "crown_spread_m2": 115.0,
      "estimated_age_years": 29,
      "carbon_sequestered_kg": 5245.54,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1997-10-02",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-008",
    "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaCAIAAAC5ZBI0AAAJIklEQVR4nO3dQW4jRxJA0e6BAF5q7jBn9R18Ka7orVeFAVLZGfn13r7FEkV+pI2Iqt+fz+cXwP3+c/oCAL6HnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRHyt/OPX//77q+X919+bfvLKe7VyVc+vu+8nr3i+qt5vtMJ38N+czoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgIilrYBTk9Azp6hPzWevTMnvm7CfOSX//LozNwpWvH/Yd9DpDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiNi4FdC7L/vK6+6bv9/3ur3nG9y4T3Ljcwbeh/5GTmdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ0DEsa2AnpnPClj5tzfeO3/fJsPMDQr+zekMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIsBVwwaT7Pqfu6H/qLvXPr3vqaQDP7Az8/5zOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6AiGNbATfOOu+75n337N93zTN/8sx9g5mf9vfIq1rhdAZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkRs3Aro3Vl/393x/dvveq+enXqCwbN9v+8r9x185nQGRMgZECFnQIScARFyBkTIGRAhZ0CEnAERcgZE/P58Pqev4RorM9b7ZrtnTo3PvKob9e7ov4/TGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZEHFsK2DmhP0pM+9hf2pa/dSuwsz3ecV72/MrZnI6AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIpa2AmZOUc/cGTh1VTNfd2Uefea7cer3PbWb8R55zU5nQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAxMZnBZya/F4xcx59xcz7we+7qpm/74qZGxSvke+z0xkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRCx8VkBN06c/7SnH5ya/LZf8Wfe52e9T7vTGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZELFxK+DZzFnnU1c1czp/5ruxz74p+Znv5Cv3JAGnMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIGJpK2CfG6fVZ24jrJj5rIBnMzcK9s3Qn3onXyP/gk5nQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAxMatgBvnpGde1bOZ0/m9LYgbf6Of9l45nQERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFfK//41JT8zInkmWZuMszc+tj3b2/crnm28rr7rsrpDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiFjaCni2b/Z35pz0qWl19/v/rndy3/t86jO5YubTLZ45nQERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARG/P5/PkRe+cbJ/5s7AjTPlM58GMHP7YsX7wu+CZwUA+I9NoML/OwMi5AyIkDMgQs6ACDkDIuQMiJAzIOJr5pz0jRPJvQ2Kme/VqWs+tcmw8pNfhzYZTr2u0xkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRCxtBVwah79xvv9r5i5q7Di1KT7vtn9mU8/eB36Dp76PDudARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEb8/n8+mHz1zInnmfehP3Wn+xn2DU5+NU/b9jV6HPhv7XtfpDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiPiaOfd/47T6sxv3HPa97r6ffONd+fd5jZz738fpDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiNj4rIB9Tm0jzHxWwIqZzzfY97orTn2uVq7qxk2GFU5nQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAxNCtgJmz+8/2zXafmoNfMfPu+DPNnL9/HdpVWOF0BkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRFy5FbDPzOn8U/eD92yEP+PGZ1+8tn0XVj7tTmdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ0DE174ffere+afuU75vdv+Ufe/kqSc2zJyhv/FZAe+R+zNOZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQMTGZwXceKf5G6/qxicYPDs1Q3/jzsDMb9n70J6D0xkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRDxdePdxGfOhT9beTdmTpyf8tPuu/9s31//feG3zOkMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyI2PisgBWn7oA+c6b82b79ipmbG89ufHLCzO2L94XfMqczIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgYuhWwEynpuRnPpNh5hMMTk3n3zhD/9q2jXDqL+h0BkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRCxtBcy8x/mKfRP2K05N2O9z4zMZVty4m3HjUyaczoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgIivnzb5fWpeecWNd9afOTU+cw6+9y17H3qvnM6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoCIjVsBz/ZNBs+c3V8xcx792b5thJXXfbZyVft2FWb+fVfs++s7nQERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARHHtgJudOru+DPv93/q971xJ2TfvkHvM7nC6QyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIiwFfBtPP3gzzg1cf5s5o7E69B+xamdAaczIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMg4thWwMzZ7p921/aZf4V9VzVzc+PGz9UzzwoAWOI/NoEIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIGLjVsC+CeyZZs6F/7S/78w9hxWnPhuvCzcKnM6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoCI35/P5/Q1AHwDpzMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgAg5A341/AO2N8usGmk9UgAAAABJRU5ErkJggg==",
    "tags": [
      "Riparian Guard",
      "Ayurvedic Cardiac"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-008",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 15.7,
        "dbh_cm": 58.1,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Arjun Tree. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-008",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 16.7,
        "dbh_cm": 61.3,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.0m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-008",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 17.8,
        "dbh_cm": 64.5,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-009",
    "common_name": "Pongamia (Indian Beech)",
    "scientific_name": "Pongamia pinnata",
    "family": "Fabaceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats & Tamil Nadu Native",
    "medicinal_uses": "Biofuel seed oil, intense nitrogen fixing root nodules, drought resilience.",
    "location": {
      "latitude": 10.99595,
      "longitude": 76.77348,
      "altitude_m": 486.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-I: Academic Quadrant",
      "landmarks": "Department of Mechanical Engineering Courtyard"
    },
    "biometrics": {
      "height_m": 13.5,
      "dbh_cm": 46.0,
      "crown_spread_m2": 68.0,
      "estimated_age_years": 22,
      "carbon_sequestered_kg": 2070.28,
      "health_status": "Healthy",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "2004-06-25",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-009",
    "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaCAIAAAC5ZBI0AAAJHUlEQVR4nO3dUY7bOhJA0fRDA97U7OGtdfYwm/KXZwdCAKZC8vY5/23Lkn3BBEXp6/P5/AK43z+7DwDgz5AzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoCI75U/fv37n18t7//+77rP+3zMz+Y+0cqZnPtEc9f3xlc+08rVtzoDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMilnYFzE33ztk1Bz93VGdOnM/97fMxr1yFM7+xK94/7DdodQZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkQM7gq4cTp/7pV33cN+zq6746/YtYPizOv7uvA3+MzqDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiNi2K+BGc1PUu6bV52bZz9xBMXeuenf0v5HVGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZEGFXwPV23ZV/156BXZ/o2dyOAnsGfp/VGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZELFtV4BZ5z91rubujr9yVHPv+2zXHf13fd4V79wzCqzOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6AiMFdAWdOQvdm98/cM7DrfZ/9tM/7+mG/QaszIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMg4uvz+ew+hh9h12T/nDOP6tmu/Qb8HVZnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAxKG7AuYmzne98pkT5z/tXvIrzny+wbPXhU9dWPm8VmdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ0DE99xLz00k75o5nnvfM8/Vs13PN9h19X/a2Xgd+crPrM6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoCIpV0Bc7POc+97493xzzzmXUc1d33n5uB37Rl4j73vmd9JqzMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyDi6/P5xHYFPNs1n/3M+/7+eT7z6Qdz73uj16bnOVidARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEYO7Ap6deSfyuaNamXWeu6f7rj0SZ95p/sZvzpn7SZ7NHZXVGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZEPG98sc3TrqvHNUuvWcUnPm92uXM6/sa+9u5a2R1BkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRAw+K+DMPQNzdk2c7zpXZz5XobdnYO77/D7yF2pXAIB/bAIV/u8MiJAzIELOgAg5AyLkDIiQMyBCzoCIpV0BZ04z3zglv+v5Br3J/hW7ruCKM49qF6szIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMg4nvupc+84/vcTPmNuxFuvNP8szPP85lPt3h25rl6ZnUGRMgZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEDO4KWDE3Y73rrvxzVo7qxk905tU/cyfDs95OBqszIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMg4vvMu4nvui/73PMN5pw56X7jnebPfPbF3Cu/L/xEz6zOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6AiKVdASvT2zfe0/3ZjXeLP5O9Cn/nt/C68JfyzOoMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIGHxWwI13mt9l7ukHz868Rme+74qVYz7zG/s+8ldmdQZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkQs7Qq4cWp81zTzmfdl37X7YtfZeDZ39X/aLoj3pve1OgMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyK+Pp9PbO5/l12T0DfybIQTzkZvJ4PVGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZELH0rIBdd/RfceNuhLmp8V1X8MxjXnHjXflfubNhdQZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkRse1ZA7z7lK86cg587G7v2hMw587kZ702v7FkBAEv8YxOIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyKWdgWsOHNafUVvj8SZewaezT2F4Majeh95jZ6tHLPVGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZEPG98scrE8krs85nznavOHPye+5MrjhzT8icXXsGXpuu7wqrMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIGLwWQG75u/PvHv6jXdtv9GNU/I37mM587dgdQZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkQs7QqYm1e+cXp7xa4z2Ztl3zWP3tvX8b5w/4zVGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZEPF95tzwyiufObvfm7Cf27nhqQu/fyZ7uxFWWJ0BEXIGRMgZECFnQIScARFyBkTIGRAhZ0CEnAER254VcKa5GfrenoE5vac97HoyxvuHPZHD6gyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIhYelbAMxPnJ0xv37iTYW4efW4Hxa5v+5m/svemHQVWZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQMTgroBnZ95r/Exzc/9n7ig4c7/B3Jk88zy/jnySwDOrMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIGLbroAb3TgXvuspBM/mZsp3Tav3zuSzXXP/z6zOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6ACLsCLpjAPnPye9czGc58FsSufQ4rf/u6cJfLM6szIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgYtuugDNnu2+c3b/xnu4rR3XjJ1r5bsy98ju3r8PqDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiBjcFXDm9PacM+/Zv+uodk2N9751c3P/r7E9A7uejWB1BkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRHx9Pp/dxwDwB1idARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBnwq+H/+evK7KIOlcwAAAAASUVORK5CYII=",
    "tags": [
      "Biofuel",
      "Nitrogen Fixer",
      "Drought Resilient"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-009",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 11.9,
        "dbh_cm": 41.4,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Pongamia (Indian Beech). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-009",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 12.7,
        "dbh_cm": 43.7,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.8m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-009",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 13.5,
        "dbh_cm": 46.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-010",
    "common_name": "Mahua Tree",
    "scientific_name": "Madhuca longifolia",
    "family": "Sapotaceae",
    "iucn_status": "Near Threatened",
    "native_region": "Western Ghats Indigenous Forests",
    "medicinal_uses": "Edible floral nectar, seed oil for cutaneous medicine, pollinator haven.",
    "location": {
      "latitude": 10.99682,
      "longitude": 76.7734,
      "altitude_m": 490.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-IV: Western Ghats Eco-Corridor",
      "landmarks": "Hill Slope Biodiversity Transect #4"
    },
    "biometrics": {
      "height_m": 15.2,
      "dbh_cm": 58.0,
      "crown_spread_m2": 85.0,
      "estimated_age_years": 34,
      "carbon_sequestered_kg": 3654.35,
      "health_status": "Healthy",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1992-08-10",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-010",
    "qr_code_base64": "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",
    "tags": [
      "Near Threatened",
      "Pollinator Sanctuary",
      "Ethnobotanical"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-010",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 13.4,
        "dbh_cm": 52.2,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Mahua Tree. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-010",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 14.3,
        "dbh_cm": 55.1,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.9m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-010",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 15.2,
        "dbh_cm": 58.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-011",
    "common_name": "Tamarind Tree",
    "scientific_name": "Tamarindus indica",
    "family": "Fabaceae",
    "iucn_status": "Least Concern",
    "native_region": "Peninsular India & Tamil Nadu Heritage",
    "medicinal_uses": "Rich in tartaric acid, antioxidant polyphenols, digestive tonic, and dense carbon sink.",
    "location": {
      "latitude": 10.99495,
      "longitude": 76.77308,
      "altitude_m": 484.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-I: Academic Quadrant",
      "landmarks": "South perimeter lawn near Student Food Court & Canteen"
    },
    "biometrics": {
      "height_m": 18.0,
      "dbh_cm": 78.0,
      "crown_spread_m2": 160.0,
      "estimated_age_years": 45,
      "carbon_sequestered_kg": 7684.83,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1981-03-21",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-011",
    "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaCAIAAAC5ZBI0AAAI80lEQVR4nO3dS44juRVA0SojAW3Ke/Baew/elEby1KPoBljEI6/OmUsKffKCCTwGf38+n18A9/vX9AUA/BlyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQ8bPy4Nd//v2r5f3Xfzc988pntXJVz6879cz7fjn73lHvd3Wmlc/K6gyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIhY2hUwNQl95hT11Hz2vun8G/cMrLzumTsKVry/7G/Q6gyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIjYuCugd1/2ldeder9T0/lTz9zbT3LjOQPvoe/I6gyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIgY2xXQMzXpPnVn/ZVnvvFb6O1z6LE6AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuwKuGDSfeqsgGdTpxA8W3ndqdMAntkz8M9ZnQERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFjuwJunHXed81nTthPfRpn/jamdl/s8z7yqlZYnQERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARE/33Zn/TNn96ce++zMaz7zs1oxdZ5Dj9UZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQ8fvz+UxfwzVWZqy/bbZ73/s9c7J/n94d/fexOgMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLGdgWYsL/9/vf7ptWnrvnbdhS8tp1RMMXqDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiFjaFbBvWn1qmvnMGfobp9V7+xx6v/ZnN16z1RkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRCx8ayAb5tlX3nmfc685jP3dfS+o9fQM099klZnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAxJVnBUxd1ZSpT2OfM2f3p67qzNMApqy8X6szIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMg4mffU984j37m3fFXHnvjHd9vnIP/th0F7yN/V1ZnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAxNJZAfv0ZqzPnL+f+hb2TeffuNvkzNMt3ke+7jOrMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIOLKswKmpvOn9gw8O/N17YI4/7FTnBUA8Df8swlEyBkQIWdAhJwBEXIGRMgZECFnQIScARFLZwVM3eP8zPvBP5v6NM68D33vs9rnzH0sz6b+uq3OgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6AiCvPCjhzTnpqOv/M2f0VZ+4YsRvhT3FWAMDf8M8mECFnQIScARFyBkTIGRAhZ0CEnAERcgZELJ0VsOLMcwbOvLf6mde8Yt9OhjN3BUx5D+29mXpmqzMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIiQMyBiaVfAjXepP3Pu/9mN5yqc+Tnf+P2euRvhPbRv55nVGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZEPGz8uCpmfJvmwvvmZp03/cdnTkl/xr6G5z6tVudARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEUtnBdw4kbzPmfe/n9ojsc+Nv43e7+rM17U6AyLkDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIpbOCvi2afV9Jxjs07sffO+u/Pu8jpz738fqDIiQMyBCzoAIOQMi5AyIkDMgQs6ACDkDIuQMiNh4VsA+U7sR9s1Yn7ln4NnU/P2Kfdc8dTJGbyfDCqszIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIkDMg4tBdAWfO7n/bxPmKM2fKpz6Nb/us3kPvyOoMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIOHRXwNRsd2/C/sz9FTdOnO9z49kXr6G/wWdWZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQMTP1AvvmzifmhqfmpJ/dua5ClPf0Zkz9Gfuc3gduWfgmdUZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQsfGsgKnJ4BW9yf599s2yT83Q3zj37zyH/2d1BkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRCydFXDjHdDPPMHg+XWn7tp+5jd446/uzN/V+/GxN+5ksDoDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMiNp4VcOMd0M+cKb/xTIapT/LGkxN63+Br6K/M6gyIkDMgQs6ACDkDIuQMiJAzIELOgAg5AyLkDIg4dFfAmaZmnXtnBex7R1PT+TfO0L+27UaY+gatzoAIOQMi5AyIkDMgQs6ACDkDIuQMiJAzIELOgIiflQefeY/zFVOz3Wc+9szZ/X1T8jfO30/tKHhv24uywuoMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIWNoV8GzfRPKKM++df+aegX2f5Jl35b9xDv7Mv7L30GdldQZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkRs3BXwbN9k8NSc9Jn3+/+2efSp/Qb79io4keOfszoDIuQMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMixnYF3OjMe/bvm0efuiv/t+0JeXbmfpLXtve7wuoMiJAzIELOgAg5AyLkDIiQMyBCzoAIOQMi5AyIsCvgj9k3Bz81gT11nsOZE+fPpubv9z32feRuk2dWZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQMTYroAzZ7tvnGVfed0bv4Ub9zn0TgN45qwAgCX+2QQi5AyIkDMgQs6ACDkDIuQMiJAzIELOgIifGyewzzQ1CT31ut92H/pv24vyunBHgdUZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQ8fvz+UxfA8AfYHUGRMgZECFnQIScARFyBkTIGRAhZ0CEnAERcgZEyBkQIWdAhJwBEXIGRMgZECFnQIScARFyBkTIGRAhZ8Cvhv8BAiLTIq8w3k8AAAAASUVORK5CYII=",
    "tags": [
      "Culinary Heritage",
      "Massive Shade",
      "Carbon Sink"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-011",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 15.8,
        "dbh_cm": 70.2,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Tamarind Tree. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-011",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 16.9,
        "dbh_cm": 74.1,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.1m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-011",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 18.0,
        "dbh_cm": 78.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-012",
    "common_name": "Rain Tree (Thoongu Moonji)",
    "scientific_name": "Samanea saman",
    "family": "Fabaceae",
    "iucn_status": "Least Concern",
    "native_region": "Tropical Flora Naturalized in Western Ghats",
    "medicinal_uses": "Broad parasol umbrella canopy cooling, nitrogen-enriching fallen leaflets, microclimate buffer.",
    "location": {
      "latitude": 10.99478,
      "longitude": 76.77435,
      "altitude_m": 485.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-III: Sports Complex Buffer",
      "landmarks": "Perimeter Boulevard along the Main Athletics Ground"
    },
    "biometrics": {
      "height_m": 21.0,
      "dbh_cm": 110.0,
      "crown_spread_m2": 290.0,
      "estimated_age_years": 36,
      "carbon_sequestered_kg": 17474.47,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "1990-07-15",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-012",
    "qr_code_base64": "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",
    "tags": [
      "Umbrella Canopy",
      "Thermal Regulator",
      "Campus Landmark"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-012",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 18.5,
        "dbh_cm": 99.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Rain Tree (Thoongu Moonji). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-012",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 19.7,
        "dbh_cm": 104.5,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+1.2m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-012",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 21.0,
        "dbh_cm": 110.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-013",
    "common_name": "Indian Gooseberry (Amla)",
    "scientific_name": "Phyllanthus emblica",
    "family": "Phyllanthaceae",
    "iucn_status": "Least Concern",
    "native_region": "Western Ghats Deciduous & Riparian Ecosystems",
    "medicinal_uses": "Ascorbic acid (Vitamin C) powerhouse, Ayurvedic Rasayana, immunological rejuvenating agent.",
    "location": {
      "latitude": 10.99622,
      "longitude": 76.77282,
      "altitude_m": 486.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-I: Academic Quadrant",
      "landmarks": "CIET Ayush & Medicinal Herbal Garden Plot #3"
    },
    "biometrics": {
      "height_m": 8.5,
      "dbh_cm": 26.0,
      "crown_spread_m2": 28.0,
      "estimated_age_years": 16,
      "carbon_sequestered_kg": 432.77,
      "health_status": "Healthy",
      "canopy_condition": "Fruiting"
    },
    "planted_date": "2010-09-05",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-013",
    "qr_code_base64": "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",
    "tags": [
      "Medicinal",
      "Vitamin C",
      "Ayurvedic"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-013",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 7.5,
        "dbh_cm": 23.4,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Indian Gooseberry (Amla). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-013",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 8.0,
        "dbh_cm": 24.7,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.5m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-013",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 8.5,
        "dbh_cm": 26.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-014",
    "common_name": "Gulmohar (Royal Poinciana)",
    "scientific_name": "Delonix regia",
    "family": "Fabaceae",
    "iucn_status": "Least Concern",
    "native_region": "Madagascar / Widely Naturalized across Tamil Nadu",
    "medicinal_uses": "Flavonoid-rich blooms, ornamental boulevard canopy, campus micro-ecosystem shelter.",
    "location": {
      "latitude": 10.99582,
      "longitude": 76.77372,
      "altitude_m": 486.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-I: Academic Quadrant",
      "landmarks": "Main Gate Avenue Entrance Driveway"
    },
    "biometrics": {
      "height_m": 12.8,
      "dbh_cm": 48.0,
      "crown_spread_m2": 85.0,
      "estimated_age_years": 24,
      "carbon_sequestered_kg": 2135.7,
      "health_status": "Healthy",
      "canopy_condition": "Flowering"
    },
    "planted_date": "2002-05-18",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-014",
    "qr_code_base64": "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",
    "tags": [
      "Ornamental",
      "Avenue Tree",
      "Campus Aesthetic"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-014",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 11.3,
        "dbh_cm": 43.2,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Gulmohar (Royal Poinciana). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-014",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 12.0,
        "dbh_cm": 45.6,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.7m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-014",
        "inspection_date": "2026-09-20",
        "health_status": "Healthy",
        "height_m": 12.8,
        "dbh_cm": 48.0,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-015",
    "common_name": "Cannonball Tree (Nagalingam)",
    "scientific_name": "Couroupita guianensis",
    "family": "Lecythidaceae",
    "iucn_status": "Least Concern",
    "native_region": "Tropical Botanical Collections / Sacred Groves of Tamil Nadu",
    "medicinal_uses": "Antiseptic floral extracts, sacred botanical grove emblem, unique cauliflorous flowering.",
    "location": {
      "latitude": 10.99585,
      "longitude": 76.77258,
      "altitude_m": 485.5,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-II: Botanical Reserve",
      "landmarks": "Temple & Meditation Garden Grove"
    },
    "biometrics": {
      "height_m": 16.0,
      "dbh_cm": 52.0,
      "crown_spread_m2": 65.0,
      "estimated_age_years": 27,
      "carbon_sequestered_kg": 3104.41,
      "health_status": "Vigorous",
      "canopy_condition": "Flowering"
    },
    "planted_date": "1999-01-26",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-015",
    "qr_code_base64": "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",
    "tags": [
      "Sacred Grove",
      "Rare Flowers",
      "Botanical Heritage"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-015",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 14.1,
        "dbh_cm": 46.8,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Cannonball Tree (Nagalingam). Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-015",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 15.0,
        "dbh_cm": 49.4,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.9m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-015",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 16.0,
        "dbh_cm": 52.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  },
  {
    "tree_id": "CIET-TREE-016",
    "common_name": "Indian Sandalwood",
    "scientific_name": "Santalum album",
    "family": "Santalaceae",
    "iucn_status": "Vulnerable",
    "native_region": "Southern Western Ghats & Eastern Ghats Endemic",
    "medicinal_uses": "Santalol essential oils, cooling skin therapeutics, precious aromatic corewood.",
    "location": {
      "latitude": 10.9964,
      "longitude": 76.77265,
      "altitude_m": 487.0,
      "gps_accuracy_m": 0.8,
      "campus_sector": "Sector-II: Botanical Reserve",
      "landmarks": "High-Security Rare Flora Nursery Bed #2"
    },
    "biometrics": {
      "height_m": 9.4,
      "dbh_cm": 30.5,
      "crown_spread_m2": 24.0,
      "estimated_age_years": 18,
      "carbon_sequestered_kg": 652.0,
      "health_status": "Vigorous",
      "canopy_condition": "Full Foliage"
    },
    "planted_date": "2008-08-15",
    "last_inspected": "2026-09-20",
    "inspector": "CIET Center for Forestry Informatics",
    "qr_code_url": "http://localhost:8000/tree/CIET-TREE-016",
    "qr_code_base64": "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",
    "tags": [
      "Vulnerable IUCN",
      "Aromatic",
      "High Conservation Value"
    ],
    "inspections": [
      {
        "inspection_id": "INS-2024-016",
        "inspection_date": "2024-09-12",
        "health_status": "Healthy",
        "height_m": 8.3,
        "dbh_cm": 27.4,
        "leaf_condition": "Good",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Baseline campus inventory audit for Indian Sandalwood. Stable root flare.",
        "inspected_by": "CIET Forestry Division (Field Team Alpha)",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2025-016",
        "inspection_date": "2025-09-18",
        "health_status": "Healthy",
        "height_m": 8.8,
        "dbh_cm": 29.0,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Annual growth increment recorded (+0.5m height). Canopy expansion healthy.",
        "inspected_by": "CIET Center for Forestry Informatics",
        "photo_url": null
      },
      {
        "inspection_id": "INS-2026-016",
        "inspection_date": "2026-09-20",
        "health_status": "Vigorous",
        "height_m": 9.4,
        "dbh_cm": 30.5,
        "leaf_condition": "Vigorous",
        "trunk_condition": "Sound",
        "pest_signs": "None observed",
        "stress_signs": "None",
        "observations": "Current biometric evaluation. Total CO2 biomass sequestration certified.",
        "inspected_by": "CIET Arid Forest Research Division",
        "photo_url": null
      }
    ]
  }
]''';

  static List<TreeProfile> getTrees() {
    final List<dynamic> data = jsonDecode(rawJson);
    return data.map((e) => TreeProfile.fromJson(e as Map<String, dynamic>)).toList();
  }
}
