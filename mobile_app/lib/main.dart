import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'screens/home_navigation_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(const CietTreeStockingApp());
}

class CietTreeStockingApp extends StatelessWidget {
  const CietTreeStockingApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CIET Trees',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF064E3B),
          primary: const Color(0xFF064E3B),
          secondary: const Color(0xFF10B981),
          surface: Colors.white,
          background: const Color(0xFFF8FAFC),
        ),
        appBarTheme: const AppBarTheme(
          centerTitle: false,
          elevation: 0,
          systemOverlayStyle: SystemUiOverlayStyle.light,
        ),
      ),
      home: const HomeNavigationScreen(),
    );
  }
}
