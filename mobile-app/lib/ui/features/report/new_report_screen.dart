import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/constants/app_colors.dart';
import '../../../domain/models/field_report.dart';
import 'new_report_view_model.dart';
import '../../shared_widgets/custom_button.dart';

class NewReportScreen extends StatefulWidget {
  const NewReportScreen({super.key});

  @override
  State<NewReportScreen> createState() => _NewReportScreenState();
}

class _NewReportScreenState extends State<NewReportScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController(text: 'Scout Tashi Dorjee');
  final _phoneController = TextEditingController(text: '+91 98320 12345');
  final _locationController = TextEditingController(text: 'NH-10 km 22 near Ranipool bridge culvert');
  final _notesController = TextEditingController();

  String _hazardType = 'Tension Crack';
  String _state = 'Sikkim';
  String _district = 'East Sikkim';

  final List<String> _hazardTypes = [
    'Tension Crack',
    'Debris Flow',
    'Rotational Cut-Slope Slide',
    'Rockfall / Toe Erosion',
    'Mudflow & Blockage',
  ];

  final List<String> _nerStates = [
    'Sikkim',
    'Assam',
    'Meghalaya',
    'Arunachal Pradesh',
    'Nagaland',
    'Manipur',
    'Mizoram',
    'Tripura',
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _locationController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => NewReportViewModel()..initLocation(),
      child: Consumer<NewReportViewModel>(
        builder: (context, vm, _) {
          return Scaffold(
            appBar: AppBar(
              title: const Text('Record Field Hazard'),
            ),
            body: Form(
              key: _formKey,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  // GPS Banner
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.my_location, color: AppColors.primary, size: 20),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'GEO-TAGGED SATELLITE POSITION',
                                style: TextStyle(
                                  color: AppColors.primary,
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                '${vm.currentGps?.latitude.toStringAsFixed(5) ?? "27.32500"}° N, ${vm.currentGps?.longitude.toStringAsFixed(5) ?? "88.61200"}° E',
                                style: const TextStyle(
                                  color: AppColors.textPrimary,
                                  fontSize: 13,
                                  fontWeight: FontWeight.bold,
                                  fontFamily: 'monospace',
                                ),
                              ),
                            ],
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.refresh, color: AppColors.textSecondary, size: 20),
                          onPressed: () => vm.initLocation(),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 16),

                  // State and District
                  Row(
                    children: [
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          value: _state,
                          decoration: const InputDecoration(labelText: 'NER State'),
                          items: _nerStates.map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
                          onChanged: (val) {
                            if (val != null) setState(() => _state = val);
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: TextFormField(
                          initialValue: _district,
                          decoration: const InputDecoration(labelText: 'District'),
                          onChanged: (val) => _district = val,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 16),

                  // Hazard Type
                  DropdownButtonFormField<String>(
                    value: _hazardType,
                    decoration: const InputDecoration(labelText: 'Observed Hazard Phenomenon'),
                    items: _hazardTypes.map((h) => DropdownMenuItem(value: h, child: Text(h))).toList(),
                    onChanged: (val) {
                      if (val != null) setState(() => _hazardType = val);
                    },
                  ),

                  const SizedBox(height: 16),

                  // Severity Selector
                  const Text('Hazard Severity Level', style: TextStyle(color: AppColors.textSecondary, fontSize: 12)),
                  const SizedBox(height: 6),
                  SegmentedButton<ReportSeverity>(
                    segments: const [
                      ButtonSegment(value: ReportSeverity.low, label: Text('Low')),
                      ButtonSegment(value: ReportSeverity.medium, label: Text('Medium')),
                      ButtonSegment(value: ReportSeverity.high, label: Text('High')),
                      ButtonSegment(value: ReportSeverity.critical, label: Text('Critical')),
                    ],
                    selected: {vm.severity},
                    onSelectionChanged: (val) => vm.setSeverity(val.first),
                    style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.resolveWith<Color>((states) {
                        if (states.contains(MaterialState.selected)) {
                          switch (vm.severity) {
                            case ReportSeverity.critical:
                              return AppColors.criticalRed;
                            case ReportSeverity.high:
                              return AppColors.warningOrange;
                            case ReportSeverity.medium:
                              return AppColors.advisoryYellow;
                            case ReportSeverity.low:
                              return AppColors.stableGreen;
                          }
                        }
                        return AppColors.surface;
                      }),
                      foregroundColor: MaterialStateProperty.resolveWith<Color>((states) {
                        return states.contains(MaterialState.selected) ? Colors.black : AppColors.textPrimary;
                      }),
                    ),
                  ),

                  const SizedBox(height: 16),

                  // Tension Crack Width Slider
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Tension Crack Width', style: TextStyle(color: AppColors.textSecondary, fontSize: 13)),
                      Text(
                        '${vm.crackWidthCm.toStringAsFixed(1)} cm',
                        style: const TextStyle(
                          color: AppColors.primary,
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  Slider(
                    value: vm.crackWidthCm,
                    min: 0.0,
                    max: 50.0,
                    divisions: 100,
                    activeColor: AppColors.primary,
                    onChanged: (val) => vm.setCrackWidth(val),
                  ),

                  const SizedBox(height: 12),

                  // Road Passability Status
                  const Text('Lifeline Highway Passability', style: TextStyle(color: AppColors.textSecondary, fontSize: 12)),
                  const SizedBox(height: 6),
                  DropdownButtonFormField<RoadStatus>(
                    value: vm.roadStatus,
                    decoration: const InputDecoration(labelText: 'Road Status'),
                    items: const [
                      DropdownMenuItem(value: RoadStatus.passable, child: Text('Passable (Normal Traffic)')),
                      DropdownMenuItem(value: RoadStatus.singleLane, child: Text('Single-Lane Only (Debris on Shoulder)')),
                      DropdownMenuItem(value: RoadStatus.blocked, child: Text('Blocked (Debris Covering Highway)')),
                      DropdownMenuItem(value: RoadStatus.collapsed, child: Text('Road Surface Collapsed / Sunk')),
                    ],
                    onChanged: (val) {
                      if (val != null) vm.setRoadStatus(val);
                    },
                  ),

                  const SizedBox(height: 16),

                  // Location Description / Landmark
                  TextFormField(
                    controller: _locationController,
                    decoration: const InputDecoration(
                      labelText: 'Location / Landmark Details',
                      hintText: 'e.g. NH-10 near Ranipool culvert, uphill slope moving',
                    ),
                    validator: (val) => val == null || val.isEmpty ? 'Required field' : null,
                  ),

                  const SizedBox(height: 16),

                  // Notes
                  TextFormField(
                    controller: _notesController,
                    maxLines: 3,
                    decoration: const InputDecoration(
                      labelText: 'Field Notes & Observations',
                      hintText: 'Water seepage observed along toe, tension fractures expanding...',
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Submit Button
                  CustomButton(
                    text: 'SAVE TO OFFLINE OUTBOX',
                    icon: Icons.save,
                    isLoading: vm.isSaving,
                    onPressed: () async {
                      if (_formKey.currentState?.validate() != true) return;

                      final success = await vm.submitReport(
                        reporterName: _nameController.text,
                        reporterPhone: _phoneController.text,
                        hazardType: _hazardType,
                        state: _state,
                        district: _district,
                        locationDescription: _locationController.text,
                        notes: _notesController.text,
                      );

                      if (context.mounted) {
                        if (success) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              backgroundColor: AppColors.stableGreen,
                              content: Text('✓ Hazard report saved to local SQLite outbox!'),
                            ),
                          );
                          Navigator.pop(context);
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              backgroundColor: AppColors.criticalRed,
                              content: Text('Failed to save report locally.'),
                            ),
                          );
                        }
                      }
                    },
                  ),

                  const SizedBox(height: 30),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
