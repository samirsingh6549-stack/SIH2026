import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/constants/app_colors.dart';
import 'evacuation_view_model.dart';
import '../../shared_widgets/status_badge.dart';

class EvacuationMapScreen extends StatelessWidget {
  const EvacuationMapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => EvacuationViewModel()..loadSafeRoute(),
      child: Consumer<EvacuationViewModel>(
        builder: (context, vm, _) {
          final path = vm.evacuationPath;

          return Scaffold(
            appBar: AppBar(
              title: const Text('Safe Evacuation Pathfinder'),
              actions: [
                IconButton(
                  icon: const Icon(Icons.refresh),
                  onPressed: () => vm.loadSafeRoute(),
                ),
              ],
            ),
            body: vm.isLoading
                ? const Center(child: CircularProgressIndicator())
                : path == null
                    ? const Center(child: Text('No safe evacuation route found.'))
                    : ListView(
                        padding: const EdgeInsets.all(16),
                        children: [
                          // 1. Dynamic Bypass Notification Header
                          Container(
                            padding: const EdgeInsets.all(14),
                            decoration: BoxDecoration(
                              color: AppColors.surface,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: AppColors.stableGreen, width: 1.5),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(Icons.verified, color: AppColors.stableGreen, size: 18),
                                        SizedBox(width: 8),
                                        Text(
                                          'SAFE BYPASS ACTIVE',
                                          style: TextStyle(
                                            color: AppColors.stableGreen,
                                            fontSize: 12,
                                            fontWeight: FontWeight.w900,
                                            letterSpacing: 0.5,
                                          ),
                                        ),
                                      ],
                                    ),
                                    StatusBadge(
                                      label: 'OFFLINE ROUTE',
                                      color: AppColors.primary,
                                      backgroundColor: AppColors.primaryGlow,
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  'Detoured around: ${path.avoidedHazardZone}',
                                  style: const TextStyle(
                                    color: AppColors.warningOrange,
                                    fontSize: 12,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                                const SizedBox(height: 12),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                                  children: [
                                    _StatItem(
                                      label: 'DISTANCE',
                                      value: '${path.totalDistanceKm} km',
                                      icon: Icons.straighten,
                                    ),
                                    _StatItem(
                                      label: 'EST. TIME',
                                      value: '${path.estimatedTravelMinutes} mins',
                                      icon: Icons.timer,
                                    ),
                                    _StatItem(
                                      label: 'WAYPOINTS',
                                      value: '${path.waypoints.length}',
                                      icon: Icons.pin_drop,
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),

                          const SizedBox(height: 16),

                          // 2. Designated Relief Shelter Card
                          Container(
                            padding: const EdgeInsets.all(14),
                            decoration: BoxDecoration(
                              color: AppColors.surfaceElevated,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: AppColors.border),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'DESIGNATED HIGH-GROUND CIVIL SHELTER',
                                  style: TextStyle(
                                    color: AppColors.primary,
                                    fontSize: 10,
                                    fontWeight: FontWeight.w800,
                                    letterSpacing: 0.5,
                                  ),
                                ),
                                const SizedBox(height: 6),
                                Text(
                                  path.targetShelter.name,
                                  style: const TextStyle(
                                    color: AppColors.textPrimary,
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  '${path.targetShelter.location} • Elevation: ${path.targetShelter.elevationM.toInt()}m',
                                  style: const TextStyle(color: AppColors.textSecondary, fontSize: 12),
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  children: [
                                    const Icon(Icons.people, color: AppColors.stableGreen, size: 16),
                                    const SizedBox(width: 6),
                                    Text(
                                      'Capacity: ${path.targetShelter.capacity} citizens (Water, Medical Aid & Power)',
                                      style: const TextStyle(
                                        color: AppColors.textPrimary,
                                        fontSize: 12,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),

                          const SizedBox(height: 20),

                          // 3. Turn-by-Turn Waypoint Navigation Sequence
                          const Text(
                            'SAFE ELEVATION WAYPOINTS',
                            style: TextStyle(
                              color: AppColors.textSecondary,
                              fontSize: 12,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.5,
                            ),
                          ),
                          const SizedBox(height: 8),

                          ...path.waypoints.asMap().entries.map((entry) {
                            final idx = entry.key;
                            final wp = entry.value;
                            final isLast = idx == path.waypoints.length - 1;

                            return Container(
                              margin: const EdgeInsets.only(bottom: 8),
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: AppColors.surface,
                                borderRadius: BorderRadius.circular(10),
                                border: Border.all(
                                  color: isLast ? AppColors.stableGreen : AppColors.border,
                                ),
                              ),
                              child: Row(
                                children: [
                                  CircleAvatar(
                                    radius: 14,
                                    backgroundColor: isLast ? AppColors.stableGreen : AppColors.primary,
                                    child: Text(
                                      '${idx + 1}',
                                      style: const TextStyle(color: Colors.black, fontSize: 11, fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          wp.name,
                                          style: const TextStyle(
                                            color: AppColors.textPrimary,
                                            fontSize: 13,
                                            fontWeight: FontWeight.w700,
                                          ),
                                        ),
                                        Text(
                                          '${wp.latitude.toStringAsFixed(4)}° N, ${wp.longitude.toStringAsFixed(4)}° E • Elev: ${wp.elevationM.toInt()}m',
                                          style: const TextStyle(
                                            color: AppColors.textSecondary,
                                            fontSize: 11,
                                            fontFamily: 'monospace',
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  if (isLast)
                                    const Icon(Icons.flag, color: AppColors.stableGreen, size: 20),
                                ],
                              ),
                            );
                          }),

                          const SizedBox(height: 30),
                        ],
                      ),
          );
        },
      ),
    );
  }
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;

  const _StatItem({
    required this.label,
    required this.value,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Icon(icon, color: AppColors.primary, size: 18),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            color: AppColors.textPrimary,
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            color: AppColors.textSecondary,
            fontSize: 10,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }
}
