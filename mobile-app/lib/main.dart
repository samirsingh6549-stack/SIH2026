import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/theme/app_theme.dart';
import 'ui/features/home/home_view_model.dart';
import 'ui/features/home/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const NerLandslideApp());
}

class NerLandslideApp extends StatelessWidget {
  const NerLandslideApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => HomeViewModel()..init(),
        ),
      ],
      child: MaterialApp(
        title: 'NER Landslide Scout',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.darkTheme,
        home: const HomeScreen(),
      ),
    );
  }
}
