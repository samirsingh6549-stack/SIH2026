const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 4000;
const PUBLIC_DIR = path.join(__dirname, 'public');

// Scalable Cloud Store covering all 8 North Eastern States (Eight Sisters)
const db = {
  stations: [
    {
      id: 'NER-SIKK-01',
      name: 'Ranipool NH-10 Corridor Station',
      state: 'Sikkim',
      district: 'East Sikkim',
      lat: 27.3389, lng: 88.6065,
      status: 'CRITICAL',
      rainfall_mm_h: 54.2, soil_moisture_pct: 93.5, pore_pressure_kpa: 48.2, tilt_deg: 3.8,
      lifeline: 'NH-10 (Siliguri-Gangtok)',
      history: [
        { time: '02:00', rain: 12.0, pore: 24.1, tilt: 0.8 },
        { time: '04:00', rain: 22.5, pore: 29.5, tilt: 1.1 },
        { time: '06:00', rain: 38.0, pore: 36.2, tilt: 1.9 },
        { time: '08:00', rain: 54.2, pore: 48.2, tilt: 3.8 }
      ]
    },
    {
      id: 'NER-MEGH-02',
      name: 'Mawkdok Dympep Escarpment',
      state: 'Meghalaya',
      district: 'East Khasi Hills',
      lat: 25.5788, lng: 91.8933,
      status: 'HIGH',
      rainfall_mm_h: 38.5, soil_moisture_pct: 82.0, pore_pressure_kpa: 36.4, tilt_deg: 2.1,
      lifeline: 'SH-5 (Shillong-Cherrapunji)',
      history: [
        { time: '02:00', rain: 8.0, pore: 20.0, tilt: 0.4 },
        { time: '04:00', rain: 15.0, pore: 24.5, tilt: 0.7 },
        { time: '06:00', rain: 26.0, pore: 31.0, tilt: 1.3 },
        { time: '08:00', rain: 38.5, pore: 36.4, tilt: 2.1 }
      ]
    },
    {
      id: 'NER-ASSA-03',
      name: 'Dima Hasao Jatinga Valley Array',
      state: 'Assam',
      district: 'Dima Hasao',
      lat: 25.1837, lng: 93.0298,
      status: 'CRITICAL',
      rainfall_mm_h: 46.0, soil_moisture_pct: 91.0, pore_pressure_kpa: 44.0, tilt_deg: 3.2,
      lifeline: 'NH-27 / Lumding-Badarpur Railway',
      history: [
        { time: '02:00', rain: 10.0, pore: 22.0, tilt: 0.6 },
        { time: '04:00', rain: 18.0, pore: 28.0, tilt: 1.2 },
        { time: '06:00', rain: 32.0, pore: 35.0, tilt: 2.1 },
        { time: '08:00', rain: 46.0, pore: 44.0, tilt: 3.2 }
      ]
    },
    {
      id: 'NER-ARUN-04',
      name: 'Bhalukpong-Tawang Alpine Pass',
      state: 'Arunachal Pradesh',
      district: 'West Kameng',
      lat: 27.5861, lng: 91.8653,
      status: 'HIGH',
      rainfall_mm_h: 29.5, soil_moisture_pct: 78.0, pore_pressure_kpa: 32.0, tilt_deg: 1.7,
      lifeline: 'NH-13 (Trans-Arunachal)',
      history: [
        { time: '02:00', rain: 5.0, pore: 16.0, tilt: 0.3 },
        { time: '04:00', rain: 11.0, pore: 21.0, tilt: 0.7 },
        { time: '06:00', rain: 19.0, pore: 26.5, tilt: 1.1 },
        { time: '08:00', rain: 29.5, pore: 32.0, tilt: 1.7 }
      ]
    },
    {
      id: 'NER-MIZO-05',
      name: 'Chite Veng Escarpment Ridge',
      state: 'Mizoram',
      district: 'Aizawl',
      lat: 23.7271, lng: 92.7176,
      status: 'MODERATE',
      rainfall_mm_h: 18.0, soil_moisture_pct: 69.5, pore_pressure_kpa: 26.0, tilt_deg: 0.9,
      lifeline: 'NH-54 (Aizawl-Lunglei)',
      history: [
        { time: '02:00', rain: 4.0, pore: 18.0, tilt: 0.2 },
        { time: '04:00', rain: 9.0, pore: 21.0, tilt: 0.4 },
        { time: '06:00', rain: 14.0, pore: 23.5, tilt: 0.6 },
        { time: '08:00', rain: 18.0, pore: 26.0, tilt: 0.9 }
      ]
    },
    {
      id: 'NER-NAGA-06',
      name: 'Kohima South Bypass / Phesama',
      state: 'Nagaland',
      district: 'Kohima',
      lat: 25.6751, lng: 94.1086,
      status: 'HIGH',
      rainfall_mm_h: 31.2, soil_moisture_pct: 79.4, pore_pressure_kpa: 33.8, tilt_deg: 1.8,
      lifeline: 'NH-29 (Dimapur-Kohima)',
      history: [
        { time: '02:00', rain: 6.0, pore: 19.5, tilt: 0.3 },
        { time: '04:00', rain: 12.0, pore: 23.0, tilt: 0.7 },
        { time: '06:00', rain: 21.0, pore: 28.5, tilt: 1.2 },
        { time: '08:00', rain: 31.2, pore: 33.8, tilt: 1.8 }
      ]
    },
    {
      id: 'NER-MANI-07',
      name: 'Noney Tupul River Corridor',
      state: 'Manipur',
      district: 'Noney',
      lat: 24.8167, lng: 93.6833,
      status: 'CRITICAL',
      rainfall_mm_h: 42.5, soil_moisture_pct: 88.0, pore_pressure_kpa: 41.5, tilt_deg: 2.9,
      lifeline: 'NH-37 (Imphal-Jiribam)',
      history: [
        { time: '02:00', rain: 9.0, pore: 20.0, tilt: 0.5 },
        { time: '04:00', rain: 16.0, pore: 26.0, tilt: 1.0 },
        { time: '06:00', rain: 28.0, pore: 33.0, tilt: 1.8 },
        { time: '08:00', rain: 42.5, pore: 41.5, tilt: 2.9 }
      ]
    },
    {
      id: 'NER-TRIP-08',
      name: 'Jampui Hills Vanghmun Station',
      state: 'Tripura',
      district: 'North Tripura',
      lat: 23.9500, lng: 92.2667,
      status: 'MODERATE',
      rainfall_mm_h: 14.5, soil_moisture_pct: 64.0, pore_pressure_kpa: 22.0, tilt_deg: 0.6,
      lifeline: 'NH-8 (Agartala-Silchar)',
      history: [
        { time: '02:00', rain: 3.0, pore: 14.0, tilt: 0.1 },
        { time: '04:00', rain: 6.0, pore: 17.0, tilt: 0.3 },
        { time: '06:00', rain: 10.0, pore: 19.5, tilt: 0.4 },
        { time: '08:00', rain: 14.5, pore: 22.0, tilt: 0.6 }
      ]
    }
  ],
  riskZones: [
    {
      zone_code: 'NER-SIKK-01',
      name: 'Ranipool NH-10 Corridor',
      state: 'Sikkim', district: 'East Sikkim',
      risk_score: 0.945, risk_level: 'CRITICAL',
      trigger_rainfall_mm: 54.2,
      coordinates: [[27.3450, 88.6000], [27.3490, 88.6150], [27.3350, 88.6220], [27.3310, 88.6040]],
      evacuation_shelter: 'Upper Martam School (Capacity: 600)',
      lifeline_highway: 'NH-10'
    },
    {
      zone_code: 'NER-MEGH-02',
      name: 'Mawkdok Dympep Escarpment',
      state: 'Meghalaya', district: 'East Khasi Hills',
      risk_score: 0.810, risk_level: 'HIGH',
      trigger_rainfall_mm: 38.5,
      coordinates: [[25.5900, 91.8800], [25.6050, 91.9050], [25.5750, 91.9150], [25.5650, 91.8900]],
      evacuation_shelter: 'Sohra Community Hall (Capacity: 450)',
      lifeline_highway: 'SH-5'
    },
    {
      zone_code: 'NER-ASSA-03',
      name: 'Dima Hasao Jatinga Hill Section',
      state: 'Assam', district: 'Dima Hasao',
      risk_score: 0.920, risk_level: 'CRITICAL',
      trigger_rainfall_mm: 46.0,
      coordinates: [[25.1950, 93.0100], [25.2100, 93.0450], [25.1700, 93.0550], [25.1600, 93.0200]],
      evacuation_shelter: 'Haflong Town Stadium Shelter (Capacity: 1200)',
      lifeline_highway: 'NH-27'
    },
    {
      zone_code: 'NER-ARUN-04',
      name: 'Bhalukpong-Tawang Pass',
      state: 'Arunachal Pradesh', district: 'West Kameng',
      risk_score: 0.790, risk_level: 'HIGH',
      trigger_rainfall_mm: 29.5,
      coordinates: [[27.5950, 91.8450], [27.6100, 91.8800], [27.5750, 91.8900], [27.5650, 91.8550]],
      evacuation_shelter: 'Dirang Civil Defense Base (Capacity: 500)',
      lifeline_highway: 'NH-13'
    },
    {
      zone_code: 'NER-MIZO-05',
      name: 'Chite Veng Escarpment',
      state: 'Mizoram', district: 'Aizawl',
      risk_score: 0.540, risk_level: 'MODERATE',
      trigger_rainfall_mm: 18.0,
      coordinates: [[23.7350, 92.7100], [23.7420, 92.7250], [23.7200, 92.7300], [23.7150, 92.7120]],
      evacuation_shelter: 'Aizawl Govt College Gym (Capacity: 750)',
      lifeline_highway: 'NH-54'
    },
    {
      zone_code: 'NER-NAGA-06',
      name: 'Kohima South Bypass / Phesama',
      state: 'Nagaland', district: 'Kohima',
      risk_score: 0.840, risk_level: 'HIGH',
      trigger_rainfall_mm: 31.2,
      coordinates: [[25.6850, 94.0950], [25.6950, 94.1200], [25.6650, 94.1250], [25.6550, 94.1000]],
      evacuation_shelter: 'Kohima Local Ground Shed (Capacity: 900)',
      lifeline_highway: 'NH-29'
    },
    {
      zone_code: 'NER-MANI-07',
      name: 'Noney Tupul River Corridor',
      state: 'Manipur', district: 'Noney',
      risk_score: 0.930, risk_level: 'CRITICAL',
      trigger_rainfall_mm: 42.5,
      coordinates: [[24.8250, 93.6650], [24.8350, 93.6950], [24.8050, 93.7050], [24.7950, 93.6700]],
      evacuation_shelter: 'Noney Higher Secondary (Capacity: 800)',
      lifeline_highway: 'NH-37'
    },
    {
      zone_code: 'NER-TRIP-08',
      name: 'Jampui Hills Ridge',
      state: 'Tripura', district: 'North Tripura',
      risk_score: 0.490, risk_level: 'MODERATE',
      trigger_rainfall_mm: 14.5,
      coordinates: [[23.9600, 92.2500], [23.9700, 92.2800], [23.9400, 92.2850], [23.9300, 92.2550]],
      evacuation_shelter: 'Vanghmun Community Centre (Capacity: 350)',
      lifeline_highway: 'NH-8'
    }
  ],
  fieldReports: new Map([
    [
      'fld_001',
      {
        client_id: 'fld_001',
        reporter: 'Sub-Inspector Lepcha (SDRF)',
        hazard_type: 'Active Debris Flow / Mudslide',
        severity: 'CRITICAL',
        state: 'Sikkim', district: 'East Sikkim',
        lat: 27.3389, lng: 88.6065,
        location_desc: 'Ranipool Bridge Km 12',
        notes: 'Slurry 1.5m deep over roadway. Vehicles stranded.',
        status: 'SYNCED'
      }
    ]
  ]),
  alerts: [
    {
      id: 'ALT-SIKKIM-01',
      zone_code: 'NER-SIKK-01',
      severity: 'EVACUATION',
      headline: {
        en: 'IMMEDIATE EVACUATION: Active Landslide on NH-10 Ranipool',
        hi: 'तत्काल खाली करने का आदेश: रानीपूल एनएच-10 पर भूस्खलन का गंभीर खतरा',
        as: 'জৰুৰীকালীন খালী কৰাৰ নিৰ্দেশ: ৰাণীপুলেৰে যোৱা এনএইচ-১০ত ভূমিস্খলন',
        ne: 'तत्काल खाली गर्ने आदेश: रानीपुल NH-10 मा पहिरोको गम्भीर जोखिम',
        bn: 'অবিলম্বে খালি করার নির্দেশ: রানীপুল এনএইচ-১০ এ ভূমিধসের তীব্র আশঙ্কা',
        mz: 'HMUN HAWLH CHHUAH THUPEK: Ranipool NH-10 ah leimin hlauhawm a awm'
      },
      instructions: {
        en: 'Move uphill towards Upper Martam relief camp immediately. Avoid valley roads and river banks.',
        hi: 'तुरंत ऊपरी मारतम राहत शिविर में जाएं। घाटी की सड़कों और नदी तटों से बचें।',
        as: 'ততালিকে উজনি মাৰ্তাম আশ্ৰয় শিবিৰলৈ যাওক। নদীৰ পাৰৰ পৰা আঁতৰি থাকক।',
        ne: 'तुरुन्तै माथिल्लो मार्तम राहत शिविरमा जानुहोस्। उपत्यकाका सडकहरूबाट टाढा रहनुहोस्।',
        bn: 'অবিলম্বে আপার মার্তাম ত্রাণ শিবিরে যান। উপত্যকার রাস্তা ও নদী তীর এড়িয়ে চলুন।',
        mz: 'Upper Martam School hmun him lam pan nghal rawh u. Lui kam kawng zawh suh u.'
      },
      target_villages: ['Ranipool', 'Martam', 'Singtam'],
      recipients: 3420
    }
  ],
  auditLogs: [
    { time: '08:00:10', module: 'M4: Weather Ingestion', message: 'Monsoon precipitation active across Sikkim, Assam & Manipur.' },
    { time: '08:01:25', module: 'M2: AI/ML Engine', message: 'LSI threshold exceeded in Ranipool (0.945) and Dima Hasao (0.920).' },
    { time: '08:02:00', module: 'M5: Multilingual Alert', message: 'CAP Evacuation broadcast dispatched in Nepali, Assamese, Hindi, Bengali & Mizo.' }
  ]
};

