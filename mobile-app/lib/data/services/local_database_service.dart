import 'dart:async';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import '../../domain/models/field_report.dart';
import '../models/field_report_model.dart';

class LocalDatabaseService {
  static final LocalDatabaseService instance = LocalDatabaseService._init();
  static Database? _database;

  LocalDatabaseService._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('ner_landslide_outbox.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future<void> _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE field_reports_outbox (
        client_id TEXT PRIMARY KEY,
        reporter_name TEXT NOT NULL,
        reporter_role TEXT,
        reporter_phone TEXT,
        hazard_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        location_description TEXT,
        tension_crack_width_cm REAL,
        road_status TEXT,
        image_base64 TEXT,
        notes TEXT,
        language TEXT,
        local_created_at INTEGER NOT NULL,
        synced_at INTEGER,
        sync_status TEXT NOT NULL
      )
    ''');

    // Index on sync_status for fast offline outbox queries
    await db.execute('''
      CREATE INDEX idx_outbox_sync_status ON field_reports_outbox (sync_status, local_created_at DESC)
    ''');
  }

  // Insert a report into the local outbox
  Future<void> insertReport(FieldReport report) async {
    final db = await database;
    final map = FieldReportModel.toDatabaseMap(report);
    await db.insert(
      'field_reports_outbox',
      map,
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  // Retrieve all reports waiting to be synced to the cloud gateway
  Future<List<FieldReport>> getPendingReports() async {
    final db = await database;
    final result = await db.query(
      'field_reports_outbox',
      where: 'sync_status = ?',
      whereArgs: ['PENDING_SYNC'],
      orderBy: 'local_created_at ASC',
    );

    return result.map((json) => FieldReportModel.fromDatabaseMap(json)).toList();
  }

  // Count pending records for HUD badges
  Future<int> getPendingCount() async {
    final db = await database;
    final result = await db.rawQuery(
      'SELECT COUNT(*) as count FROM field_reports_outbox WHERE sync_status = ?',
      ['PENDING_SYNC'],
    );
    return Sqflite.firstIntValue(result) ?? 0;
  }

  // Mark reports as successfully synced after gateway confirmation
  Future<void> markReportsSynced(List<String> clientIds) async {
    if (clientIds.isEmpty) return;
    final db = await database;
    final now = DateTime.now().millisecondsSinceEpoch;

    final batch = db.batch();
    for (final id in clientIds) {
      batch.update(
        'field_reports_outbox',
        {
          'sync_status': 'SYNCED',
          'synced_at': now,
        },
        where: 'client_id = ?',
        whereArgs: [id],
      );
    }
    await batch.commit(noResult: true);
  }

  // Retrieve all reports history (both synced and pending)
  Future<List<FieldReport>> getAllReports() async {
    final db = await database;
    final result = await db.query(
      'field_reports_outbox',
      orderBy: 'local_created_at DESC',
    );
    return result.map((json) => FieldReportModel.fromDatabaseMap(json)).toList();
  }

  Future<void> close() async {
    final db = _database;
    if (db != null) {
      await db.close();
    }
  }
}
