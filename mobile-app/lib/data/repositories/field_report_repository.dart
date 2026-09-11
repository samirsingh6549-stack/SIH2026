import 'dart:async';
import '../../domain/models/field_report.dart';
import '../services/local_database_service.dart';
import '../services/api_client.dart';

class FieldReportRepository {
  final LocalDatabaseService _localDb;
  final ApiClient _apiClient;

  FieldReportRepository({
    LocalDatabaseService? localDb,
    ApiClient? apiClient,
  })  : _localDb = localDb ?? LocalDatabaseService.instance,
        _apiClient = apiClient ?? ApiClient();

  // Core offline-first submission: ALWAYS write to local outbox first!
  Future<FieldReport> submitReport(FieldReport report) async {
    // 1. Persist in local SQLite database
    await _localDb.insertReport(report);

    // 2. Opportunistically attempt background synchronization if network is present
    final isOnline = await _apiClient.checkConnectivity();
    if (isOnline) {
      await syncPendingReports();
    }

    return report;
  }

  // Drain local outbox to Cloud Gateway
  Future<int> syncPendingReports() async {
    final pending = await _localDb.getPendingReports();
    if (pending.isEmpty) return 0;

    final syncedIds = await _apiClient.syncBatchReports(pending);
    if (syncedIds.isNotEmpty) {
      await _localDb.markReportsSynced(syncedIds);
    }
    return syncedIds.length;
  }

  Future<int> getPendingCount() async {
    return await _localDb.getPendingCount();
  }

  Future<List<FieldReport>> getAllReports() async {
    return await _localDb.getAllReports();
  }
}
