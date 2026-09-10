// NER-LEWS: Full 8-State Disaster Platform Controller with Multilingual Support

let map;
let telemetryChart;
let isOfflineMode = false;
let currentLanguage = 'en';

// Layer Groups
let zoneLayerGroup;
let stationLayerGroup;
let reportLayerGroup;
let bufferLayerGroup;
let mlHeatmapLayer;
let mlCircleMarkersGroup;

// Local Outbox (IndexedDB simulation)
let localOutbox = [
  {
    client_id: 'fld_001',
    reporter: 'Sub-Inspector Lepcha (SDRF)',
    hazard_type: 'Active Debris Flow / Mudslide',
    severity: 'CRITICAL',
    state: 'Sikkim',
    lat: 27.3389, lng: 88.6065,
    location_desc: 'Ranipool Bridge Km 12 (NH-10)',
    notes: 'Slurry 1.5m deep over roadway. Vehicles stranded.',
    status: 'SYNCED',
    synced_at: '08:05:40 IST'
  }
];

// All 8 North Eastern States (Eight Sisters)
const HOTSPOTS = {
  sikkim: { lat: 27.3389, lng: 88.6065, zoom: 13, name: 'Sikkim (NH-10 Ranipool Corridor)' },
  assam: { lat: 25.1837, lng: 93.0298, zoom: 13, name: 'Assam (Dima Hasao Jatinga Section)' },
  manipur: { lat: 24.8167, lng: 93.6833, zoom: 13, name: 'Manipur (Noney Tupul Corridor)' },
  meghalaya: { lat: 25.5788, lng: 91.8933, zoom: 13, name: 'Meghalaya (East Khasi Hills Sohra)' },
  nagaland: { lat: 25.6751, lng: 94.1086, zoom: 13, name: 'Nagaland (Kohima South Bypass NH-29)' },
  arunachal: { lat: 27.5861, lng: 91.8653, zoom: 13, name: 'Arunachal Pradesh (Tawang Alpine Pass)' },
  mizoram: { lat: 23.7271, lng: 92.7176, zoom: 13, name: 'Mizoram (Aizawl Chite Veng)' },
  tripura: { lat: 23.9500, lng: 92.2667, zoom: 13, name: 'Tripura (Jampui Hills Ridge)' }
};

