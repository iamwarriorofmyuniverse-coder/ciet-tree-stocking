"""
Western Ghats Biodiversity Symbiosis & Faunal Support Quotient (FSQ) Engine.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).

Scientific Focus:
- Keystone ecological mutualisms connecting campus flora to Western Ghats avifauna and pollinators.
- Campus Shannon-Wiener Ecological Biodiversity Index (H').
- 12-Month Phenological Flowering & Frugivore Resource Calendar.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# Western Ghats Ecological Taxa Association Matrix
SPECIES_FAUNA_ASSOCIATIONS: Dict[str, Dict[str, Any]] = {
    "Azadirachta indica": {
        "tamil_name": "வேம்பு (Neem)",
        "keystone_rating": 88,
        "supported_avifauna": [
            {"common": "White-cheeked Barbet", "scientific": "Psilopogon viridis", "role": "Fruit forager & seed disperser"},
            {"common": "Red-vented Bulbul", "scientific": "Pycnonotus cafer", "role": "Canopy pest gleaner"},
            {"common": "Spotted Dove", "scientific": "Spilopelia chinensis", "role": "Sub-canopy nester"},
        ],
        "pollinators": ["Apis cerana indica (Indian Honeybee)", "Trigona iridipennis (Dammar Bee)", "Syrphid Hoverflies"],
        "flowering_months": ["Mar", "Apr", "May"],
        "fruiting_months": ["Jun", "Jul", "Aug"],
        "ecological_service": "Natural pesticide volatile emissions, mosquito deterrent, and nesting canopy.",
    },
    "Ficus religiosa": {
        "tamil_name": "அரசு (Peepal)",
        "keystone_rating": 98,
        "supported_avifauna": [
            {"common": "Malabar Pied Hornbill", "scientific": "Anthracoceros coronatus", "role": "Obligate keystone frugivore"},
            {"common": "Indian Grey Hornbill", "scientific": "Ocyceros birostris", "role": "Fig cavity nester & disperser"},
            {"common": "Asian Koel", "scientific": "Eudynamys scolopaceus", "role": "Fig seed consumer"},
            {"common": "Brown-headed Barbet", "scientific": "Psilopogon zeylanicus", "role": "Frugivore"},
        ],
        "pollinators": ["Blastophaga quadriceps (Specialized Fig Wasp)", "Apis dorsata (Giant Rock Bee)"],
        "flowering_months": ["All Season (Syconia)"],
        "fruiting_months": ["Feb", "Mar", "Apr", "May", "Oct", "Nov"],
        "ecological_service": "Apex Western Ghats keystone species; year-round starvation food resource for 28+ bird species.",
    },
    "Ficus benghalensis": {
        "tamil_name": "ஆல மரம் (Banyan)",
        "keystone_rating": 99,
        "supported_avifauna": [
            {"common": "Malabar Pied Hornbill", "scientific": "Anthracoceros coronatus", "role": "Apex frugivore"},
            {"common": "Coppersmith Barbet", "scientific": "Psilopogon haemacephalus", "role": "Fruit feeder"},
            {"common": "Rose-ringed Parakeet", "scientific": "Psittacula krameri", "role": "Canopy flock roosting"},
        ],
        "pollinators": ["Eupristina masoni (Obligate Fig Wasp)", "Megachiroptera (Fruit Bats)"],
        "flowering_months": ["All Season"],
        "fruiting_months": ["Mar", "Apr", "May", "Jun", "Jul"],
        "ecological_service": "Massive prop-root microhabitat hosting reptiles, predatory birds, and micro-mammals.",
    },
    "Tectona grandis": {
        "tamil_name": "தேக்கு (Teak)",
        "keystone_rating": 76,
        "supported_avifauna": [
            {"common": "Greater Coucal", "scientific": "Centropus sinensis", "role": "Caterpillar predator"},
            {"common": "Black Drongo", "scientific": "Dicrurus macrocercus", "role": "Aerial insectivore sally perch"},
        ],
        "pollinators": ["Xylocopa latipes (Carpenter Bee)", "Bombus (Bumblebees)"],
        "flowering_months": ["Jun", "Jul", "Aug", "Sep"],
        "fruiting_months": ["Nov", "Dec", "Jan"],
        "ecological_service": "High timber biomass and high perch vantage for insect-controlling raptors.",
    },
    "Pongamia pinnata": {
        "tamil_name": "புங்க மரம் (Indian Beech)",
        "keystone_rating": 89,
        "supported_avifauna": [
            {"common": "Purple-rumped Sunbird", "scientific": "Leptocoma zeylonica", "role": "Nectarivore pollinator"},
            {"common": "Lotta's Sunbird", "scientific": "Cinnyris lotenius", "role": "Nectar consumer"},
        ],
        "pollinators": ["Apis dorsata (Giant Rock Bee)", "Nomia bees", "Catopsilia butterflies"],
        "flowering_months": ["Apr", "May", "Jun"],
        "fruiting_months": ["Sep", "Oct", "Nov"],
        "ecological_service": "Nitrogen-fixing root nodules enrich campus soil; crucial nectar corridor in hot pre-monsoon.",
    },
    "Syzygium cumini": {
        "tamil_name": "நாவல் (Jamun)",
        "keystone_rating": 94,
        "supported_avifauna": [
            {"common": "Tickell's Blue Flycatcher", "scientific": "Cyornis tickelliae", "role": "Understory insect predator"},
            {"common": "Indian Golden Oriole", "scientific": "Oriolus kundoo", "role": "Berry feeder"},
            {"common": "White-eye", "scientific": "Zosterops palpebrosus", "role": "Foliage gleaner"},
        ],
        "pollinators": ["Apis cerana", "Melipona (Stingless bees)", "Fruit bats"],
        "flowering_months": ["Mar", "Apr", "May"],
        "fruiting_months": ["Jun", "Jul", "Aug"],
        "ecological_service": "High-sugar berry crops sustain monsoon bird migration across the Palakkad Gap corridor.",
    },
    "Delonix regia": {
        "tamil_name": "நெருப்புக்கொன்றை (Gulmohar)",
        "keystone_rating": 82,
        "supported_avifauna": [
            {"common": "Purple Sunbird", "scientific": "Cinnyris asiaticus", "role": "Nectarivore"},
            {"common": "Common Myna", "scientific": "Acridotheres tristis", "role": "Canopy nester"},
        ],
        "pollinators": ["Papilio demoleus (Lime Butterfly)", "Xylocopa carpenter bees", "Honeybees"],
        "flowering_months": ["Apr", "May", "Jun", "Jul"],
        "fruiting_months": ["Aug", "Sep", "Oct"],
        "ecological_service": "Hyper-dense scarlet nectar bloom supporting thousands of solitary and social pollinators.",
    },
}

DEFAULT_FAUNA = {
    "tamil_name": "வளாக மரம் (Campus Specimen)",
    "keystone_rating": 75,
    "supported_avifauna": [
        {"common": "Common Myna", "scientific": "Acridotheres tristis", "role": "Canopy nester"},
        {"common": "Black Drongo", "scientific": "Dicrurus macrocercus", "role": "Insect predator"},
    ],
    "pollinators": ["Apis cerana indica", "Local native pollinators"],
    "flowering_months": ["Mar", "Apr"],
    "fruiting_months": ["May", "Jun"],
    "ecological_service": "Campus soil conservation and shade canopy.",
}


class BiodiversityProfile(BaseModel):
    """Detailed Faunal and Ecological Mutualism Profile for an individual tree."""
    tree_id: str
    scientific_name: str
    tamil_name: str
    keystone_rating: int = Field(..., ge=0, le=100)
    supported_avifauna: List[Dict[str, str]]
    pollinators: List[str]
    flowering_months: List[str]
    fruiting_months: List[str]
    ecological_service: str


class CampusBiodiversitySummary(BaseModel):
    """Aggregate Ecological Health & Shannon-Wiener Diversity Score for CIET."""
    total_trees: int
    total_distinct_species: int
    shannon_wiener_index_h: float
    simpson_diversity_index_d: float
    campus_faunal_support_quotient_fsq: float
    keystone_species_count: int
    nilgiri_biosphere_connectivity_rating: str = "High Western Ghats Foothill Integration"
    profiles: List[BiodiversityProfile]


def compute_campus_biodiversity(trees: List[Dict[str, Any]]) -> CampusBiodiversitySummary:
    """
    Computes Shannon-Wiener index, FSQ score, and faunal mutualisms for CIET campus.
    """
    total_trees = len(trees)
    if total_trees == 0:
        return CampusBiodiversitySummary(
            total_trees=0,
            total_distinct_species=0,
            shannon_wiener_index_h=0.0,
            simpson_diversity_index_d=0.0,
            campus_faunal_support_quotient_fsq=0.0,
            keystone_species_count=0,
            profiles=[],
        )

    species_counts: Dict[str, int] = {}
    profiles: List[BiodiversityProfile] = []
    keystone_count = 0
    fsq_sum = 0.0

    for t in trees:
        tree_id = t.get("tree_id", "CIET-TREE-001")
        sci_name = t.get("scientific_name", "Azadirachta indica")
        species_counts[sci_name] = species_counts.get(sci_name, 0) + 1

        info = SPECIES_FAUNA_ASSOCIATIONS.get(sci_name, DEFAULT_FAUNA)
        rating = info["keystone_rating"]
        fsq_sum += rating

        if rating >= 90:
            keystone_count += 1

        profiles.append(
            BiodiversityProfile(
                tree_id=tree_id,
                scientific_name=sci_name,
                tamil_name=info["tamil_name"],
                keystone_rating=rating,
                supported_avifauna=info["supported_avifauna"],
                pollinators=info["pollinators"],
                flowering_months=info["flowering_months"],
                fruiting_months=info["fruiting_months"],
                ecological_service=info["ecological_service"],
            )
        )

    # Shannon-Wiener Index: H' = - sum(pi * ln(pi))
    h_prime = 0.0
    simpson_d = 0.0
    for count in species_counts.values():
        p_i = count / total_trees
        if p_i > 0:
            h_prime -= p_i * math.log(p_i)
            simpson_d += p_i ** 2

    simpson_index = 1.0 - simpson_d
    mean_fsq = round(fsq_sum / total_trees, 1)

    return CampusBiodiversitySummary(
        total_trees=total_trees,
        total_distinct_species=len(species_counts),
        shannon_wiener_index_h=round(h_prime, 3),
        simpson_diversity_index_d=round(simpson_index, 3),
        campus_faunal_support_quotient_fsq=mean_fsq,
        keystone_species_count=keystone_count,
        profiles=profiles,
    )
