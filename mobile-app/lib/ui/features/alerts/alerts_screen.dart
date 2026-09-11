import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/i18n/dialect_translations.dart';
import 'alerts_view_model.dart';
import '../../shared_widgets/status_badge.dart';

class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AlertsViewModel()..loadAlerts(),
      child: Consumer<AlertsViewModel>(
        builder: (context, vm, _) {
          return Scaffold(
            appBar: AppBar(
              title: const Text('Disaster Warnings & Advisories'),
              actions: [
                IconButton(
                  icon: const Icon(Icons.refresh),
                  onPressed: () => vm.loadAlerts(language: vm.currentLanguage),
                ),
              ],
            ),
            body: Column(
              children: [
                // Horizontal Dialect Selector Bar
                Container(
                  height: 48,
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  color: AppColors.surface,
                  child: ListView.separated(
                    scrollDirection: Axis.horizontal,
                    itemCount: DialectTranslations.supportedLanguages.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 8),
                    itemBuilder: (context, idx) {
                      final item = DialectTranslations.supportedLanguages[idx];
                      final isSelected = item['code'] == vm.currentLanguage;

                      return ChoiceChip(
                        label: Text(
                          item['native']!,
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                            color: isSelected ? Colors.black : AppColors.textPrimary,
                          ),
                        ),
                        selected: isSelected,
                        selectedColor: AppColors.primary,
                        backgroundColor: AppColors.surfaceElevated,
                        onSelected: (_) => vm.switchLanguage(item['code']!),
                      );
                    },
                  ),
                ),

                Expanded(
                  child: vm.isLoading
                      ? const Center(child: CircularProgressIndicator())
                      : vm.alerts.isEmpty
                          ? const Center(child: Text('No active advisories for this region.'))
                          : ListView.separated(
                              padding: const EdgeInsets.all(16),
                              itemCount: vm.alerts.length,
                              separatorBuilder: (_, __) => const SizedBox(height: 12),
                              itemBuilder: (context, idx) {
                                final alert = vm.alerts[idx];

                                return Container(
                                  padding: const EdgeInsets.all(16),
                                  decoration: BoxDecoration(
                                    color: AppColors.surface,
                                    borderRadius: BorderRadius.circular(12),
                                    border: Border.all(
                                      color: alert.isEvacuation ? AppColors.criticalRed : AppColors.border,
                                      width: alert.isEvacuation ? 1.5 : 1.0,
                                    ),
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          StatusBadge.severity(alert.severity),
                                          Text(
                                            'CAP v1.2 • ${alert.urgency}',
                                            style: const TextStyle(
                                              color: AppColors.textSecondary,
                                              fontSize: 11,
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 10),
                                      Text(
                                        alert.headline,
                                        style: const TextStyle(
                                          color: AppColors.textPrimary,
                                          fontSize: 15,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      const SizedBox(height: 6),
                                      Text(
                                        alert.description,
                                        style: const TextStyle(
                                          color: AppColors.textSecondary,
                                          fontSize: 13,
                                        ),
                                      ),
                                      const SizedBox(height: 12),
                                      Container(
                                        padding: const EdgeInsets.all(10),
                                        decoration: BoxDecoration(
                                          color: AppColors.surfaceElevated,
                                          borderRadius: BorderRadius.circular(8),
                                        ),
                                        child: Row(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            const Icon(Icons.info_outline, color: AppColors.primary, size: 16),
                                            const SizedBox(width: 8),
                                            Expanded(
                                              child: Text(
                                                alert.instruction,
                                                style: const TextStyle(
                                                  color: AppColors.textPrimary,
                                                  fontSize: 12,
                                                  fontWeight: FontWeight.w600,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                      const SizedBox(height: 8),
                                      Text(
                                        'Target Area: ${alert.areaDesc}',
                                        style: const TextStyle(
                                          color: AppColors.textMuted,
                                          fontSize: 11,
                                        ),
                                      ),
                                    ],
                                  ),
                                );
                              },
                            ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
