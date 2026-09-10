const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const CLIENT_DIR = path.join(__dirname, '..', 'client');

// in-memory store for local testing
const db = {
  reports: new Map(),
  riskZones: [
    {
      id: 'rz-1',
      zone_code: 'NER-MEGH-SHILLONG-01',
      zone_name: 'East Khasi Hills Slope Segment A',
      state: 'Meghalaya',
      district: 'East Khasi Hills',
      risk_level: 'HIGH',
      risk_score: 0.81,
      latitude: 25.5788,
      longitude: 91.8933,
      contributing_factors: { rain_accum_mm: 142.5, slope_angle_deg: 38.2 },
      updated_at: new Date().toISOString()
    },
    {
      id: 'rz-2',
      zone_code: 'NER-SIKK-GANGTOK-02',
      zone_name: 'NH-10 Corridor Near Ranipool',
      state: 'Sikkim',
      district: 'East Sikkim',
      risk_level: 'CRITICAL',
      risk_score: 0.935,
      latitude: 27.3389,
      longitude: 88.6065,
      contributing_factors: { pore_pressure_kpa: 42.1, historical_failures: 4 },
      updated_at: new Date().toISOString()
    },
    {
      id: 'rz-3',
      zone_code: 'NER-MIZO-AIZAWL-03',
      zone_name: 'Chite Veng Escarpment',
      state: 'Mizoram',
      district: 'Aizawl',
      risk_level: 'MODERATE',
      risk_score: 0.54,
      latitude: 23.7271,
      longitude: 92.7176,
      contributing_factors: { soil_moisture_pct: 68.0 },
      updated_at: new Date().toISOString()
    }
  ],
  telemetry: [],
  alerts: [
    {
      id: 'alt-1',
      alert_code: 'ALT-2026-001',
      zone_code: 'NER-SIKK-GANGTOK-02',
      severity: 'EVACUATION',
      headline: 'Immediate Evacuation Order: Active debris flow risk along NH-10 Ranipool sector',
      instructions: 'Move immediately to assigned disaster relief shelter at Upper Martam School. Avoid valley roads.',
      target_villages: ['Ranipool', 'Martam', 'Singtam'],
      is_active: true,
      created_at: new Date().toISOString()
    }
  ]
};

function reply(res, status, payload) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, Prefer'
  });
  res.end(JSON.stringify(payload));
}

function parseJson(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', () => {
      if (!raw.trim()) return resolve({});
      try {
        resolve(JSON.parse(raw));
      } catch (err) {
        reject(new Error('Malformed JSON payload'));
      }
    });
    req.on('error', reject);
  });
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.svg': 'image/svg+xml'
};

function serveStatic(req, res, pathname) {
  let target = pathname === '/' ? 'public/index.html' : pathname;
  if (target.startsWith('/src/')) {
    target = target.slice(1);
  } else if (!target.startsWith('public/')) {
    target = path.join('public', target);
  }

  const filePath = path.join(CLIENT_DIR, target);

  fs.stat(filePath, (err, stat) => {
    if (err || !stat.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      return res.end('File not found');
    }

    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    fs.createReadStream(filePath).pipe(res);
  });
}

const server = http.createServer(async (req, res) => {
  const host = req.headers.host || `localhost:${PORT}`;
  const parsed = new URL(req.url, `http://${host}`);
  const pathname = parsed.pathname;

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, Prefer'
    });
    return res.end();
  }

  try {
    // API routes
    if (pathname === '/api/health' && req.method === 'GET') {
      return reply(res, 200, {
        status: 'online',
        server_time: new Date().toISOString(),
        reports_count: db.reports.size,
        active_alerts: db.alerts.filter(a => a.is_active).length
      });
    }

    if (pathname === '/api/risk_zones') {
      if (req.method === 'GET') {
        return reply(res, 200, { count: db.riskZones.length, data: db.riskZones });
      }
      if (req.method === 'POST') {
        const body = await parseJson(req);
        body.id = 'rz-' + (db.riskZones.length + 1);
        body.updated_at = new Date().toISOString();
        db.riskZones.push(body);
        return reply(res, 201, { message: 'saved', data: body });
      }
    }

    if (pathname === '/api/field_reports') {
      if (req.method === 'GET') {
        return reply(res, 200, {
          count: db.reports.size,
          data: Array.from(db.reports.values())
        });
      }

      if (req.method === 'POST') {
        const report = await parseJson(req);
        if (!report.client_id) {
          return reply(res, 400, { error: 'client_id is required' });
        }

        // idempotency check: don't create duplicates on retry
        if (db.reports.has(report.client_id)) {
          return reply(res, 200, {
            status: 'ALREADY_SYNCED',
            client_id: report.client_id
          });
        }

        const saved = {
          ...report,
          synced_at: new Date().toISOString(),
          sync_status: 'SYNCED'
        };
        db.reports.set(report.client_id, saved);

        return reply(res, 201, {
          status: 'SYNCED',
          client_id: saved.client_id,
          synced_at: saved.synced_at
        });
      }
    }

    // batch upload from offline queue
    if (pathname === '/api/field_reports/batch' && req.method === 'POST') {
      const { reports = [] } = await parseJson(req);
      const synced = [];
      const dups = [];

      for (const r of reports) {
        if (!r.client_id) continue;
        if (db.reports.has(r.client_id)) {
          dups.push(r.client_id);
        } else {
          const item = {
            ...r,
            synced_at: new Date().toISOString(),
            sync_status: 'SYNCED'
          };
          db.reports.set(r.client_id, item);
          synced.push(r.client_id);
        }
      }

      return reply(res, 200, {
        status: 'BATCH_SYNC_SUCCESS',
        synced_count: synced.length,
        duplicate_count: dups.length,
        synced_ids: [...synced, ...dups]
      });
    }

    if (pathname === '/api/alerts' && req.method === 'GET') {
      return reply(res, 200, { count: db.alerts.length, data: db.alerts });
    }

    if (pathname === '/api/telemetry') {
      if (req.method === 'GET') {
        return reply(res, 200, {
          count: db.telemetry.length,
          data: db.telemetry.slice(-50)
        });
      }
      if (req.method === 'POST') {
        const item = await parseJson(req);
        item.id = 'tel_' + Date.now();
        item.created_at = new Date().toISOString();
        db.telemetry.push(item);
        return reply(res, 201, { status: 'RECORDED', id: item.id });
      }
    }

    // serve frontend static assets
    serveStatic(req, res, pathname);

  } catch (err) {
    console.error('request handler error:', err);
    reply(res, 500, { error: 'Internal Server Error', detail: err.message });
  }
});

server.listen(PORT, () => {
  console.log(`[server] sync gateway listening on http://localhost:${PORT}`);
});

module.exports = server;
