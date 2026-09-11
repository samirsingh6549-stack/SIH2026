import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../../../core/constants/app_colors.dart';
import 'sos_view_model.dart';
import '../../shared_widgets/custom_button.dart';

class SosScreen extends StatelessWidget {
  const SosScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => SosViewModel()..init(),
      child: Consumer<SosViewModel>(
        builder: (context, vm, _) {
          return Scaffold(
            backgroundColor: const Color(0xFF0B0606),
            appBar: AppBar(
              backgroundColor: Colors.transparent,
              title: const Text('Emergency Distress SOS'),
            ),
            body: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Top Status
                  Column(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                        decoration: BoxDecoration(
                          color: AppColors.criticalRedBg,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: AppColors.criticalRed),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.warning, color: AppColors.criticalRed, size: 16),
                            SizedBox(width: 8),
                            Text(
                              'LIFE SAFETY DISTRESS BEACON',
                              style: TextStyle(
                                color: AppColors.criticalRed,
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                                letterSpacing: 0.8,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 12),
                      const Text(
                        'Direct Satellite Geolocation',
                        style: TextStyle(color: AppColors.textSecondary, fontSize: 13),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '${vm.currentGps?.latitude.toStringAsFixed(4) ?? "27.3250"}° N, ${vm.currentGps?.longitude.toStringAsFixed(4) ?? "88.6120"}° E',
                        style: const TextStyle(
                          color: AppColors.textPrimary,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          fontFamily: 'monospace',
                        ),
                      ),
                    ],
                  ),

                  // Giant Center Panic Trigger
                  Center(
                    child: GestureDetector(
                      onTap: () => vm.triggerEmergencyBeacon(),
                      child: Container(
                        width: 200,
                        height: 200,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: AppColors.criticalRed,
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.criticalRed.withOpacity(0.5),
                              blurRadius: 30,
                              spreadRadius: 8,
                            ),
                          ],
                        ),
                        child: Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                vm.isDispatched ? Icons.check_circle : Icons.touch_app,
                                color: Colors.white,
                                size: 54,
                              ),
                              const SizedBox(height: 8),
                              Text(
                                vm.isDispatched ? 'SOS ACTIVE' : 'TAP FOR SOS',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 18,
                                  fontWeight: FontWeight.w900,
                                  letterSpacing: 1.0,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Siren / Audio Toggle
                  if (vm.isSirenActive)
                    ElevatedButton.icon(
                      onPressed: () => vm.stopSiren(),
                      icon: const Icon(Icons.volume_off, color: Colors.black),
                      label: const Text('SILENCE SIREN', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.white),
                    ),

                  // Bottom Action Box (SMS 2G Fallback)
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.sms, color: AppColors.primary, size: 16),
                            SizedBox(width: 8),
                            Text(
                              'OFFLINE 2G SMS FALLBACK BEACON',
                              style: TextStyle(
                                color: AppColors.primary,
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Text(
                          vm.smsPayload ?? 'Generating coordinate beacon...',
                          style: const TextStyle(color: AppColors.textSecondary, fontSize: 12),
                        ),
                        const SizedBox(height: 10),
                        Row(
                          children: [
                            Expanded(
                              child: OutlinedButton.icon(
                                icon: const Icon(Icons.copy, size: 14),
                                label: const Text('COPY FOR SMS (112)'),
                                onPressed: () {
                                  if (vm.smsPayload != null) {
                                    Clipboard.setData(ClipboardData(text: vm.smsPayload!));
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(content: Text('✓ SOS text copied! Paste into SMS to 112.')),
                                    );
                                  }
                                },
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