function sendJson(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  });
  res.end(JSON.stringify(data));
}

function parseJson(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', () => {
      if (!raw.trim()) return resolve({});
      try { resolve(JSON.parse(raw)); } catch (err) { reject(err); }
    });
  });
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.svg': 'image/svg+xml'
};

const server = http.createServer(async (req, res) => {
  const host = req.headers.host || `localhost:${PORT}`;
  const parsed = new URL(req.url, `http://${host}`);
  const pathname = parsed.pathname;

  if (req.method === 'OPTIONS') {
    res.writeHead(204, { 'Access-Control-Allow-Origin': '*' });
    return res.end();
  }

  try {
    if (pathname === '/api/stations') return sendJson(res, 200, { stations: db.stations });
    if (pathname === '/api/risk_zones') return sendJson(res, 200, { zones: db.riskZones });
    if (pathname === '/api/alerts') return sendJson(res, 200, { alerts: db.alerts });
    if (pathname === '/api/audit_logs') return sendJson(res, 200, { logs: db.auditLogs });

    if (pathname === '/api/reports') {
      if (req.method === 'GET') {
        return sendJson(res, 200, { reports: Array.from(db.fieldReports.values()) });
      }
      if (req.method === 'POST') {
        const body = await parseJson(req);
        if (db.fieldReports.has(body.client_id)) {
          return sendJson(res, 200, { status: 'ALREADY_SYNCED' });
        }
        const saved = { ...body, status: 'SYNCED', synced_at: new Date().toISOString() };
        db.fieldReports.set(body.client_id, saved);
        db.auditLogs.unshift({
          time: new Date().toLocaleTimeString(),
          module: 'M6: Sync Gateway',
          message: `Ground report [${saved.hazard_type}] received from ${saved.state}: ${saved.reporter}`
        });
        return sendJson(res, 201, { status: 'SYNCED', report: saved });
      }
    }

    if (pathname === '/api/reports/batch' && req.method === 'POST') {
      const { reports = [] } = await parseJson(req);
      const synced = [];
      for (const r of reports) {
        if (!r.client_id) continue;
        const item = { ...r, status: 'SYNCED', synced_at: new Date().toISOString() };
        db.fieldReports.set(r.client_id, item);
        synced.push(r.client_id);
      }
      db.auditLogs.unshift({
        time: new Date().toLocaleTimeString(),
        module: 'M6: Sync Gateway',
        message: `Batch sync complete: ${synced.length} offline report(s) flushed from field device.`
      });
      return sendJson(res, 200, { status: 'BATCH_SYNC_SUCCESS', synced_count: synced.length, synced_ids: synced });
    }

    if (pathname === '/api/simulate/monsoon_surge' && req.method === 'POST') {
      const { rainfall_mm = 75.0 } = await parseJson(req);
      const st = db.stations[0];
      st.rainfall_mm_h = rainfall_mm;
      st.pore_pressure_kpa = +(45.0 + rainfall_mm * 0.12).toFixed(1);
      st.soil_moisture_pct = Math.min(99.0, 88.0 + rainfall_mm * 0.1);
      return sendJson(res, 200, { station: st });
    }

    // Static Assets
    let fileTarget = pathname === '/' ? 'index.html' : pathname.replace(/^\//, '');
    const fullPath = path.join(PUBLIC_DIR, fileTarget);

    fs.stat(fullPath, (err, stat) => {
      if (err || !stat.isFile()) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        return res.end('Not Found');
      }
      const ext = path.extname(fullPath);
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
      fs.createReadStream(fullPath).pipe(res);
    });

  } catch (err) {
    sendJson(res, 500, { error: err.message });
  }
});

server.listen(PORT, () => {
  console.log(`[NER-LEWS] Unified Platform covering all 8 States: http://localhost:${PORT}`);
});
