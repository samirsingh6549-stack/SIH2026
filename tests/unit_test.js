const http = require('http');

// lightweight assertion library (zero external npm dependencies)
let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function it(description, fn) {
  totalTests++;
  try {
    fn();
    console.log(`    ✓ ${description}`);
    passedTests++;
  } catch (err) {
    console.error(`    ✗ ${description}`);
    console.error(`      Error: ${err.message}`);
    failedTests++;
  }
}

async function itAsync(description, fn) {
  totalTests++;
  try {
    await fn();
    console.log(`    ✓ ${description}`);
    passedTests++;
  } catch (err) {
    console.error(`    ✗ ${description}`);
    console.error(`      Error: ${err.message}`);
    failedTests++;
  }
}

function expect(actual) {
  return {
    toBe(expected) {
      if (actual !== expected) {
        throw new Error(`Expected ${JSON.stringify(expected)} but received ${JSON.stringify(actual)}`);
      }
    },
    toBeGreaterThanOrEqual(expected) {
      if (actual < expected) {
        throw new Error(`Expected ${actual} >= ${expected}`);
      }
    },
    toBeDefined() {
      if (actual === undefined || actual === null) {
        throw new Error(`Expected value to be defined, got ${actual}`);
      }
    },
    toContain(expected) {
      if (!Array.isArray(actual) && typeof actual !== 'string') {
        throw new Error(`Expected array or string, got ${typeof actual}`);
      }
      if (!actual.includes(expected)) {
        throw new Error(`Expected collection to contain ${expected}`);
      }
    }
  };
}

