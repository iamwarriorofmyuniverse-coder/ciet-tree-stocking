import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../models/campus_landmark.dart';
import '../models/tree_model.dart';
import '../services/api_service.dart';
import 'tree_detail_screen.dart';

class CampusMapScreen extends StatefulWidget {
  const CampusMapScreen({super.key});

  @override
  State<CampusMapScreen> createState() => _CampusMapScreenState();
}

class _CampusMapScreenState extends State<CampusMapScreen> {
  final MapController _mapController = MapController();
  final ApiService _api = ApiService();

  List<TreeProfile> _trees = [];
  bool _loading = true;
  bool _showLandmarks = true;

  static const LatLng cietCenter = LatLng(10.995556, 76.773333);

  static const List<LatLng> cietBoundary = [
    LatLng(10.99720, 76.77180),
    LatLng(10.99705, 76.77490),
    LatLng(10.99460, 76.77510),
    LatLng(10.99380, 76.77440),
    LatLng(10.99410, 76.77190),
    LatLng(10.99560, 76.77160),
  ];

  @override
  void initState() {
    super.initState();
    _loadTrees();
  }

  Future<void> _loadTrees() async {
    setState(() => _loading = true);
    final list = await _api.getTrees();
    setState(() {
      _trees = list;
      _loading = false;
    });
  }

  Color _getTreeColor(String status) {
    switch (status.toLowerCase()) {
      case 'endangered':
        return Colors.red.shade600;
      case 'vulnerable':
        return Colors.amber.shade700;
      default:
        return const Color(0xFF10B981);
    }
  }

  void _showLandmarkSheet(CampusLandmark landmark) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) {
        return Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                landmark.name,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(
                landmark.category.toUpperCase(),
                style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.blue),
              ),
              const SizedBox(height: 8),
              Text(landmark.description, style: const TextStyle(fontSize: 12, color: Colors.grey)),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: const Color(0xFFECFDF5),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFFA7F3D0)),
                ),
                child: Text(
                  '🌿 Nearby Trees: ${landmark.nearbyTrees}',
                  style: const TextStyle(fontSize: 11, color: Color(0xFF047857), fontWeight: FontWeight.w600),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _showServerSettingsDialog() async {
    final currentUrl = await _api.getBaseUrl();
    final controller = TextEditingController(text: currentUrl);

    if (!mounted) return;
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.dns, color: Color(0xFF059669)),
            SizedBox(width: 8),
            Text('Server Connection', style: TextStyle(fontSize: 16)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Enter CIET Backend URL (Cloudflare Tunnel, Local LAN IP, or ngrok):',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: controller,
              style: const TextStyle(fontSize: 12, fontFamily: 'monospace'),
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'https://...',
                isDense: true,
              ),
            ),
            const SizedBox(height: 8),
            TextButton.icon(
              icon: const Icon(Icons.restore, size: 14),
              label: const Text('Reset to Default', style: TextStyle(fontSize: 11)),
              onPressed: () {
                controller.text = ApiService.defaultBaseUrl;
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF064E3B), foregroundColor: Colors.white),
            onPressed: () async {
              await _api.setCustomBaseUrl(controller.text);
              if (mounted) {
                Navigator.pop(ctx);
                _loadTrees();
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Server endpoint updated! Reconnecting...')),
                );
              }
            },
            child: const Text('Save & Reconnect'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CIET Campus GPS Map', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF064E3B),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: 'Server Connection',
            onPressed: _showServerSettingsDialog,
          ),
          IconButton(
            icon: Icon(_showLandmarks ? Icons.business : Icons.business_outlined),
            tooltip: 'Toggle Campus Buildings',
            onPressed: () => setState(() => _showLandmarks = !_showLandmarks),
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Reload Trees',
            onPressed: _loadTrees,
          ),
        ],
      ),
      body: Stack(
        children: [
          FlutterMap(
            mapController: _mapController,
            options: const MapOptions(
              initialCenter: cietCenter,
              initialZoom: 17.0,
              maxZoom: 19.0,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'in.edu.ciet.treestocking',
              ),

              // CIET 26.5-Acre Cadastral Boundary Polygon
              PolygonLayer(
                polygons: [
                  Polygon(
                    points: cietBoundary,
                    color: const Color(0x1A10B981),
                    borderColor: const Color(0xFF10B981),
                    borderStrokeWidth: 2.0,
                    isDotted: true,
                  ),
                ],
              ),

              // Tree Circle Markers
              MarkerLayer(
                markers: _trees.map((t) {
                  final color = _getTreeColor(t.iucnStatus);
                  return Marker(
                    point: LatLng(t.location.latitude, t.location.longitude),
                    width: 36,
                    height: 36,
                    child: GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => TreeDetailScreen(tree: t)),
                        );
                      },
                      child: Container(
                        decoration: BoxDecoration(
                          color: color,
                          shape: BoxShape.circle,
                          border: Border.all(color: Colors.white, width: 2),
                          boxShadow: const [
                            BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(0, 2))
                          ],
                        ),
                        child: const Icon(Icons.park, color: Colors.white, size: 18),
                      ),
                    ),
                  );
                }).toList(),
              ),

              // Campus Landmarks Markers
              if (_showLandmarks)
                MarkerLayer(
                  markers: CampusLandmark.cietLandmarks.map((lm) {
                    return Marker(
                      point: LatLng(lm.latitude, lm.longitude),
                      width: 32,
                      height: 32,
                      child: GestureDetector(
                        onTap: () => _showLandmarkSheet(lm),
                        child: Container(
                          decoration: BoxDecoration(
                            color: const Color(0xFF2563EB),
                            borderRadius: BorderRadius.circular(6),
                            border: Border.all(color: Colors.white, width: 1.5),
                            boxShadow: const [
                              BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(0, 2))
                            ],
                          ),
                          child: Center(
                            child: Text(
                              lm.iconCode,
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 10,
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
            ],
          ),

          if (_loading)
            const Positioned(
              top: 10,
              right: 10,
              child: Card(
                child: Padding(
                  padding: EdgeInsets.all(8),
                  child: SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2)),
                ),
              ),
            ),

          // Floating Quick Navigation Pills at Bottom
          Positioned(
            bottom: 20,
            left: 10,
            right: 10,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _navPill('Sector-I (Academic)', const LatLng(10.9994, 76.9042)),
                  const SizedBox(width: 6),
                  _navPill('Sector-II (Botanical)', const LatLng(10.9989, 76.9045)),
                  const SizedBox(width: 6),
                  _navPill('Sector-III (Sports)', const LatLng(10.9997, 76.9059)),
                  const SizedBox(width: 6),
                  _navPill('Sector-IV (Eco-Corridor)', const LatLng(11.0005, 76.9051)),
                  const SizedBox(width: 6),
                  _navPill('Center Campus', cietCenter),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _navPill(String title, LatLng target) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF064E3B),
        elevation: 3,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      ),
      onPressed: () => _mapController.move(target, 17.5),
      child: Text(title, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
    );
  }
}
