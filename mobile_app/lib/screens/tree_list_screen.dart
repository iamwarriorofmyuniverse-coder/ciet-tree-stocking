import 'package:flutter/material.dart';
import '../models/tree_model.dart';
import '../services/api_service.dart';
import 'tree_detail_screen.dart';

class TreeListScreen extends StatefulWidget {
  const TreeListScreen({super.key});

  @override
  State<TreeListScreen> createState() => _TreeListScreenState();
}

class _TreeListScreenState extends State<TreeListScreen> {
  final ApiService _api = ApiService();
  List<TreeProfile> _allTrees = [];
  List<TreeProfile> _filteredTrees = [];
  String _searchQuery = '';
  String _selectedSector = 'All';
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchTrees();
  }

  Future<void> _fetchTrees() async {
    setState(() => _loading = true);
    final trees = await _api.getTrees();
    setState(() {
      _allTrees = trees;
      _filteredTrees = trees;
      _loading = false;
    });
  }

  void _applyFilter() {
    setState(() {
      _filteredTrees = _allTrees.where((t) {
        final matchesQuery = _searchQuery.isEmpty ||
            t.commonName.toLowerCase().contains(_searchQuery.toLowerCase()) ||
            t.scientificName.toLowerCase().contains(_searchQuery.toLowerCase()) ||
            t.treeId.toLowerCase().contains(_searchQuery.toLowerCase()) ||
            t.family.toLowerCase().contains(_searchQuery.toLowerCase());

        final matchesSector = _selectedSector == 'All' ||
            t.location.campusSector.toLowerCase().contains(_selectedSector.toLowerCase());

        return matchesQuery && matchesSector;
      }).toList();
    });
  }

  Color _getIucnColor(String status) {
    switch (status.toLowerCase()) {
      case 'endangered':
        return Colors.red.shade700;
      case 'vulnerable':
        return Colors.amber.shade800;
      case 'near threatened':
        return Colors.orange.shade700;
      default:
        return const Color(0xFF059669);
    }
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
                _fetchTrees();
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
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Tree Inventory Directory', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF064E3B),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: 'Server Connection',
            onPressed: _showServerSettingsDialog,
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Reload',
            onPressed: _fetchTrees,
          ),
        ],
      ),
      body: Column(
        children: [
          // Search & Filter Header
          Container(
            padding: const EdgeInsets.all(12),
            color: Colors.white,
            child: Column(
              children: [
                TextField(
                  onChanged: (val) {
                    _searchQuery = val;
                    _applyFilter();
                  },
                  decoration: InputDecoration(
                    hintText: 'Search species, tree ID, family...',
                    prefixIcon: const Icon(Icons.search, size: 20, color: Colors.grey),
                    filled: true,
                    fillColor: const Color(0xFFF1F5F9),
                    contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _filterChip('All'),
                      const SizedBox(width: 6),
                      _filterChip('Sector-I'),
                      const SizedBox(width: 6),
                      _filterChip('Sector-II'),
                      const SizedBox(width: 6),
                      _filterChip('Sector-III'),
                      const SizedBox(width: 6),
                      _filterChip('Sector-IV'),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Tree List
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : _filteredTrees.isEmpty
                    ? const Center(child: Text('No trees match the filter criteria.'))
                    : ListView.builder(
                        itemCount: _filteredTrees.length,
                        padding: const EdgeInsets.all(12),
                        itemBuilder: (context, index) {
                          final tree = _filteredTrees[index];
                          final iucnColor = _getIucnColor(tree.iucnStatus);

                          return Card(
                            margin: const EdgeInsets.only(bottom: 10),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(14),
                              side: BorderSide(color: Colors.grey.shade200),
                            ),
                            elevation: 0,
                            child: InkWell(
                              borderRadius: BorderRadius.circular(14),
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(builder: (_) => TreeDetailScreen(tree: tree)),
                                );
                              },
                              child: Padding(
                                padding: const EdgeInsets.all(14),
                                child: Row(
                                  children: [
                                    Container(
                                      width: 44,
                                      height: 44,
                                      decoration: BoxDecoration(
                                        color: const Color(0xFFECFDF5),
                                        borderRadius: BorderRadius.circular(10),
                                        border: Border.all(color: const Color(0xFFA7F3D0)),
                                      ),
                                      child: const Icon(Icons.park, color: Color(0xFF059669)),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Row(
                                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                            children: [
                                              Text(
                                                tree.treeId,
                                                style: const TextStyle(
                                                  fontFamily: 'monospace',
                                                  fontSize: 11,
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.blueGrey,
                                                ),
                                              ),
                                              Container(
                                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                                decoration: BoxDecoration(
                                                  color: iucnColor.withOpacity(0.12),
                                                  borderRadius: BorderRadius.circular(6),
                                                ),
                                                child: Text(
                                                  tree.iucnStatus,
                                                  style: TextStyle(
                                                    color: iucnColor,
                                                    fontSize: 9,
                                                    fontWeight: FontWeight.bold,
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                          const SizedBox(height: 2),
                                          Text(
                                            tree.commonName,
                                            style: const TextStyle(
                                              fontSize: 14,
                                              fontWeight: FontWeight.bold,
                                              color: Color(0xFF0F172A),
                                            ),
                                          ),
                                          Text(
                                            '${tree.scientificName} • ${tree.location.campusSector.split(":").first}',
                                            style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                          ),
                                          const SizedBox(height: 4),
                                          Text(
                                            'CO₂: ${tree.biometrics.carbonSequesteredKg.toStringAsFixed(0)} kg | Age: ${tree.biometrics.estimatedAgeYears} yrs',
                                            style: const TextStyle(
                                              fontSize: 10,
                                              fontWeight: FontWeight.w600,
                                              color: Color(0xFF047857),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                    const Icon(Icons.chevron_right, color: Colors.grey, size: 20),
                                  ],
                                ),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }

  Widget _filterChip(String sector) {
    final isSelected = _selectedSector == sector;
    return ChoiceChip(
      label: Text(sector, style: TextStyle(fontSize: 10, color: isSelected ? Colors.white : Colors.black87)),
      selected: isSelected,
      selectedColor: const Color(0xFF064E3B),
      backgroundColor: const Color(0xFFF1F5F9),
      onSelected: (_) {
        setState(() {
          _selectedSector = sector;
          _applyFilter();
        });
      },
    );
  }
}
