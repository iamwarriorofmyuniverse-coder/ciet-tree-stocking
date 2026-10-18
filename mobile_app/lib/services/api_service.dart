import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/tree_model.dart';

class ApiService {
  static const String defaultBaseUrl = 'https://qualifications-asylum-workers-counter.trycloudflare.com';
  final String baseUrl;

  ApiService({this.baseUrl = defaultBaseUrl});

  /// Fetches all registered trees with offline caching fallback.
  Future<List<TreeProfile>> getTrees() async {
    final prefs = await SharedPreferences.getInstance();

    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/trees'))
          .timeout(const Duration(seconds: 8));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        // Update offline cache
        await prefs.setString('cached_trees_json', response.body);
        return data.map((e) => TreeProfile.fromJson(e as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      // Offline fallback: load from cached device memory
      final cached = prefs.getString('cached_trees_json');
      if (cached != null) {
        final List<dynamic> data = jsonDecode(cached);
        return data.map((e) => TreeProfile.fromJson(e as Map<String, dynamic>)).toList();
      }
    }

    return [];
  }

  /// Fetches single tree profile by ID.
  Future<TreeProfile?> getTree(String treeId) async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/trees/$treeId'))
          .timeout(const Duration(seconds: 6));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return TreeProfile.fromJson(data as Map<String, dynamic>);
      }
    } catch (e) {
      // Fallback search in cached trees
      final trees = await getTrees();
      return trees.where((t) => t.treeId.toUpperCase() == treeId.toUpperCase()).firstOrNull;
    }
    return null;
  }

  /// Fetches macro carbon and forest metrics summary.
  Future<Map<String, dynamic>> getMetricsSummary() async {
    final prefs = await SharedPreferences.getInstance();

    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/metrics/summary'))
          .timeout(const Duration(seconds: 6));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        await prefs.setString('cached_metrics_json', response.body);
        return data;
      }
    } catch (e) {
      final cached = prefs.getString('cached_metrics_json');
      if (cached != null) {
        return jsonDecode(cached) as Map<String, dynamic>;
      }
    }

    return {
      'total_trees': 16,
      'total_carbon_sequestered_kg': 106706.09,
      'total_canopy_coverage_m2': 1847.0,
      'average_tree_age_years': 32.5,
    };
  }
}
