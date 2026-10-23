import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/tree_model.dart';
import 'offline_seed.dart';

class ApiService {
  static const String defaultBaseUrl = 'https://unions-punch-bundle-chicken.trycloudflare.com';
  String? _explicitBaseUrl;

  ApiService({String? baseUrl}) : _explicitBaseUrl = baseUrl;

  Future<String> getBaseUrl() async {
    if (_explicitBaseUrl != null && _explicitBaseUrl!.isNotEmpty) {
      return _explicitBaseUrl!;
    }
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('custom_base_url') ?? defaultBaseUrl;
  }

  Future<void> setCustomBaseUrl(String newUrl) async {
    final prefs = await SharedPreferences.getInstance();
    final cleanUrl = newUrl.trim().replaceAll(RegExp(r'/+$'), '');
    await prefs.setString('custom_base_url', cleanUrl);
    _explicitBaseUrl = cleanUrl;
  }

  /// Fetches all registered trees with offline caching and seed data fallback.
  Future<List<TreeProfile>> getTrees() async {
    final prefs = await SharedPreferences.getInstance();
    final baseUrl = await getBaseUrl();

    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/trees'))
          .timeout(const Duration(seconds: 6));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        // Update offline cache
        await prefs.setString('cached_trees_json', response.body);
        return data.map((e) => TreeProfile.fromJson(e as Map<String, dynamic>)).toList();
      }
    } catch (_) {
      // Offline fallback: load from cached device memory
      final cached = prefs.getString('cached_trees_json');
      if (cached != null) {
        try {
          final List<dynamic> data = jsonDecode(cached);
          final list = data.map((e) => TreeProfile.fromJson(e as Map<String, dynamic>)).toList();
          if (list.isNotEmpty) return list;
        } catch (_) {}
      }
    }

    // Secondary fallback: Return pre-compiled authentic CIET seed data
    return OfflineSeed.getTrees();
  }

  /// Fetches single tree profile by ID.
  Future<TreeProfile?> getTree(String treeId) async {
    final baseUrl = await getBaseUrl();

    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/trees/$treeId'))
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return TreeProfile.fromJson(data as Map<String, dynamic>);
      }
    } catch (_) {
      // Fallback search in cached trees / offline seed
      final trees = await getTrees();
      return trees.where((t) => t.treeId.toUpperCase() == treeId.toUpperCase()).firstOrNull;
    }
    return null;
  }

  /// Fetches macro carbon and forest metrics summary.
  Future<Map<String, dynamic>> getMetricsSummary() async {
    final prefs = await SharedPreferences.getInstance();
    final baseUrl = await getBaseUrl();

    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/metrics/summary'))
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        await prefs.setString('cached_metrics_json', response.body);
        return data;
      }
    } catch (_) {
      final cached = prefs.getString('cached_metrics_json');
      if (cached != null) {
        try {
          return jsonDecode(cached) as Map<String, dynamic>;
        } catch (_) {}
      }
    }

    final trees = OfflineSeed.getTrees();
    final totalCarbon = trees.fold<double>(0.0, (sum, t) => sum + t.biometrics.carbonSequesteredKg);
    final totalCanopy = trees.fold<double>(0.0, (sum, t) => sum + t.biometrics.crownSpreadM2);
    final avgAge = trees.fold<int>(0, (sum, t) => sum + t.biometrics.estimatedAgeYears) / (trees.isNotEmpty ? trees.length : 1);

    return {
      'total_trees': trees.length,
      'total_carbon_sequestered_kg': double.parse(totalCarbon.toStringAsFixed(2)),
      'total_canopy_coverage_m2': double.parse(totalCanopy.toStringAsFixed(2)),
      'average_tree_age_years': double.parse(avgAge.toStringAsFixed(1)),
    };
  }
}