// helper for HTTP requests to cloud gateway
function request(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: 'localhost',
      port: 3000,
      path,
      method,
      headers: { 'Content-Type': 'application/json' }
    }, res => {
      let buf = '';
      res.on('data', chunk => buf += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(buf) });
        } catch {
          resolve({ status: res.statusCode, body: buf });
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// mock storage unit to test offline queue logic in pure nodejs
class MockOutboxQueue {
  constructor() {
    this.store = new Map();
  }

  saveReport(report) {
    const id = report.client_id || 'uuid_' + Date.now();
    const record = {
      ...report,
      client_id: id,
      status: 'PENDING_SYNC',
      local_timestamp: new Date().toISOString()
    };
    this.store.set(id, record);
    return record;
  }

  getPending() {
    return Array.from(this.store.values()).filter(r => r.status === 'PENDING_SYNC');
  }

  markSynced(clientIds) {
    clientIds.forEach(id => {
      if (this.store.has(id)) {
        const item = this.store.get(id);
        item.status = 'SYNCED';
        item.synced_at = new Date().toISOString();
      }
    });
  }
}

async function runUnitTests() {
  console.log('======================================================');
  console.log('  RUNNING UNIT & FUNCTIONAL TESTS FOR CLOUD & SYNC    ');
  console.log('======================================================\n');

  let serverInstance = null;
  try {
    await request('GET', '/api/health');
  } catch {
    serverInstance = require('../server/mock_backend.js');
    await new Promise(r => setTimeout(r, 250));
  }

  // SUITE 1: OFFLINE OUTBOX & STORE-AND-FORWARD LOGIC
  console.log('Suite 1: Offline Outbox & Queue Logic (Client SDK)');
  
  const queue = new MockOutboxQueue();
  
  it('should store report in local outbox with PENDING_SYNC status', () => {
    const r = queue.saveReport({
      client_id: 'test_c1',
      reporter_name: 'Scout A',
      hazard_type: 'Soil Crack',
      severity: 'HIGH'
    });
    expect(r.status).toBe('PENDING_SYNC');
    expect(queue.getPending().length).toBe(1);
  });

  it('should preserve multiple offline reports in order without data loss', () => {
    queue.saveReport({ client_id: 'test_c2', hazard_type: 'Rockfall', severity: 'MEDIUM' });
    queue.saveReport({ client_id: 'test_c3', hazard_type: 'Mudflow', severity: 'CRITICAL' });
    expect(queue.getPending().length).toBe(3);
  });

  it('should transition records from PENDING_SYNC to SYNCED upon acknowledgment', () => {
    queue.markSynced(['test_c1', 'test_c2']);
    expect(queue.getPending().length).toBe(1);
    expect(queue.store.get('test_c1').status).toBe('SYNCED');
  });

  // SUITE 2: CLOUD API & IDEMPOTENCY
  console.log('\nSuite 2: Cloud Gateway & Idempotency Engine');

  await itAsync('GET /api/health should confirm cloud backend is operational', async () => {
    const res = await request('GET', '/api/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('online');
  });

  const uniqueId = 'unit_idempotent_' + Date.now();

  await itAsync('POST /api/field_reports should ingest initial offline record', async () => {
    const res = await request('POST', '/api/field_reports', {
      client_id: uniqueId,
      reporter_name: 'Ground Scout',
      hazard_type: 'Debris Flow',
      severity: 'CRITICAL',
      latitude: 27.3389,
      longitude: 88.6065
    });
    expect(res.status).toBe(201);
    expect(res.body.status).toBe('SYNCED');
  });

  await itAsync('POST /api/field_reports should handle retry with same client_id without creating duplicate', async () => {
    const res = await request('POST', '/api/field_reports', {
      client_id: uniqueId,
      reporter_name: 'Ground Scout',
      hazard_type: 'Debris Flow',
      severity: 'CRITICAL'
    });
    // Must return 200 ALREADY_SYNCED (idempotent, no server crash or duplicate)
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ALREADY_SYNCED');
  });

  await itAsync('POST /api/field_reports/batch should sync multiple offline records in one HTTP round-trip', async () => {
    const b1 = 'batch_' + Date.now() + '_1';
    const b2 = 'batch_' + Date.now() + '_2';
    
    const res = await request('POST', '/api/field_reports/batch', {
      reports: [
        { client_id: b1, hazard_type: 'Rockfall', severity: 'HIGH' },
        { client_id: b2, hazard_type: 'Soil Crack', severity: 'LOW' },
        { client_id: uniqueId } // repeat duplicate to verify mixed handling
      ]
    });

    expect(res.status).toBe(200);
    expect(res.body.synced_count).toBe(2);
    expect(res.body.duplicate_count).toBe(1);
    expect(res.body.synced_ids).toContain(b1);
    expect(res.body.synced_ids).toContain(b2);
  });

  // SUITE 3: SENSOR TELEMETRY & PHYSICAL CONSTRAINTS
  console.log('\nSuite 3: Sensor Feeds & Geotechnical Boundary Validation');

  await itAsync('POST /api/telemetry should accept valid slope & precipitation metrics', async () => {
    const res = await request('POST', '/api/telemetry', {
      station_id: 'NER-MEGH-SHILLONG-01',
      rainfall_mm_h: 32.5,
      soil_moisture_percent: 88.2,
      pore_water_pressure_kpa: 41.0,
      slope_tilt_degrees: 2.3
    });
    expect(res.status).toBe(201);
    expect(res.body.status).toBe('RECORDED');
    expect(res.body.id).toBeDefined();
  });

  // SUITE 4: DOWNSTREAM HAZARD ZONES & EMERGENCY BROADCASTS
  console.log('\nSuite 4: Downstream Data for Offline Map Caching');

  await itAsync('GET /api/risk_zones should provide pre-cached zones with severity ratings', async () => {
    const res = await request('GET', '/api/risk_zones');
    expect(res.status).toBe(200);
    expect(res.body.count).toBeGreaterThanOrEqual(3);
    const firstZone = res.body.data[0];
    expect(firstZone.zone_code).toBeDefined();
    expect(['LOW', 'MODERATE', 'HIGH', 'CRITICAL']).toContain(firstZone.risk_level);
  });

  await itAsync('GET /api/alerts should return active evacuation orders with village targets', async () => {
    const res = await request('GET', '/api/alerts');
    expect(res.status).toBe(200);
    expect(res.body.count).toBeGreaterThanOrEqual(1);
    const alert = res.body.data[0];
    expect(alert.is_active).toBe(true);
    expect(alert.target_villages.length).toBeGreaterThanOrEqual(1);
  });

  console.log('\n======================================================');
  console.log(`  UNIT TEST SUMMARY: ${passedTests}/${totalTests} PASSED (${failedTests} FAILED)`);
  console.log('======================================================\n');

  if (serverInstance && serverInstance.close) {
    serverInstance.close();
  }

  if (failedTests > 0) {
    process.exit(1);
  }
}

runUnitTests();
