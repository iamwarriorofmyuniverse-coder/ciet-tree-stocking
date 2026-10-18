import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../services/api_service.dart';
import 'tree_detail_screen.dart';

class QrScannerScreen extends StatefulWidget {
  const QrScannerScreen({super.key});

  @override
  State<QrScannerScreen> createState() => _QrScannerScreenState();
}

class _QrScannerScreenState extends State<QrScannerScreen> {
  final MobileScannerController _controller = MobileScannerController();
  final ApiService _api = ApiService();
  bool _isProcessing = false;

  void _onDetect(BarcodeCapture capture) async {
    if (_isProcessing) return;
    final List<Barcode> barcodes = capture.barcodes;
    if (barcodes.isEmpty) return;

    final String? rawValue = barcodes.first.rawValue;
    if (rawValue == null || rawValue.isEmpty) return;

    setState(() => _isProcessing = true);

    // Extract tree_id from URL or raw tag (e.g. "CIET-TREE-002" or ".../tree/CIET-TREE-002")
    String treeId = rawValue.trim();
    if (treeId.contains('/tree/')) {
      treeId = treeId.split('/tree/').last.split('?').first.trim();
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Decoded QR: $treeId. Fetching biometric passport...'),
        duration: const Duration(seconds: 1),
      ),
    );

    final tree = await _api.getTree(treeId);

    if (mounted) {
      if (tree != null) {
        await Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => TreeDetailScreen(tree: tree)),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Specimen $treeId not found in local or remote database.'),
            backgroundColor: Colors.red.shade700,
          ),
        );
      }
      setState(() => _isProcessing = false);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('In-Field QR Scanner', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF064E3B),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.flash_on),
            onPressed: () => _controller.toggleTorch(),
          ),
          IconButton(
            icon: const Icon(Icons.flip_camera_ios),
            onPressed: () => _controller.switchCamera(),
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: _controller,
            onDetect: _onDetect,
          ),

          // Aiming Viewfinder Reticle
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(color: const Color(0xFF10B981), width: 3),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Align(
                alignment: Alignment.bottomCenter,
                child: Padding(
                  padding: EdgeInsets.only(bottom: 8),
                  child: Text(
                    'ALIGN TREE BARK TAG',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      backgroundColor: Colors.black45,
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Bottom Helper Instructions
          Positioned(
            bottom: 30,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.75),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.white24),
              ),
              child: const Text(
                'Point camera at any weatherproof CIET tree barcode tag. Scans instantly even in partial sunlight.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white70, fontSize: 12),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