// Multilingual Dictionary (Stored locally for offline dead zones)
const I18N = {
  en: {
    app_title: 'NER-LEWS',
    app_sub: 'AI Landslide Monitoring & Offline Sync Backbone for the Eight Sisters of North East India',
    sector_focus: 'State / Sector:',
    dead_zone: 'Mountain Dead Zone:',
    net_online: 'ONLINE (4G/LTE)',
    net_offline: 'OFFLINE (DEAD ZONE)',
    matrix_title: '8-State Vulnerability Matrix',
    scenario_title: 'Cloudburst Simulator',
    cap_orders: 'CAP Evacuation Orders',
    audio_btn: 'Audio Alert',
    tab_sensors: 'Telemetry',
    tab_fieldapp: 'Field Scout App',
    tab_audit: 'Audit Stream',
    lbl_reporter: 'Reporter Identification',
    lbl_severity: 'Severity Level',
    lbl_roadstatus: 'Roadway Status',
    lbl_hazard: 'GSI Landslide Classification',
    lbl_notes: 'Field Observations & Endangered Assets',
    lbl_submit: 'Save & Queue Ground Report',
    lbl_outbox: 'Device Outbox (Offline Queue)'
  },
  hi: {
    app_title: 'एनईआर-लेव्स (NER-LEWS)',
    app_sub: 'पूर्वोत्तर भारत के आठ राज्यों के लिए एआई भूस्खलन निगरानी और ऑफलाइन सिंक प्लेटफॉर्म',
    sector_focus: 'राज्य / सेक्टर चयन:',
    dead_zone: 'पहाड़ी डेड ज़ोन:',
    net_online: 'ऑनलाइन (4G/LTE)',
    net_offline: 'ऑफलाइन (डेड ज़ोन - नेटवर्क बंद)',
    matrix_title: '8-राज्य सुभेद्यता मैट्रिक्स',
    scenario_title: 'बादल फटने का सिम्युलेटर',
    cap_orders: 'सीएपी निकासी आदेश',
    audio_btn: 'ऑडियो अलर्ट सुनें',
    tab_sensors: 'टेलीमेट्री सेंसर',
    tab_fieldapp: 'फील्ड स्काउट ऐप',
    tab_audit: 'ऑडिट स्ट्रीम',
    lbl_reporter: 'अधिकारी / नागरिक का नाम',
    lbl_severity: 'खतरे की गंभीरता',
    lbl_roadstatus: 'सड़क मार्ग की स्थिति',
    lbl_hazard: 'जीएसआई भूस्खलन वर्गीकरण',
    lbl_notes: 'अवलोकन एवं खतरे में संपत्तियां',
    lbl_submit: 'रिपोर्ट सहेजें और सिंक कतार में रखें',
    lbl_outbox: 'डिवाइस आउटबॉक्स (ऑफलाइन कतार)'
  },
  as: {
    app_title: 'এনইআৰ-লেউছ (NER-LEWS)',
    app_sub: 'উত্তৰ-পূৰ্বাঞ্চলৰ অষ্টভগ্নী ৰাজ্যৰ বাবে এআই ভূমিস্খলন সতৰ্কবাণী আৰু অফলাইন ছিংক',
    sector_focus: 'ৰাজ্য / খণ্ড বাছক:',
    dead_zone: 'পাহাৰীয়া ডেড জ\'ন:',
    net_online: 'অনলাইন (সংযোগ সক্ৰিয়)',
    net_offline: 'অফলাইন (ডেড জ\'ন - বিচ্ছিন্ন)',
    matrix_title: '৮-ৰাজ্যৰ ভূমিস্খলন মেট্ৰিক্স',
    scenario_title: 'মেঘ বিস্ফোৰণ ছিমুলেটৰ',
    cap_orders: 'স্থান খালী কৰাৰ নিৰ্দেশনা',
    audio_btn: 'শব্দ বাৰ্তা শুনক',
    tab_sensors: 'ছেন্সৰ টেলিমেট্ৰী',
    tab_fieldapp: 'ফিল্ড স্কাউট এপ',
    tab_audit: 'অডিট বাৰ্তা',
    lbl_reporter: 'প্ৰতিবেদকৰ পৰিচয়',
    lbl_severity: 'বিপদৰ তীব্ৰতা',
    lbl_roadstatus: 'পথৰ স্থিতি',
    lbl_hazard: 'জিএছআই ভূমিস্খলনৰ প্ৰকাৰ',
    lbl_notes: 'প্ৰত্যক্ষদৰ্শীৰ টোকা',
    lbl_submit: 'প্ৰতিবেদন সংৰক্ষণ কৰক',
    lbl_outbox: 'ডিভাইচ আউটবক্স (অফলাইন)'
  },
  ne: {
    app_title: 'एनईआर-लेव्स (NER-LEWS)',
    app_sub: 'पूर्वोत्तर भारतका आठ राज्यहरूका लागि एआई पहिरो पूर्व चेतावनी प्रणाली',
    sector_focus: 'राज्य / क्षेत्र छनौट:',
    dead_zone: 'पहाडी डेड जोन:',
    net_online: 'अनलाइन (४जी जडान)',
    net_offline: 'अफलाइन (नेटवर्क बन्द)',
    matrix_title: '८-राज्य पहिरो जोखिम तालिका',
    scenario_title: 'वर्षा प्रकोप सिम्युलेटर',
    cap_orders: 'तुरुन्त खाली गर्ने आदेश',
    audio_btn: 'अडियो सुन्नुहोस्',
    tab_sensors: 'सेन्सर टेलिमेट्री',
    tab_fieldapp: 'फिल्ड स्काउट एप',
    tab_audit: 'अडिट स्ट्रिम',
    lbl_reporter: 'प्रतिवेदकको नाम',
    lbl_severity: 'जोखिम स्तर',
    lbl_roadstatus: 'सडक यातायातको अवस्था',
    lbl_hazard: 'पहिरोको वैज्ञानिक वर्गीकरण',
    lbl_notes: 'अवलोकन र विवरण',
    lbl_submit: 'प्रतिवेदन दर्ता गर्नुहोस्',
    lbl_outbox: 'उपकरण आउटबक्स (अफलाइन)'
  },
  bn: {
    app_title: 'এনইআর-লেউস (NER-LEWS)',
    app_sub: 'উত্তর-পূর্ব ভারতের আটটি রাজ্যের জন্য এআই ভূমিধস আগাম সতর্কবার্তা প্ল্যাটফর্ম',
    sector_focus: 'রাজ্য / সেক্টর নির্বাচন:',
    dead_zone: 'পাহাড়ি ডেড জোন:',
    net_online: 'অনলাইন (৪জি সংযুক্ত)',
    net_offline: 'অফলাইন (নেটওয়ার্ক বিচ্ছিন্ন)',
    matrix_title: '৮-রাজ্য ভূমিধস ম্যাট্রিক্স',
    scenario_title: 'বৃষ্টিপাত সিমুলেটর',
    cap_orders: 'অবিলম্বে স্থান ত্যাগের নির্দেশ',
    audio_btn: 'অডিও শুনুন',
    tab_sensors: 'টেলিমেট্রি সেন্সর',
    tab_fieldapp: 'ফিল্ড স্কাউট অ্যাপ',
    tab_audit: 'অডিট স্ট্রিম',
    lbl_reporter: 'রিপোর্টারের পরিচয়',
    lbl_severity: 'বিপদের মাত্রা',
    lbl_roadstatus: 'সড়ক পথের অবস্থা',
    lbl_hazard: 'জিএসআই ভূমিধস শ্রেণিবিভাগ',
    lbl_notes: 'পর্যবেক্ষণ ও তথ্য',
    lbl_submit: 'রিপোর্ট সংরক্ষণ ও সিঙ্ক করুন',
    lbl_outbox: 'ডিভাইস আউটবক্স (অফলাইন)'
  },
  mz: {
    app_title: 'NER-LEWS',
    app_sub: 'Hmar-Chhak State 8 te tana AI hmanga Leimin Vauhkhanna leh Offline Sync',
    sector_focus: 'State / Hmun thlanna:',
    dead_zone: 'Tlang ram Signal awmlohna:',
    net_online: 'ONLINE (Inzawm fel a ni)',
    net_offline: 'OFFLINE (Signal a bo)',
    matrix_title: 'State 8 Leimin Hlauhawm Dinhmun',
    scenario_title: 'Ruahpui Sur Zual Chhutna',
    cap_orders: 'Hmun Chhuahsan Tura Thupek',
    audio_btn: 'Aw Ngaithla Rawh',
    tab_sensors: 'Sensor Hmuhte',
    tab_fieldapp: 'Field Scout App',
    tab_audit: 'Audit Stream',
    lbl_reporter: 'Hming leh Nihna',
    lbl_severity: 'Hlauhawm Dan',
    lbl_roadstatus: 'Kawng Dinhmun',
    lbl_hazard: 'Leimin Dan Pung',
    lbl_notes: 'Hmuh dan tlangpui',
    lbl_submit: 'Duhna Khawl Khawmna a Dah',
    lbl_outbox: 'Device Outbox (Offline)'
  }
};

