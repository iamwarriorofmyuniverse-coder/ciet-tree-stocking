class CampusLandmark {
  final String name;
  final String category;
  final double latitude;
  final double longitude;
  final String iconCode;
  final String description;
  final String nearbyTrees;

  const CampusLandmark({
    required this.name,
    required this.category,
    required this.latitude,
    required this.longitude,
    required this.iconCode,
    required this.description,
    required this.nearbyTrees,
  });

  static const List<CampusLandmark> cietLandmarks = [
    CampusLandmark(
      name: 'Main Administrative Block (A-Block)',
      category: 'Administration',
      latitude: 10.99568,
      longitude: 76.77315,
      iconCode: 'A',
      description: "Principal's Office, Academic Deanery, Admissions & Boardroom.",
      nearbyTrees: 'CIET-TREE-001 (Neem)',
    ),
    CampusLandmark(
      name: 'Dept. of AI & Data Science (CoE)',
      category: 'Research',
      latitude: 10.99585,
      longitude: 76.77330,
      iconCode: 'AI',
      description: 'High-Performance GPU Clusters, Forestry Computer Vision Labs.',
      nearbyTrees: 'CIET-TREE-009 (Pongamia), CIET-TREE-014 (Gulmohar)',
    ),
    CampusLandmark(
      name: 'Central Library & Digital Knowledge Hub',
      category: 'Academic',
      latitude: 10.99540,
      longitude: 76.77295,
      iconCode: 'LIB',
      description: '55,000+ volumes, IEEE/Springer digital access & quiet reading suites.',
      nearbyTrees: 'CIET-TREE-003 (Sacred Fig)',
    ),
    CampusLandmark(
      name: 'Mechanical & Civil Innovation Hub',
      category: 'Laboratories',
      latitude: 10.99615,
      longitude: 76.77365,
      iconCode: 'M&C',
      description: 'Heavy Machinery, CNC/CAD/CAM, Material Testing & Surveying Labs.',
      nearbyTrees: 'CIET-TREE-009 (Pongamia)',
    ),
    CampusLandmark(
      name: 'CIET Central Auditorium & Quadrangle',
      category: 'Auditorium',
      latitude: 10.99515,
      longitude: 76.77355,
      iconCode: 'AUD',
      description: '1,500-seat multi-tier acoustic convention hall & amphitheater.',
      nearbyTrees: 'CIET-TREE-002 (Heritage Banyan - 75 Yrs)',
    ),
    CampusLandmark(
      name: 'Student Amenities & Food Court',
      category: 'Dining',
      latitude: 10.99530,
      longitude: 76.77265,
      iconCode: 'FC',
      description: 'Multi-cuisine dining hall, cooperative store & student lawn.',
      nearbyTrees: 'CIET-TREE-011 (Tamarind Tree)',
    ),
    CampusLandmark(
      name: 'CIET Athletics Stadium & Sports Arena',
      category: 'Sports',
      latitude: 10.99475,
      longitude: 76.77440,
      iconCode: 'SPT',
      description: '400m running track, football stadium, cricket turf wickets.',
      nearbyTrees: 'CIET-TREE-012 (Giant Rain Tree - 290m²)',
    ),
    CampusLandmark(
      name: 'Ayush Herbal Garden & Botanical Reserve',
      category: 'Botanical',
      latitude: 10.99595,
      longitude: 76.77235,
      iconCode: 'BOT',
      description: 'Medicinal plants cultivation & Western Ghats endangered taxa.',
      nearbyTrees: 'CIET-TREE-005 (Red Sandalwood), CIET-TREE-013 (Amla), CIET-TREE-016 (Sandalwood)',
    ),
    CampusLandmark(
      name: 'Campus Temple & Meditation Grove',
      category: 'Heritage',
      latitude: 10.99505,
      longitude: 76.77335,
      iconCode: 'TMP',
      description: 'Sacred Nagalingam trees and serene contemplation flora.',
      nearbyTrees: 'CIET-TREE-015 (Nagalingam / Cannonball)',
    ),
    CampusLandmark(
      name: 'Rainwater Eco-Pond & Swale Basin',
      category: 'Hydrology',
      latitude: 10.99445,
      longitude: 76.77380,
      iconCode: 'H2O',
      description: 'Natural aquifer recharge catchment and riparian bird wetland.',
      nearbyTrees: 'CIET-TREE-008 (Arjun), CIET-TREE-007 (Jamun)',
    ),
    CampusLandmark(
      name: 'Western Ghats Eco-Corridor & Hillside',
      category: 'Conservation',
      latitude: 10.99665,
      longitude: 76.77370,
      iconCode: 'ECO',
      description: 'Native timber buffer connecting campus to Velliangiri foothills.',
      nearbyTrees: 'CIET-TREE-004 (Rosewood), CIET-TREE-006 (Teak), CIET-TREE-010 (Mahua)',
    ),
    CampusLandmark(
      name: 'Student Residential Hostels Complex',
      category: 'Residential',
      latitude: 10.99450,
      longitude: 76.77250,
      iconCode: 'HST',
      description: 'Eco-friendly hostel blocks with solar heating & green lawns.',
      nearbyTrees: 'CIET-TREE-007 (Jamun), CIET-TREE-012 (Rain Tree)',
    ),
  ];
}
