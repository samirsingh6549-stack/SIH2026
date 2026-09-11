import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/i18n/dialect_translations.dart';
import '../../shared_widgets/offline_sync_banner.dart';
import '../../shared_widgets/status_badge.dart';
import 'home_view_model.dart';
import '../report/new_report_screen.dart';
import '../sos/sos_screen.dart';
import '../evacuation/evacuation_map_screen.dart';
import '../alerts/alerts_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<HomeViewModel>(
      builder: (context, vm, _) {
        final lang = vm.selectedLanguage;

        return Scaffold(
          appBar: AppBar(
            title: Row(
              children: [
                const Icon(Icons.shield, color: AppColors.primary, size: 22),
                const SizedBox(width: 8),
                Text(DialectTranslations.get('app_title', langCode: lang)),
              ],
            ),
            actions: [
              // 8-Dialect language picker dropdown
              PopupMenuButton<String>(
                icon: const Icon(Icons.translate, color: AppColors.textPrimary),
                tooltip: 'Select Regional Dialect',
                onSelected: (code) => vm.setLanguage(code),
                itemBuilder: (context) {
                  return DialectTranslations.supportedLanguages.map((l) {
                    final isSelected = l['code'] == lang;
                    return PopupMenuItem<String>(
                      value: l['code'],
                      child: Row(
                        children: [
                          if (isSelected)
                            const Icon(Icons.check, color: AppColors.primary, size: 16)
                          else
                            const SizedBox(width: 16),
                          const SizedBox(width: 8),
                          Text('${l['native']} (${l['name']})'),
                        ],
                      ),
                    );
                  }).toList();
                },
              ),
              IconButton(
                icon: const Icon(Icons.refresh),
                tooltip: 'Refresh Status',
                onPressed: () => vm.refreshState(),
              ),
            ],
          ),
          body: RefreshIndicator(
            onRefresh: () => vm.refreshState(),
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                // 1. Offline Sync Status Banner
                OfflineSyncBanner(
                  isOnline: vm.isOnline,
                  pendingCount: vm.pendingOutboxCount,
                  isSyncing: vm.isSyncing,
                  onSyncPressed: () => vm.triggerSync(),
                ),

                // 2. Tactical Telemetry & GPS Coordinates HUD
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Row(
                              children: [
                                Icon(Icons.satellite_alt, color: AppColors.primary, size: 16),
                                SizedBox(width: 6),
                                Text(
                                  'SATELLITE GPS FIX',
                                  style: TextStyle(
                                    color: AppColors.primary,
                                    fontSize: 11,
                                    fontWeight: FontWeight.w800,
                                    letterSpacing: 0.5,
                                  ),
                                ),
                              ],
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: vm.currentGps?.isMockOrCached == true
                                    ? AppColors.warningOrangeBg
                                    : AppColors.stableGreenBg,
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                vm.currentGps?.isMockOrCached == true ? 'OFFLINE CACHED' : 'LIVE SATELLITE',
                                style: TextStyle(
                                  color: vm.currentGps?.isMockOrCached == true
                                      ? AppColors.warningOrange
                                      : AppColors.stableGreen,
                                  fontSize: 9,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '${vm.currentGps?.latitude.toStringAsFixed(4) ?? '27.3250'}° N, ${vm.currentGps?.longitude.toStringAsFixed(4) ?? '88.6120'}° E',
                          style: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'monospace',
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Altitude: ${vm.currentGps?.altitude.toStringAsFixed(0) ?? '1450'} m • Sector: Sikkim Lifeline (NH-10 Ranipool Axis)',
                          style: const TextStyle(color: AppColors.textSecondary, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ),

                // 3. Urgent SOS Panic Beacon Button
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: InkWell(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const SosScreen()),
                      );
                    },
                    borderRadius: BorderRadius.circular(12),
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFFDC2626), Color(0xFF991B1B)],
                        ),
                        borderRadius: BorderRadius.circular(12),
                        boxShadow: [
                          BoxShadow(
                            color: AppColors.criticalRed.withOpacity(0.4),
                            blurRadius: 12,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.warning_amber_rounded, color: Colors.white, size: 28),
                          const SizedBox(width: 10),
                          Text(
                            DialectTranslations.get('sos_panic', langCode: lang),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                              fontWeight: FontWeight.w900,
                              letterSpacing: 1.0,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 20),

                // 4. Primary Feature Grid
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.15,
                    children: [
                      // Card A: Record Field Hazard
                      _ActionCard(
                        icon: Icons.add_location_alt,
                        iconColor: AppColors.primary,
                        title: DialectTranslations.get('new_report', langCode: lang),
                        subtitle: 'Zero-network crack measurement',
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const NewReportScreen()),
                          ).then((_) => vm.refreshState());
                        },
                      ),

                      // Card B: Safe Evacuation Paths
                      _ActionCard(
                        icon: Icons.alt_route,
                        iconColor: AppColors.accent,
                        title: DialectTranslations.get('evac_routes', langCode: lang),
                        subtitle: 'Bypass active debris zones',
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const EvacuationMapScreen()),
                          );
                        },
                      ),

                      // Card C: Active Disaster Alerts
                      _ActionCard(
                        icon: Icons.campaign,
                        iconColor: AppColors.warningOrange,
                        title: DialectTranslations.get('active_alerts', langCode: lang),
                        subtitle: '${vm.activeAlerts.length} regional advisories',
                        badge: vm.activeAlerts.isNotEmpty ? '${vm.activeAlerts.length}' : null,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const AlertsScreen()),
                          );
                        },
                      ),

                      // Card D: Relief Shelter Finder
                      _ActionCard(
                        icon: Icons.night_shelter,
                        iconColor: AppColors.stableGreen,
                        title: 'Relief Shelters',
                        subtitle: 'High ground civil defense camps',
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const EvacuationMapScreen()),
                          );
                        },
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 24),

                // 5. Active Advisory Snapshot
                if (vm.activeAlerts.isNotEmpty) ...[
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          'CRITICAL ADVISORY',
                          style: TextStyle(
                            color: AppColors.textSecondary,
                            fontSize: 12,
                            fontWeight: FontWeight.w800,
                            letterSpacing: 0.5,
                          ),
                        ),
                        StatusBadge.severity(vm.activeAlerts.first.severity),
                      ],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.surfaceElevated,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            vm.activeAlerts.first.headline,
                            style: const TextStyle(
                              color: AppColors.textPrimary,
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            vm.activeAlerts.first.instruction,
                            style: const TextStyle(
                              color: AppColors.textSecondary,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],

                const SizedBox(height: 30),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String title;
  final String subtitle;
  final String? badge;
  final VoidCallback onTap;

  const _ActionCard({
    required this.icon,
    required this.iconColor,
    required this.title,
    required this.subtitle,
    this.badge,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(14.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: iconColor.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(icon, color: iconColor, size: 22),
                  ),
                  if (badge != null)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.criticalRed,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        badge!,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: AppColors.textPrimary,
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: AppColors.textSecondary,
                      fontSize: 11,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