let cachedAlertsData = [];

document.addEventListener('DOMContentLoaded', async () => {
  startClock();
  initTabs();
  initGISMap();
  initChart();
  initLanguageSwitcher();
  initOfflineToggle();
  initScenarioSlider();
  initFieldScoutForm();
  initVoiceAlertButton();

  await refreshAllData();
  setInterval(pollAuditLogs, 6000);
});

// 1. CLOCK
function startClock() {
  const clockEl = document.getElementById('ist-clock');
  const dateEl = document.getElementById('ist-date');
  function update() {
    const now = new Date();
    clockEl.textContent = now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour12: false }) + ' IST';
    dateEl.textContent = now.toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'short', year: 'numeric' });
  }
  update();
  setInterval(update, 1000);
}

// 2. LANGUAGE SWITCHER
function initLanguageSwitcher() {
  const select = document.getElementById('lang-select');
  select.addEventListener('change', (e) => {
    currentLanguage = e.target.value;
    applyLanguage(currentLanguage);
    renderAlerts(cachedAlertsData);
  });
}

function applyLanguage(lang) {
  const dict = I18N[lang] || I18N.en;
  document.getElementById('lbl-app-title').textContent = dict.app_title;
  document.getElementById('lbl-app-sub').textContent = dict.app_sub;
  document.getElementById('lbl-sector-focus').textContent = dict.sector_focus;
  document.getElementById('lbl-dead-zone-sim').textContent = dict.dead_zone;
  document.getElementById('lbl-vulnerability-matrix').textContent = dict.matrix_title;
  document.getElementById('lbl-what-if-sim').textContent = dict.scenario_title;
  document.getElementById('lbl-cap-orders').textContent = dict.cap_orders;
  document.getElementById('lbl-voice-btn').textContent = dict.audio_btn;
  document.getElementById('lbl-tab-sensors').textContent = dict.tab_sensors;
  document.getElementById('lbl-tab-fieldapp').textContent = dict.tab_fieldapp;
  document.getElementById('lbl-tab-audit').textContent = dict.tab_audit;
  document.getElementById('lbl-reporter').textContent = dict.lbl_reporter;
  document.getElementById('lbl-severity').textContent = dict.lbl_severity;
  document.getElementById('lbl-roadstatus').textContent = dict.lbl_roadstatus;
  document.getElementById('lbl-hazard').textContent = dict.lbl_hazard;
  document.getElementById('lbl-notes').textContent = dict.lbl_notes;
  document.getElementById('lbl-submit-btn').textContent = dict.lbl_submit;
  document.getElementById('lbl-outbox-title').textContent = dict.lbl_outbox;
  
  const badge = document.getElementById('net-indicator');
  badge.textContent = isOfflineMode ? dict.net_offline : dict.net_online;
}

