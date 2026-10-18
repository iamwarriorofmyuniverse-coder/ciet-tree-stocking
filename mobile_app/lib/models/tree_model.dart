import 'dart:convert';

class GeoLocation {
  final double latitude;
  final double longitude;
  final double altitudeM;
  final double gpsAccuracyM;
  final String campusSector;
  final String landmarks;

  const GeoLocation({
    required this.latitude,
    required this.longitude,
    this.altitudeM = 430.0,
    this.gpsAccuracyM = 0.8,
    required this.campusSector,
    this.landmarks = '',
  });

  factory GeoLocation.fromJson(Map<String, dynamic> json) {
    return GeoLocation(
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      altitudeM: (json['altitude_m'] as num?)?.toDouble() ?? 430.0,
      gpsAccuracyM: (json['gps_accuracy_m'] as num?)?.toDouble() ?? 0.8,
      campusSector: json['campus_sector'] as String? ?? 'Sector-I: Academic Quadrant',
      landmarks: json['landmarks'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'latitude': latitude,
    'longitude': longitude,
    'altitude_m': altitudeM,
    'gps_accuracy_m': gpsAccuracyM,
    'campus_sector': campusSector,
    'landmarks': landmarks,
  };

  String get googleMapsUrl => 'https://www.google.com/maps/dir/?api=1&destination=$latitude,$longitude';
  String get coordinatesFormatted => '${latitude.toStringAsFixed(6)}° N, ${longitude.toStringAsFixed(6)}° E';
}

class Biometrics {
  final double heightM;
  final double dbhCm;
  final double crownSpreadM2;
  final int estimatedAgeYears;
  final double carbonSequesteredKg;
  final String healthStatus;
  final String canopyCondition;

  const Biometrics({
    required this.heightM,
    required this.dbhCm,
    required this.crownSpreadM2,
    required this.estimatedAgeYears,
    required this.carbonSequesteredKg,
    this.healthStatus = 'Healthy',
    this.canopyCondition = 'Full Foliage',
  });

  factory Biometrics.fromJson(Map<String, dynamic> json) {
    return Biometrics(
      heightM: (json['height_m'] as num).toDouble(),
      dbhCm: (json['dbh_cm'] as num).toDouble(),
      crownSpreadM2: (json['crown_spread_m2'] as num).toDouble(),
      estimatedAgeYears: (json['estimated_age_years'] as num).toInt(),
      carbonSequesteredKg: (json['carbon_sequestered_kg'] as num).toDouble(),
      healthStatus: json['health_status'] as String? ?? 'Healthy',
      canopyCondition: json['canopy_condition'] as String? ?? 'Full Foliage',
    );
  }

  Map<String, dynamic> toJson() => {
    'height_m': heightM,
    'dbh_cm': dbhCm,
    'crown_spread_m2': crownSpreadM2,
    'estimated_age_years': estimatedAgeYears,
    'carbon_sequestered_kg': carbonSequesteredKg,
    'health_status': healthStatus,
    'canopy_condition': canopyCondition,
  };

  double get drivingDistanceOffsetKm => carbonSequesteredKg * 4.1;
}

class InspectionRecord {
  final String inspectionId;
  final String inspectionDate;
  final String healthStatus;
  final double heightM;
  final double dbhCm;
  final String leafCondition;
  final String trunkCondition;
  final String pestSigns;
  final String stressSigns;
  final String observations;
  final String inspectedBy;

  const InspectionRecord({
    required this.inspectionId,
    required this.inspectionDate,
    this.healthStatus = 'Healthy',
    required this.heightM,
    required this.dbhCm,
    this.leafCondition = 'Good',
    this.trunkCondition = 'Sound',
    this.pestSigns = 'None observed',
    this.stressSigns = 'None',
    this.observations = 'Healthy growth',
    this.inspectedBy = 'CIET Center for Forestry Informatics',
  });

  factory InspectionRecord.fromJson(Map<String, dynamic> json) {
    return InspectionRecord(
      inspectionId: json['inspection_id'] as String? ?? '',
      inspectionDate: json['inspection_date'] as String? ?? '',
      healthStatus: json['health_status'] as String? ?? 'Healthy',
      heightM: (json['height_m'] as num?)?.toDouble() ?? 0.0,
      dbhCm: (json['dbh_cm'] as num?)?.toDouble() ?? 0.0,
      leafCondition: json['leaf_condition'] as String? ?? 'Good',
      trunkCondition: json['trunk_condition'] as String? ?? 'Sound',
      pestSigns: json['pest_signs'] as String? ?? 'None observed',
      stressSigns: json['stress_signs'] as String? ?? 'None',
      observations: json['observations'] as String? ?? 'Healthy growth',
      inspectedBy: json['inspected_by'] as String? ?? 'CIET Center for Forestry Informatics',
    );
  }

  Map<String, dynamic> toJson() => {
    'inspection_id': inspectionId,
    'inspection_date': inspectionDate,
    'health_status': healthStatus,
    'height_m': heightM,
    'dbh_cm': dbhCm,
    'leaf_condition': leafCondition,
    'trunk_condition': trunkCondition,
    'pest_signs': pestSigns,
    'stress_signs': stressSigns,
    'observations': observations,
    'inspected_by': inspectedBy,
  };
}

class TreeProfile {
  final String treeId;
  final String commonName;
  final String scientificName;
  final String family;
  final String iucnStatus;
  final String nativeRegion;
  final String medicinalUses;
  final GeoLocation location;
  final Biometrics biometrics;
  final String plantedDate;
  final String lastInspected;
  final String inspector;
  final String qrCodeUrl;
  final String qrCodeBase64;
  final List<String> tags;
  final List<InspectionRecord> inspections;

  const TreeProfile({
    required this.treeId,
    required this.commonName,
    required this.scientificName,
    required this.family,
    required this.iucnStatus,
    required this.nativeRegion,
    required this.medicinalUses,
    required this.location,
    required this.biometrics,
    required this.plantedDate,
    required this.lastInspected,
    required this.inspector,
    required this.qrCodeUrl,
    required this.qrCodeBase64,
    required this.tags,
    this.inspections = const [],
  });

  factory TreeProfile.fromJson(Map<String, dynamic> json) {
    return TreeProfile(
      treeId: json['tree_id'] as String,
      commonName: json['common_name'] as String,
      scientificName: json['scientific_name'] as String,
      family: json['family'] as String,
      iucnStatus: json['iucn_status'] as String? ?? 'Least Concern',
      nativeRegion: json['native_region'] as String? ?? '',
      medicinalUses: json['medicinal_uses'] as String? ?? '',
      location: GeoLocation.fromJson(json['location'] as Map<String, dynamic>),
      biometrics: Biometrics.fromJson(json['biometrics'] as Map<String, dynamic>),
      plantedDate: json['planted_date'] as String? ?? '',
      lastInspected: json['last_inspected'] as String? ?? '',
      inspector: json['inspector'] as String? ?? 'CIET Center for Forestry Informatics',
      qrCodeUrl: json['qr_code_url'] as String? ?? '',
      qrCodeBase64: json['qr_code_base64'] as String? ?? '',
      tags: (json['tags'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
      inspections: (json['inspections'] as List<dynamic>?)
              ?.map((e) => InspectionRecord.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() => {
    'tree_id': treeId,
    'common_name': commonName,
    'scientific_name': scientificName,
    'family': family,
    'iucn_status': iucnStatus,
    'native_region': nativeRegion,
    'medicinal_uses': medicinalUses,
    'location': location.toJson(),
    'biometrics': biometrics.toJson(),
    'planted_date': plantedDate,
    'last_inspected': lastInspected,
    'inspector': inspector,
    'qr_code_url': qrCodeUrl,
    'qr_code_base64': qrCodeBase64,
    'tags': tags,
    'inspections': inspections.map((e) => e.toJson()).toList(),
  };
}
