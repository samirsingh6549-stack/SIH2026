import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';

class OfflineSyncBanner extends StatelessWidget {
  final bool isOnline;
  final int pendingCount;
  final VoidCallback onSyncPressed;
  final bool isSyncing;

  const OfflineSyncBanner({
    super.key,
    required this.isOnline,
    required this.pendingCount,
    required this.onSyncPressed,
    this.isSyncing = false,
  });

  @override
  Widget build(BuildContext context) {
    if (isOnline && pendingCount == 0) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        color: AppColors.surface,
        child: const Row(
          children: [
            Icon(Icons.cloud_done, color: AppColors.stableGreen, size: 16),
            SizedBox(width: 8),
            Text(
              'CLOUD GATEWAY CONNECTED',
              style: TextStyle(
                color: AppColors.stableGreen,
                fontSize: 12,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.5,
              ),
            ),
          ],
        ),
      );
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: pendingCount > 0 ? AppColors.warningOrangeBg : AppColors.surfaceElevated,
        border: Border(
          bottom: BorderSide(
            color: pendingCount > 0 ? AppColors.warningOrange : AppColors.border,
            width: 1,
          ),
        ),
      ),
      child: Row(
        children: [
          Icon(
            isOnline ? Icons.cloud_upload : Icons.cloud_off,
            color: pendingCount > 0 ? AppColors.warningOrange : AppColors.textSecondary,
            size: 20,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  isOnline ? 'NETWORK RESTORED' : 'OFFLINE OUTBOX ACTIVE',
                  style: TextStyle(
                    color: pendingCount > 0 ? AppColors.warningOrange : AppColors.textPrimary,
                    fontSize: 12,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.5,
                  ),
                ),
                Text(
                  pendingCount > 0
                      ? '$pendingCount reports queued locally in SQLite'
                      : 'Zero-network local storage enabled',
                  style: const TextStyle(
                    color: AppColors.textSecondary,
                    fontSize: 11,
                  ),
                ),
              ],
            ),
          ),
          if (pendingCount > 0)
            ElevatedButton(
              onPressed: isSyncing ? null : onSyncPressed,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.warningOrange,
                foregroundColor: Colors.black,
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                minimumSize: Size.zero,
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
              child: isSyncing
                  ? const SizedBox(
                      width: 14,
                      height: 14,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black),
                    )
                  : const Text('SYNC NOW', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            ),
        ],
      ),
    );
  }
}