// 3. VOICE ALERT (TEXT-TO-SPEECH)
function initVoiceAlertButton() {
  document.getElementById('btn-voice-alert').addEventListener('click', () => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }

    if (!cachedAlertsData || !cachedAlertsData.length) return;
    const alertItem = cachedAlertsData[0];
    
    // Pick text in selected language
    const textToSpeak = (alertItem.headline[currentLanguage] || alertItem.headline.en) + ". " + 
                        (alertItem.instructions[currentLanguage] || alertItem.instructions.en);

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = 0.9;
    
    // Set appropriate voice language tag if available
    const langMap = { en: 'en-IN', hi: 'hi-IN', bn: 'bn-IN', as: 'as-IN', ne: 'ne-NP', mz: 'en-IN' };
    utterance.lang = langMap[currentLanguage] || 'en-IN';

    window.speechSynthesis.speak(utterance);
  });
}

// 4. TABS
function initTabs() {
  const tabs = document.querySelectorAll('.p-tab');
  const panes = document.querySelectorAll('.p-tab-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panes.forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const target = tab.getAttribute('data-target');
      document.getElementById(target).classList.add('active');
      if (telemetryChart) telemetryChart.resize();
    });
  });
}

// 5. GIS MAP
function initGISMap() {
  map = L.map('gis-main-map', { zoomControl: true, minZoom: 6, maxZoom: 18 }).setView([26.2006, 92.9376], 7); // Center over NER

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; CARTO | OpenStreetMap | SIH 2026 NER-LEWS'
  }).addTo(map);

  zoneLayerGroup = L.layerGroup().addTo(map);
  stationLayerGroup = L.layerGroup().addTo(map);
  reportLayerGroup = L.layerGroup().addTo(map);
  bufferLayerGroup = L.layerGroup().addTo(map);
  mlCircleMarkersGroup = L.layerGroup().addTo(map);

  document.getElementById('chk-ml-heatmap').addEventListener('change', e => {
    if (e.target.checked) {
      if (mlHeatmapLayer) map.addLayer(mlHeatmapLayer);
      if (mlCircleMarkersGroup) map.addLayer(mlCircleMarkersGroup);
    } else {
      if (mlHeatmapLayer) map.removeLayer(mlHeatmapLayer);
      if (mlCircleMarkersGroup) map.removeLayer(mlCircleMarkersGroup);
    }
  });

  document.getElementById('chk-zones').addEventListener('change', e => { if (e.target.checked) map.addLayer(zoneLayerGroup); else map.removeLayer(zoneLayerGroup); });
  document.getElementById('chk-stations').addEventListener('change', e => { if (e.target.checked) map.addLayer(stationLayerGroup); else map.removeLayer(stationLayerGroup); });
  document.getElementById('chk-reports').addEventListener('change', e => { if (e.target.checked) map.addLayer(reportLayerGroup); else map.removeLayer(reportLayerGroup); });
  document.getElementById('chk-buffers').addEventListener('change', e => { if (e.target.checked) map.addLayer(bufferLayerGroup); else map.removeLayer(bufferLayerGroup); });

  document.getElementById('hotspot-select').addEventListener('change', e => {
    const loc = HOTSPOTS[e.target.value];
    if (loc) map.flyTo([loc.lat, loc.lng], loc.zoom, { duration: 1.5 });
  });

  document.getElementById('btn-center-map').addEventListener('click', () => {
    map.flyTo([26.2006, 92.9376], 7, { duration: 1.2 });
  });
}

