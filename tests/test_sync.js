const http = require('http');

const HOST = 'localhost';
const PORT = 3000;

function api(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: HOST,
      port: PORT,
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
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function run() {
  let serverProcess = null;

  // auto-start server if not already running
  try {
    await api('GET', '/api/health');
  } catch {
    serverProcess = require('../server/mock_backend.js');
    await new Promise(r => setTimeout(r, 200));
  }

  let passed = 0;
  let failed = 0;

  function check(desc, condition) {
    if (condition) {
      console.log(`  ✓ ${desc}`);
      passed++;
    } else {
      console.error(`  ✗ ${desc}`);
      failed++;
    }
  }

  console.log('\nRunning sync gateway test suite...\n');

  try {
    // 1. health
    const health = await api('GET', '/api/health');
    check('gateway health returns online', health.status === 200 && health.body.status === 'online');

    // 2. single report
    const testId = 'fld_test_' + Date.now();
    const repRes = await api('POST', '/api/field_reports', {
      client_id: testId,
      reporter_name: 'Scout A',
      hazard_type: 'Soil Crack',
      severity: 'HIGH',
      latitude: 25.5788,
      longitude: 91.8933,
      local_created_at: new Date().toISOString()
    });
    check('ingests field report with client_id', repRes.status === 201 && repRes.body.status === 'SYNCED');

    // 3. duplicate report (idempotent retry)
    const dupRes = await api('POST', '/api/field_reports', {
      client_id: testId,
      reporter_name: 'Scout A',
      hazard_type: 'Soil Crack',
      severity: 'HIGH',
      latitude: 25.5788,
      longitude: 91.8933,
      local_created_at: new Date().toISOString()
    });
    check('duplicate report returns ALREADY_SYNCED without error', dupRes.status === 200 && dupRes.body.status === 'ALREADY_SYNCED');

    // 4. batch sync
    const batchRes = await api('POST', '/api/field_reports/batch', {
      reports: [
        {
          client_id: 'fld_batch_1',
          hazard_type: 'Rockfall',
          severity: 'MEDIUM',
          latitude: 27.3389,
          longitude: 88.6065,
          local_created_at: new Date().toISOString()
        },
        {
          client_id: 'fld_batch_2',
          hazard_type: 'Mudslide',
          severity: 'CRITICAL',
          latitude: 23.7271,
          longitude: 92.7176,
          local_created_at: new Date().toISOString()
        },
        { client_id: testId } // re-send existing to test mixed batch
      ]
    });
    check(
      'batch sync handles new and duplicate reports cleanly',
      batchRes.status === 200 && batchRes.body.synced_count === 2 && batchRes.body.duplicate_count === 1
    );

    // 5. query reports
    const list = await api('GET', '/api/field_reports');
    check('lists all synced reports', list.status === 200 && list.body.count >= 3);

    // 6. telemetry
    const tel = await api('POST', '/api/telemetry', {
      station_id: 'NER-MEGH-SHILLONG-01',
      rainfall_mm_h: 18.2,
      soil_moisture_percent: 74.0,
      pore_water_pressure_kpa: 30.5,
      slope_tilt_degrees: 1.1
    });
    check('records station telemetry', tel.status === 201 && tel.body.status === 'RECORDED');

    // 7. risk zones
    const zones = await api('GET', '/api/risk_zones');
    check('retrieves cached risk zones', zones.status === 200 && zones.body.count >= 3);

    // 8. alerts
    const alerts = await api('GET', '/api/alerts');
    check('retrieves emergency alerts', alerts.status === 200 && alerts.body.count >= 1);

    console.log(`\nTests finished: ${passed} passed, ${failed} failed.\n`);

    if (serverProcess && serverProcess.close) {
      serverProcess.close();
    }

    if (failed > 0) process.exit(1);
  } catch (err) {
    console.error('test suite failed with error:', err);
    if (serverProcess && serverProcess.close) serverProcess.close();
    process.exit(1);
  }
}

run();
