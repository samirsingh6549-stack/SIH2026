import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';

class StatusBadge extends StatelessWidget {
  final String label;
  final Color color;
  final Color backgroundColor;

  const StatusBadge({
    super.key,
    required this.label,
    required this.color,
    required this.backgroundColor,
  });

  factory StatusBadge.severity(String severity) {
    switch (severity.toUpperCase()) {
      case 'CRITICAL':
      case 'EVACUATION':
        return const StatusBadge(
          label: 'CRITICAL',
          color: AppColors.criticalRed,
          backgroundColor: AppColors.criticalRedBg,
        );
      case 'HIGH':
      case 'WARNING':
        return const StatusBadge(
          label: 'HIGH RISK',
          color: AppColors.warningOrange,
          backgroundColor: AppColors.warningOrangeBg,
        );
      case 'MEDIUM':
      case 'ADVISORY':
        return const StatusBadge(
          label: 'ADVISORY',
          color: AppColors.advisoryYellow,
          backgroundColor: AppColors.advisoryYellowBg,
        );
      default:
        return const StatusBadge(
          label: 'STABLE',
          color: AppColors.stableGreen,
          backgroundColor: AppColors.stableGreenBg,
        );
    }
  }

  factory StatusBadge.syncStatus(String syncStatus) {
    if (syncStatus.toUpperCase() == 'SYNCED') {
      return const StatusBadge(
        label: 'SYNCED TO CLOUD',
        color: AppColors.syncedGreen,
        backgroundColor: AppColors.stableGreenBg,
      );
    }
    return const StatusBadge(
      label: 'OFFLINE QUEUED',
      color: AppColors.offlinePending,
      backgroundColor: AppColors.warningOrangeBg,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withOpacity(0.5), width: 1),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 10,
          fontWeight: FontWeight.w800,
          letterSpacing: 0.4,
        ),
      ),
    );
  }
}