// 6. CHART.JS
function initChart() {
  const ctx = document.getElementById('telemetry-chart').getContext('2d');
  telemetryChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['02:00', '04:00', '06:00', '08:00'],
      datasets: [
        {
          label: 'Rainfall Intensity (mm/h)',
          data: [12.0, 22.5, 38.0, 54.2],
          borderColor: '#0284c7',
          backgroundColor: 'rgba(2, 132, 199, 0.15)',
          fill: true,
          tension: 0.35,
          yAxisID: 'yRain'
        },
        {
          label: 'Pore Pressure (kPa)',
          data: [24.1, 29.5, 36.2, 48.2],
          borderColor: '#ef4444',
          backgroundColor: 'transparent',
          borderDash: [4, 4],
          tension: 0.35,
          yAxisID: 'yPore'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { labels: { color: '#94a3b8', font: { size: 9 } } } },
      scales: {
        x: { grid: { color: '#142035' }, ticks: { color: '#64748b', font: { size: 8 } } },
        yRain: { type: 'linear', position: 'left', grid: { color: '#142035' }, ticks: { color: '#0284c7', font: { size: 8 } } },
        yPore: { type: 'linear', position: 'right', grid: { drawOnChartArea: false }, ticks: { color: '#ef4444', font: { size: 8 } } }
      }
    }
  });
}

// 7. DATA REFRESH & MAP RENDERING ACROSS ALL 8 STATES
async function refreshAllData() {
  try {
    const rainSliderVal = document.getElementById('rain-range') ? document.getElementById('rain-range').value : 75;
    const [stRes, zRes, altRes, repRes, mlRes] = await Promise.all([
      fetch('/api/stations').then(r => r.json()),
      fetch('/api/risk_zones').then(r => r.json()),
      fetch('/api/alerts').then(r => r.json()),
      fetch('/api/reports').then(r => r.json()),
      fetch(`/api/ml/heatmap?rainfall=${rainSliderVal}`).then(r => r.json()).catch(err => {
        console.warn('ML Heatmap endpoint fetch failed:', err);
        return null;
      })
    ]);

    cachedAlertsData = altRes.alerts || [];

    // Plot AI Machine Learning Probability Heatmap & Hotspot Circle Markers
    if (mlRes && mlRes.status === 'success') {
      renderMlHeatmap(mlRes);
    }

    // Plot All 8 State Risk Zones & Lifelines
    zoneLayerGroup.clearLayers();
    bufferLayerGroup.clearLayers();
    zRes.zones.forEach(z => {
      const color = z.risk_level === 'CRITICAL' ? '#ef4444' : z.risk_level === 'HIGH' ? '#f59e0b' : '#eab308';
      const poly = L.polygon(z.coordinates, { color, fillColor: color, fillOpacity: 0.32, weight: 2 }).addTo(zoneLayerGroup);

      poly.bindPopup(`
        <div style="font-size:12px; line-height:1.4;">
          <strong style="color:${color};">${z.zone_code}: ${z.name}</strong><br>
          State: <strong>${z.state}</strong> (${z.district})<br>
          Lifeline Corridor: <strong>${z.lifeline_highway}</strong><br>
          LSI Risk: <strong>${(z.risk_score * 100).toFixed(1)}% (${z.risk_level})</strong><br>
          Trigger Rain: ${z.trigger_rainfall_mm} mm/h<br>
          <hr style="margin:4px 0; border:0; border-top:1px solid #444;">
          Shelter: ${z.evacuation_shelter}
        </div>
      `);

      if (z.risk_level === 'CRITICAL') {
        L.circle(z.coordinates[0], { radius: 1500, color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.08, dashArray: '6,6', weight: 1 }).addTo(bufferLayerGroup);
      }
    });

    // Plot 8 Geotech Stations
    stationLayerGroup.clearLayers();
    stRes.stations.forEach(st => {
      const color = st.status === 'CRITICAL' ? '#ef4444' : st.status === 'HIGH' ? '#f59e0b' : '#10b981';
      const m = L.circleMarker([st.lat, st.lng], { radius: 8, color: '#fff', fillColor: color, fillOpacity: 0.95, weight: 2 }).addTo(stationLayerGroup);
      
      m.bindPopup(`
        <div style="font-size:12px;">
          <strong>🛰️ ${st.id}: ${st.name}</strong><br>
          State: <strong>${st.state}</strong> (${st.district})<br>
          Lifeline Highway: <strong>${st.lifeline}</strong><br>
          Rain: <strong>${st.rainfall_mm_h} mm/h</strong> | Soil: <strong>${st.soil_moisture_pct}%</strong><br>
          Pore Pressure: <strong>${st.pore_pressure_kpa} kPa</strong> | Tilt: <strong>${st.tilt_deg}°</strong><br>
          Status: <span style="color:${color}; font-weight:bold;">${st.status}</span>
        </div>
      `);
      m.on('click', () => selectStation(st));
    });

    // Plot Field Reports
    reportLayerGroup.clearLayers();
    repRes.reports.forEach(r => plotReportMarker(r));

    renderDistrictTable(zRes.zones);
    renderAlerts(cachedAlertsData);
    renderOutboxUI();

  } catch (err) {
    console.error('Data refresh error:', err);
  }
}

// RENDER AI PROBABILITY HEATMAP & SCORING LAYER
function renderMlHeatmap(data) {
  if (!data || !data.leaflet_heat_points) return;

  // 1. Remove previous smooth heat layer if exists
  if (mlHeatmapLayer && map.hasLayer(mlHeatmapLayer)) {
    map.removeLayer(mlHeatmapLayer);
  }

  // 2. Build continuous density heat layer via Leaflet.heat
  if (typeof L.heatLayer === 'function') {
    mlHeatmapLayer = L.heatLayer(data.leaflet_heat_points, {
      radius: 42,
      blur: 24,
      maxZoom: 12,
      max: 1.0,
      gradient: {
        0.15: '#22c55e',
        0.40: '#eab308',
        0.65: '#f97316',
        0.85: '#ef4444'
      }
    });

    if (document.getElementById('chk-ml-heatmap').checked) {
      mlHeatmapLayer.addTo(map);
    }
  }

  // 3. Clear and render crisp interactive circle markers with probability scores
  mlCircleMarkersGroup.clearLayers();
  if (data.geojson_feature_collection && data.geojson_feature_collection.features) {
    data.geojson_feature_collection.features.forEach(f => {
      const p = f.properties;
      const coords = [f.geometry.coordinates[1], f.geometry.coordinates[0]];
      const pct = (p.lsi_score * 100).toFixed(1);

      const circle = L.circleMarker(coords, {
        radius: 9,
        fillColor: p.color,
        color: '#ffffff',
        weight: 1.5,
        fillOpacity: 0.92
      });

      // Quick hover tooltip
      circle.bindTooltip(`<strong>${p.station_name}</strong><br>AI Probability: <span style="color:${p.color};font-weight:bold;">${pct}% (${p.risk_level})</span>`, {
        direction: 'top',
        className: 'heatmap-tooltip'
      });

      // Detailed popup
      circle.bindPopup(`
        <div style="font-size:12px; line-height:1.45; min-width:190px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="background:${p.color}; color:#fff; padding:2px 7px; border-radius:3px; font-weight:bold; font-size:10px;">${p.risk_level} RISK</span>
            <span style="font-weight:bold; color:${p.color}; font-size:13px;">${pct}%</span>
          </div>
          <strong>${p.station_name}</strong><br>
          State: <strong>${p.state}</strong> (${p.location_id})<br>
          Continuous LSI Score: <strong>${p.lsi_score}</strong><br>
          <hr style="margin:5px 0; border:0; border-top:1px solid #334155;">
          <span style="font-size:10px; color:#94a3b8;">Module 1 AI Engine (Physics-Guided Random Forest + Antecedent Rain Matrix)</span>
        </div>
      `);

      circle.addTo(mlCircleMarkersGroup);
    });
  }

  // 4. Update status summary in map toolbar footer
  const statusEl = document.getElementById('lbl-batch-status');
  if (statusEl) {
    const maxPct = (data.max_lsi_score * 100).toFixed(1);
    const meanPct = (data.mean_lsi_score * 100).toFixed(1);
    statusEl.textContent = `${data.grid_cell_count} Cells (Max: ${maxPct}%, Mean: ${meanPct}%)`;
  }
}


function selectStation(st) {
  document.getElementById('station-name-disp').textContent = `${st.id}: ${st.name}`;
  document.getElementById('station-coords-disp').textContent = `${st.district}, ${st.state} • Lifeline: ${st.lifeline}`;
  document.getElementById('station-status-disp').textContent = st.status;
  document.getElementById('station-status-disp').className = `badge ${st.status === 'CRITICAL' ? 'badge-critical' : 'badge-high'}`;

  document.getElementById('disp-rain').innerHTML = `${st.rainfall_mm_h} <small>mm/h</small>`;
  document.getElementById('disp-moisture').innerHTML = `${st.soil_moisture_pct} <small>%</small>`;
  document.getElementById('disp-pore').innerHTML = `${st.pore_pressure_kpa} <small>kPa</small>`;
  document.getElementById('disp-tilt').innerHTML = `${st.tilt_deg} <small>deg</small>`;

  if (telemetryChart && st.history) {
    telemetryChart.data.labels = st.history.map(h => h.time);
    telemetryChart.data.datasets[0].data = st.history.map(h => h.rain);
    telemetryChart.data.datasets[1].data = st.history.map(h => h.pore);
    telemetryChart.update();
  }
}

function plotReportMarker(r) {
  const m = L.circleMarker([r.lat, r.lng], { radius: 9, fillColor: '#0284c7', color: '#ffffff', weight: 2, fillOpacity: 0.95 }).addTo(reportLayerGroup);
  m.bindPopup(`
    <div style="font-size:12px;">
      <span style="background:#0284c7; color:#fff; padding:1px 5px; border-radius:3px; font-weight:bold;">GROUND REPORT</span><br>
      <strong>${r.hazard_type}</strong> (${r.severity})<br>
      State: <strong>${r.state}</strong><br>
      Reporter: ${r.reporter}<br>
      Location: ${r.location_desc || 'NER Sector'}<br>
      Notes: <small>${r.notes || ''}</small>
    </div>
  `);
}

function renderDistrictTable(zones) {
  const tbody = document.getElementById('district-tbody');
  tbody.innerHTML = zones.map(z => {
    const badge = z.risk_level === 'CRITICAL' ? 'badge-critical' : z.risk_level === 'HIGH' ? 'badge-high' : 'badge-moderate';
    return `
      <tr>
        <td><strong>${z.state}</strong><br><small style="color:var(--text-dim);">${z.district}</small></td>
        <td>${z.trigger_rainfall_mm} mm</td>
        <td><strong>${(z.risk_score * 100).toFixed(0)}%</strong></td>
        <td><span class="badge ${badge}">${z.risk_level}</span></td>
      </tr>
    `;
  }).join('');
}

function renderAlerts(alerts) {
  const container = document.getElementById('active-alerts-container');
  if (!alerts || !alerts.length) {
    container.innerHTML = '<div style="font-size:11px; color:var(--text-dim);">No active evacuation directives.</div>';
    return;
  }

  container.innerHTML = alerts.map(a => {
    const title = a.headline[currentLanguage] || a.headline.en;
    const desc = a.instructions[currentLanguage] || a.instructions.en;
    return `
      <div class="cap-alert-item">
        <div class="cap-alert-header">
          <span class="cap-badge">${a.severity}</span>
          <span style="font-size:10px; color:var(--text-dim);"><i class="fa-solid fa-language"></i> ${currentLanguage.toUpperCase()}</span>
        </div>
        <div class="cap-body">
          <strong>${title}</strong><br>
          ${desc}
        </div>
        <div class="cap-footer">
          <i class="fa-solid fa-bullhorn"></i> Villages: ${a.target_villages.join(', ')} • 
          Broadcast: <strong>${a.recipients} SMS/IVRS</strong>
        </div>
      </div>
    `;
  }).join('');
}

// 8. WHAT-IF SCENARIO
function initScenarioSlider() {
  const slider = document.getElementById('rain-range');
  const disp = document.getElementById('slider-rain-val');
  const btn = document.getElementById('btn-run-scenario');

  slider.addEventListener('input', () => { 
    disp.textContent = `${slider.value} mm/h`; 
  });

  // Dynamically recompute batch ML probabilities and heatmap on slider drag release
  slider.addEventListener('change', async () => {
    try {
      const res = await fetch(`/api/ml/heatmap?rainfall=${slider.value}`);
      const data = await res.json();
      if (data && data.status === 'success') {
        renderMlHeatmap(data);
      }
    } catch (e) {
      console.warn('Live slider heatmap update error:', e);
    }
  });

  btn.addEventListener('click', async () => {
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Testing Factor of Safety...';
    btn.disabled = true;

    try {
      const res = await fetch('/api/simulate/monsoon_surge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rainfall_mm: parseFloat(slider.value) })
      });
      const data = await res.json();
      selectStation(data.station);
      if (data.heatmap) {
        renderMlHeatmap(data.heatmap);
      }
      await refreshAllData();
      alert(`⚡ MONSOON SURGE SIMULATED:\n\nRainfall intensity ${slider.value} mm/h evaluated across Sikkim & Assam lifelines.\nPore water pressure reached ${data.station.pore_pressure_kpa} kPa.\nEmergency sirens & SMS dispatched in native dialects!`);
    } finally {
      btn.innerHTML = '<i class="fa-solid fa-bolt"></i> Run Predictive Slope Stress Test';
      btn.disabled = false;
    }
  });
}

// 9. OFFLINE SYNC ENGINE & FIELD FORM
function initOfflineToggle() {
  const toggle = document.getElementById('offline-toggle');
  const badge = document.getElementById('net-indicator');
  const banner = document.getElementById('banner-text');

  toggle.addEventListener('change', async () => {
    isOfflineMode = toggle.checked;
    const dict = I18N[currentLanguage] || I18N.en;

    if (isOfflineMode) {
      badge.textContent = dict.net_offline;
      badge.className = 'network-badge offline';
      banner.textContent = 'CELLULAR DEAD ZONE DETECTED. Local IndexedDB store-and-forward queue active.';
    } else {
      badge.textContent = dict.net_online;
      badge.className = 'network-badge online';
      banner.textContent = 'Network Restored (4G/LTE). Flushing offline outbox packets to cloud...';
      await flushOutbox();
    }
  });
}

function initFieldScoutForm() {
  const form = document.getElementById('scout-report-form');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const selectedState = document.getElementById('in-state').value;
    const loc = HOTSPOTS[selectedState.toLowerCase()] || HOTSPOTS.sikkim;

    const report = {
      client_id: 'fld_' + Date.now().toString(36),
      reporter: document.getElementById('in-reporter').value,
      severity: document.getElementById('in-severity').value,
      state: selectedState,
      hazard_type: document.getElementById('in-hazard').value,
      road_status: document.getElementById('in-roadstatus').value,
      notes: document.getElementById('in-notes').value,
      lat: loc.lat + (Math.random() - 0.5) * 0.015,
      lng: loc.lng + (Math.random() - 0.5) * 0.015,
      location_desc: `${selectedState} Lifeline Corridor`,
      status: isOfflineMode ? 'PENDING_SYNC' : 'SYNCED'
    };

    localOutbox.unshift(report);
    renderOutboxUI();

    if (isOfflineMode) {
      alert(`📦 OFFLINE STORE-AND-FORWARD QUEUE:\n\nDevice is in a remote mountain dead zone in ${selectedState}.\nReport saved in local device storage.\nIt will auto-sync as soon as signal returns.`);
    } else {
      try {
        await fetch('/api/reports', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(report)
        });
        plotReportMarker(report);
        alert('✅ Ground Report transmitted to Cloud Gateway and plotted on GIS map!');
      } catch (err) {
        console.warn('Saved offline:', err);
      }
    }
  });
}

async function flushOutbox() {
  const pending = localOutbox.filter(r => r.status === 'PENDING_SYNC');
  if (!pending.length) return;

  try {
    const res = await fetch('/api/reports/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reports: pending })
    });
    const data = await res.json();

    pending.forEach(r => {
      r.status = 'SYNCED';
      plotReportMarker(r);
    });

    renderOutboxUI();
    alert(`📡 RECONNECTED:\n\nSynced ${data.synced_count} offline report(s) to Cloud Gateway.\nNew hazard markers plotted on the GIS map!`);
  } catch (err) {
    console.error('Batch sync error:', err);
  }
}

function renderOutboxUI() {
  const container = document.getElementById('outbox-items-container');
  const pendingCount = localOutbox.filter(r => r.status === 'PENDING_SYNC').length;
  const syncedCount = localOutbox.filter(r => r.status === 'SYNCED').length;

  document.getElementById('badge-pending').textContent = `${pendingCount} Pending`;
  document.getElementById('badge-synced').textContent = `${syncedCount} Synced`;

  container.innerHTML = localOutbox.map(item => `
    <div class="outbox-card-item">
      <div>
        <strong>${item.hazard_type}</strong> (${item.state})<br>
        <span style="color:var(--text-dim); font-size:9px;">${item.reporter} • ${item.road_status || ''}</span>
      </div>
      <span class="badge ${item.status === 'PENDING_SYNC' ? 'badge-amber' : 'badge-success'}">
        ${item.status === 'PENDING_SYNC' ? '⏳ OFFLINE' : '✓ SYNCED'}
      </span>
    </div>
  `).join('');
}

// 10. AUDIT LOGS
async function pollAuditLogs() {
  try {
    const res = await fetch('/api/audit_logs');
    const data = await res.json();
    document.getElementById('audit-log-list').innerHTML = data.logs.map(l => `
      <div class="log-row">
        <span class="log-time">[${l.time}]</span>
        <span class="log-mod">${l.module}:</span>
        <span class="log-msg">${l.message}</span>
      </div>
    `).join('');
  } catch (e) {
    // offline
  }
}

document.getElementById('btn-clear-logs').addEventListener('click', () => {
  document.getElementById('audit-log-list').innerHTML = '<div style="color:var(--text-dim);">Logs cleared.</div>';
});
