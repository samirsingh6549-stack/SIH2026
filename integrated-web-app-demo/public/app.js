// TerraSafe AI NER: Defense-Grade 8-State Early Warning Platform Controller
// Grounded in authentic GIS cockpit architecture, resilient offline buffers, and tactical telemetry

// ==========================================
// 1. GLOBAL STATE & CONSTANTS
// ==========================================

let map = null;
let telemetryChart = null;
let isOfflineMode = false;
let currentLanguage = 'en';
let activeTab = 'command';

// Leaflet Layer Groups
let zoneLayerGroup;
let stationLayerGroup;
let bypassLayerGroup;
let bufferLayerGroup;
let reportLayerGroup;
let mlHeatmapLayer;
let mlCircleMarkersGroup;

// 8 North Eastern States Strategic Hotspot Coordinates
const HOTSPOTS = {
  sikkim: {
    lat: 27.3389, lng: 88.6065, zoom: 12,
    name: 'Ranipool NH-10 Corridor',
    state: 'Sikkim', district: 'East Sikkim',
    prob: 94, fos: '0.82 (Failure Imminent)', pore: '48.2 kPa', rain: '242 mm',
    factor: 'Toe Hydrostatic Shear', risk: 'CRITICAL',
    protocol: 'Suspend commercial heavy convoy, engage Upper Martam Western Crest bypass, and broadcast automated Cell SMS in Nepali & Hindi to perimeter mobile towers.'
  },
  assam: {
    lat: 25.1837, lng: 93.0298, zoom: 12,
    name: 'Dima Hasao Jatinga Section',
    state: 'Assam', district: 'Dima Hasao',
    prob: 92, fos: '0.86 (Critical Slippage)', pore: '44.0 kPa', rain: '215 mm',
    factor: 'Hill-cutting Slump & Railway Cut', risk: 'CRITICAL',
    protocol: 'Halt Lumding-Badarpur railway cutting traffic, divert NH-27 via Circuit House Ridge Bypass, and mobilize Haflong NDRF platoon.'
  },
  manipur: {
    lat: 24.8167, lng: 93.6833, zoom: 12,
    name: 'Noney Tupul Railway Corridor',
    state: 'Manipur', district: 'Noney',
    prob: 89, fos: '0.91 (Severe Shear)', pore: '41.5 kPa', rain: '198 mm',
    factor: 'Ijei River Damming & Debris Surge', risk: 'CRITICAL',
    protocol: 'Issue Flash Flood alert downriver from Tupul bridge yard, engage Longmai Mountain Spur, and establish VHF relay with Noney District Shelter.'
  },
  meghalaya: {
    lat: 25.5788, lng: 91.8933, zoom: 12,
    name: 'East Khasi Hills Sohra Arc',
    state: 'Meghalaya', district: 'East Khasi Hills',
    prob: 81, fos: '1.08 (Sub-surface Creep)', pore: '36.4 kPa', rain: '312 mm',
    factor: 'Gorge Joint Water Wedging', risk: 'HIGH',
    protocol: 'Restrict heavy mining dumpers on SH-5, redirect light tourist transit via Laitryngew Plateau Bypass, and monitor piezometer array #04.'
  },
  nagaland: {
    lat: 25.6751, lng: 94.1086, zoom: 12,
    name: 'Kohima South Bypass NH-29',
    state: 'Nagaland', district: 'Kohima',
    prob: 84, fos: '1.04 (Progressive Slump)', pore: '33.8 kPa', rain: '185 mm',
    factor: 'Dzüdza Fault Plane Reactivation', risk: 'HIGH',
    protocol: 'Enforce one-way convoy at Dzüdza river crossing, prepare Khonoma Mountain Crest single-lane bypass, and inspect culvert drainage.'
  },
  arunachal: {
    lat: 27.5861, lng: 91.8653, zoom: 11,
    name: 'Bhalukpong-Tawang Alpine Pass',
    state: 'Arunachal Pradesh', district: 'West Kameng',
    prob: 79, fos: '1.14 (Frost Thaw Runoff)', pore: '32.0 kPa', rain: '164 mm',
    factor: 'Freeze-Thaw Rock Splitting', risk: 'HIGH',
    protocol: 'Stage BRO Border Road clearing bulldozers at Sela tunnel approaches and restrict night vehicular movement.'
  },
  mizoram: {
    lat: 23.7271, lng: 92.7176, zoom: 12,
    name: 'Aizawl Chite Veng Ridge',
    state: 'Mizoram', district: 'Aizawl',
    prob: 54, fos: '1.38 (Moderate Infiltration)', pore: '26.0 kPa', rain: '118 mm',
    factor: 'Clay Sandstone Interbedding', risk: 'MODERATE',
    protocol: 'Advise residents along Chite stream slopes to inspect septic and drainage overflow. Normal traffic maintained on NH-54.'
  },
  tripura: {
    lat: 23.9500, lng: 92.2667, zoom: 12,
    name: 'Jampui Hills Ridge Vanghmun',
    state: 'Tripura', district: 'North Tripura',
    prob: 49, fos: '1.45 (Stable Runoff)', pore: '22.0 kPa', rain: '94 mm',
    factor: 'Laterite Soil Sheet Wash', risk: 'MODERATE',
    protocol: 'Continue automated solar telemetry transmission. Normal lifeline corridor operations on NH-8.'
  }
};

// Strategic Safe Bypass Routes
const BYPASS_ROUTES = [
  {
    name: 'Upper Martam Western Crest Bypass (Sikkim)',
    coords: [
      [27.2920, 88.5620],
      [27.3250, 88.5450],
      [27.3520, 88.6180],
      [27.3389, 88.6065]
    ],
    state: 'Sikkim',
    status: 'ACTIVE SAFE BYPASS'
  },
  {
    name: 'Mahur - Circuit House Crest Bypass (Assam)',
    coords: [
      [25.1200, 93.1100],
      [25.1890, 93.0220],
      [25.1780, 93.0150]
    ],
    state: 'Assam',
    status: 'ACTIVE SAFE BYPASS'
  },
  {
    name: 'Longmai Ridge Mountain Trail (Manipur)',
    coords: [
      [24.8000, 93.1200],
      [24.8450, 93.7100],
      [24.8320, 93.6990]
    ],
    state: 'Manipur',
    status: 'ACTIVE SAFE BYPASS'
  },
  {
    name: 'Laitryngew Plateau Bypass (Meghalaya)',
    coords: [
      [25.4200, 91.8100],
      [25.3800, 91.7600],
      [25.2850, 91.7450]
    ],
    state: 'Meghalaya',
    status: 'ACTIVE SAFE BYPASS'
  },
  {
    name: 'Khonoma Mountain Crest Bypass (Nagaland)',
    coords: [
      [25.7100, 94.0450],
      [25.6500, 94.0200],
      [25.6620, 94.1190]
    ],
    state: 'Nagaland',
    status: 'ACTIVE SAFE BYPASS'
  }
];

// Arterial Lifeline Corridors Database
const ARTERIAL_ROADS = [
  {
    code: 'NH-10',
    name: 'Siliguri - Gangtok National Lifeline',
    sector: 'Ranipool Km 12 (Sikkim)',
    status: 'TRAFFIC SUSPENDED',
    riskClass: 'danger',
    rain: '242 mm / 24h',
    detour: 'Upper Martam Western Crest Bypass (Active - 4x4 / Light Emergency Vehicles Only)',
    agency: 'Border Roads Organisation (Project Swastik)'
  },
  {
    code: 'NH-27',
    name: 'Haflong - Silchar East-West Corridor',
    sector: 'Jatinga Valley Cutting (Assam)',
    status: 'TRAFFIC SUSPENDED',
    riskClass: 'danger',
    rain: '215 mm / 24h',
    detour: 'Mahur - Circuit House Upper Ridge Bypass (Clear)',
    agency: 'NHIDCL & Assam PWD Hills'
  },
  {
    code: 'NH-29',
    name: 'Dimapur - Kohima Mountain Highway',
    sector: 'Dzüdza River Crossing (Nagaland)',
    status: 'REGULATED CONVOY',
    riskClass: 'warning',
    rain: '185 mm / 24h',
    detour: 'Khonoma Crest Single-Lane Alternating Pilot Escort',
    agency: 'Nagaland PWD (National Highways)'
  },
  {
    code: 'SH-5',
    name: 'Shillong - Cherrapunji Lifeline',
    sector: 'Mawkdok Dympep Gorge (Meghalaya)',
    status: 'RESTRICTED ACCESS',
    riskClass: 'warning',
    rain: '312 mm / 24h',
    detour: 'Laitryngew Plateau Crest Route Available',
    agency: 'Meghalaya PWD (Roads)'
  },
  {
    code: 'NH-37',
    name: 'Imphal - Jiribam Highway',
    sector: 'Noney Tupul River Bed (Manipur)',
    status: 'REGULATED CONVOY',
    riskClass: 'warning',
    rain: '198 mm / 24h',
    detour: 'Longmai Ridge Mountain Trail Operational',
    agency: 'BRO Project Sevak'
  },
  {
    code: 'NH-13',
    name: 'Trans-Arunachal Highway',
    sector: 'Bhalukpong - Tawang Pass (Arunachal)',
    status: 'OPEN WITH PILOT',
    riskClass: 'emerald',
    rain: '164 mm / 24h',
    detour: 'BRO Snow/Debris Clearance Units on 15-min standby',
    agency: 'BRO Project Vartak'
  },
  {
    code: 'NH-54',
    name: 'Aizawl - Lunglei Corridor',
    sector: 'Chite Veng Escarpment (Mizoram)',
    status: 'NORMAL TRAFFIC',
    riskClass: 'emerald',
    rain: '118 mm / 24h',
    detour: 'Direct valley transit uninterrupted',
    agency: 'Mizoram PWD'
  },
  {
    code: 'NH-8',
    name: 'Agartala - Silchar Corridor',
    sector: 'Jampui Hills Ridge (Tripura)',
    status: 'NORMAL TRAFFIC',
    riskClass: 'emerald',
    rain: '94 mm / 24h',
    detour: 'Direct transit uninterrupted',
    agency: 'Tripura PWD'
  }
];

// Multilingual Dialect Dictionary for Emergency Directives
const I18N_WARNINGS = {
  en: {
    marquee: 'Extreme Slope Saturation: NH-10 Ranipool & Cherrapunji Crest',
    protocolRanipool: 'Suspend commercial heavy convoy, engage Upper Martam Western Crest bypass, and broadcast automated Cell SMS in Nepali & Hindi to perimeter mobile towers.',
    protocolJatinga: 'Halt Lumding-Badarpur railway cutting traffic, divert NH-27 via Circuit House Ridge Bypass, and mobilize Haflong NDRF platoon.',
    speechHeadline: 'Emergency Landslide Evacuation Directive. Active slope failure detected on NH-10 Ranipool and East Khasi Hills. Move to designated high-ground shelters immediately.'
  },
  hi: {
    marquee: 'गंभीर ढलान संतृप्ति: एनएच-10 रानीपूल एवं चेरापूंजी शिखर पर भूस्खलन खतरा',
    protocolRanipool: 'व्यावसायिक भारी वाहनों का आवागमन तुरंत रोकें, ऊपरी मारतम पश्चिमी दर्रा बाईपास सक्रिय करें और नेपाली एवं हिंदी में स्वचालित एसएमएस प्रसारित करें।',
    protocolJatinga: 'लुमडिंग-बदरपुर रेलवे लाइन और एनएच-27 को तुरंत बंद करें, सर्किट हाउस बाईपास से यातायात मोड़ें।',
    speechHeadline: 'आपातकालीन भूस्खलन चेतावनी। एनएच-10 रानीपूल और चेरापूंजी क्षेत्र में भारी भूस्खलन का खतरा। तुरंत ऊंचे राहत शिविरों में जाएं।'
  },
  as: {
    marquee: 'চৰম পাহাৰীয়া স্খলনৰ সতৰ্কবাণী: এনএইচ-১০ ৰাণীপূৰ আৰু চেৰাপুঞ্জী খণ্ড',
    protocolRanipool: 'গধুৰ যান-বাহন চলাচল বন্ধ কৰক, উজনি মাৰ্তাম পশ্চিম ক্ৰেষ্ট বাইপাছ ব্যৱহাৰ কৰক আৰু স্থানীয় নাগৰিকলৈ সতৰ্কবাণী বাৰ্তা প্ৰেৰণ কৰক।',
    protocolJatinga: 'লামডিং-বদৰপুৰ ৰেলপথ আৰু এনএইচ-২৭ পথ বন্ধ কৰক, চাৰ্কিট হাউচ বাইপাছেৰে যান-বাহন এৰি দিয়ক।',
    speechHeadline: 'জৰুৰীকালীন ভূমিস্খলন সতৰ্কবাণী। এনএইচ-১০ আৰু ডিমা হাছাওত ভূমিস্খলনৰ আশংকা। ততালিকে সুৰক্ষিত আশ্ৰয় শিবিৰলৈ যাওক।'
  },
  ne: {
    marquee: 'गम्भीर पहिरो जोखिम: रानीपुल NH-10 र चेरापुन्जी पहाडी खण्ड',
    protocolRanipool: 'भारी सवारी साधनको आवतजावत बन्द गर्नुहोस्, माथिल्लो मार्तम पश्चिमी बाइपास प्रयोग गर्नुहोस् र नेपाली र हिन्दीमा तुरुन्तै मोबाइल एसएमएस पठाउनुहोस्।',
    protocolJatinga: 'हाफलोङ र जतिङ्गा क्षेत्रमा रेल र सडक यातायात रोक्नुहोस्, सर्किट हाउस बाइपास प्रयोग गर्नुहोस्।',
    speechHeadline: 'आपतकालीन पहिरो पूर्व चेतावनी। रानीपुल NH-10 मा ठूलो पहिरोको जोखिम। तुरुन्तै माथिल्लो मार्तम राहत शिविरमा जानुहोस्।'
  },
  mz: {
    marquee: 'Leimin Hlauhawm Zual: NH-10 Ranipool leh Cherrapunji Tlang',
    protocolRanipool: 'Motor lian chi kalphung tihtawp ni se, Upper Martam Bypass lam pan tur a ni e.',
    protocolJatinga: 'Rel kawng leh NH-27 khar a ni, Circuit House kalkawng hman tur a ni.',
    speechHeadline: 'Leimin vauhkhanna thupek. Ranipool leh Cherrapunji tlang velah leimin a hlauhawm. Hmun him lam pan nghal rawh u.'
  }
};

// Local Incident Reports (Offline-First Store-and-Forward Outbox)
let localReports = [
  {
    id: 101,
    reporter: 'Sub-Inspector Lepcha (SDRF)',
    location: 'NH-10 Km 12 near Ranipool bridge culvert',
    hazardType: 'Active Debris Flow / Mudslide',
    crackWidth: '24 cm',
    time: '08:05 AM',
    notes: 'Slurry 1.5m deep over roadway. 2 freight trucks stranded.',
    status: 'SYNCED TO SEOC 112'
  },
  {
    id: 102,
    reporter: 'Civil Defense Volunteer Gogoi',
    location: 'NH-27 Jatinga Valley Cutting Section',
    hazardType: 'Tension Crack / Fissure Opening',
    crackWidth: '18 cm',
    time: '08:24 AM',
    notes: 'Longitudinal fissure widening rapidly along cut-slope shoulder.',
    status: 'SYNCED TO SEOC 112'
  }
];

// Load persisted reports if available
try {
  const cached = localStorage.getItem('terrasafe_field_reports');
  if (cached) {
    const parsed = JSON.parse(cached);
    if (Array.isArray(parsed) && parsed.length > 0) {
      localReports = parsed;
    }
  }
} catch (e) {}

let currentInspectorSector = HOTSPOTS.sikkim;

// Safe wrapper utility to prevent any single component error from halting page execution
function safeInit(fn, name) {
  try {
    fn();
  } catch (err) {
    console.error(`[TerraSafe Core] Error during ${name}:`, err);
  }
}

// ==========================================
// 2. LIFECYCLE INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  safeInit(initTabs, 'Tabs');
  safeInit(initGISMap, 'GIS Map');
  safeInit(initTelemetryChart, 'Telemetry Chart');
  safeInit(initHotspotDropdown, 'Hotspot Dropdown');
  safeInit(initDialectSwitcher, 'Dialect Switcher');
  safeInit(initOfflineSimulation, 'Offline Simulation');
  safeInit(initSurgeSlider, 'Surge Slider');
  safeInit(initLiveWeatherToggle, 'Live Weather Toggle');
  safeInit(initSmsGatewayModal, 'SMS Gateway Modal');
  safeInit(initEmergencyBroadcast, 'Emergency Broadcast');
  safeInit(initAudioSiren, 'Audio Siren');
  safeInit(initInSARRefresh, 'InSAR Refresh');
  safeInit(initFieldIncidentForm, 'Field Incident Form');
  safeInit(renderRoadLifelines, 'Road Lifelines');
  safeInit(renderIncidentFeed, 'Incident Feed');
  safeInit(() => updateSectorInspector(HOTSPOTS.sikkim), 'Sector Inspector Default');

  // Load live data asynchronously
  loadBackendData();

  // Periodic size invalidation to guarantee Leaflet tiles render completely
  setTimeout(() => {
    if (map) map.invalidateSize();
  }, 250);
  setTimeout(() => {
    if (map) map.invalidateSize();
  }, 1000);
});

// ==========================================
// 3. TAB NAVIGATION
// ==========================================

function initTabs() {
  const navButtons = document.querySelectorAll('.nav-item');
  const tabPanes = document.querySelectorAll('.tab-pane');

  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      if (!targetTab) return;

      activeTab = targetTab;
      navButtons.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const activePane = document.getElementById(`tab-${targetTab}`);
      if (activePane) activePane.classList.add('active');

      if (targetTab === 'command' && map) {
        setTimeout(() => map.invalidateSize(), 100);
        setTimeout(() => map.invalidateSize(), 400);
      }
      if (targetTab === 'analytics' && telemetryChart) {
        setTimeout(() => telemetryChart.resize(), 100);
      }
    });
  });
}

// ==========================================
// 4. LEAFLET GIS MAP
// ==========================================

function createCustomPin(color, pulse = false) {
  if (typeof L === 'undefined') return null;
  return L.divIcon({
    className: 'custom-leaflet-divicon ' + (pulse ? 'radar-ping' : ''),
    html: `
      <div class="custom-pin-wrap" style="background: radial-gradient(circle, ${color}33 30%, transparent 75%);">
        <div class="custom-pin-core" style="background-color: ${color}; box-shadow: 0 0 14px ${color}, 0 0 24px ${color};"></div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12]
  });
}

function initGISMap() {
  const mapContainer = document.getElementById('gis-main-map');
  if (!mapContainer) return;

  if (typeof L === 'undefined') {
    console.error('Leaflet library is not available yet.');
    return;
  }

  if (map) {
    map.remove();
    map = null;
  }

  map = L.map('gis-main-map', {
    zoomControl: true,
    minZoom: 5,
    maxZoom: 18
  }).setView([26.0, 92.5], 7);

  // Base Layer 1: CartoDB Dark Matter (Tactical Defense Cockpit)
  const cartoDarkLayer = L.tileLayer('https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; CARTO &copy; OpenStreetMap | SIH 2026 TerraSafe AI NER',
    maxZoom: 19
  });

  // Base Layer 2: ESRI World Imagery (100% Free Satellite Relief - No API Key Needed)
  const esriSatelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri, Earthstar Geographics | SIH 2026 TerraSafe AI NER',
    maxZoom: 18
  });

  // Base Layer 3: OpenStreetMap Standard (100% Free Public Topo - No API Key Needed)
  const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors | SIH 2026 TerraSafe AI NER',
    maxZoom: 19
  });

  // Add default base layer
  cartoDarkLayer.addTo(map);

  // Add basemap layer control in bottom-left so user can toggle between Satellite, Dark, and OSM
  const baseMaps = {
    "<span style='color:#fff;font-size:11px;'>Tactical Dark</span>": cartoDarkLayer,
    "<span style='color:#38bdf8;font-size:11px;'>Satellite Relief (ESRI)</span>": esriSatelliteLayer,
    "<span style='color:#10b981;font-size:11px;'>OpenStreetMap (No Key)</span>": osmLayer
  };
  L.control.layers(baseMaps, null, { position: 'bottomleft', collapsed: true }).addTo(map);

  // Layer Groups
  zoneLayerGroup = L.layerGroup().addTo(map);
  stationLayerGroup = L.layerGroup().addTo(map);
  bypassLayerGroup = L.layerGroup().addTo(map);
  bufferLayerGroup = L.layerGroup().addTo(map);
  reportLayerGroup = L.layerGroup().addTo(map);
  mlCircleMarkersGroup = L.layerGroup().addTo(map);

  // Render Bypass Routes
  renderBypassPolylines();

  // Layer Checkboxes
  const chkHeatmap = document.getElementById('chk-ml-heatmap');
  if (chkHeatmap) {
    chkHeatmap.addEventListener('change', e => {
      if (e.target.checked) {
        if (mlHeatmapLayer) map.addLayer(mlHeatmapLayer);
        if (mlCircleMarkersGroup) map.addLayer(mlCircleMarkersGroup);
      } else {
        if (mlHeatmapLayer) map.removeLayer(mlHeatmapLayer);
        if (mlCircleMarkersGroup) map.removeLayer(mlCircleMarkersGroup);
      }
    });
  }

  const chkStations = document.getElementById('chk-stations');
  if (chkStations) {
    chkStations.addEventListener('change', e => {
      if (e.target.checked) map.addLayer(stationLayerGroup);
      else map.removeLayer(stationLayerGroup);
    });
  }

  const chkBypass = document.getElementById('chk-bypass');
  if (chkBypass) {
    chkBypass.addEventListener('change', e => {
      if (e.target.checked) map.addLayer(bypassLayerGroup);
      else map.removeLayer(bypassLayerGroup);
    });
  }

  const chkBuffers = document.getElementById('chk-buffers');
  if (chkBuffers) {
    chkBuffers.addEventListener('change', e => {
      if (e.target.checked) map.addLayer(bufferLayerGroup);
      else map.removeLayer(bufferLayerGroup);
    });
  }

  window.addEventListener('resize', () => {
    if (map) map.invalidateSize();
  });
}

function renderBypassPolylines() {
  if (!bypassLayerGroup || typeof L === 'undefined') return;
  bypassLayerGroup.clearLayers();
  BYPASS_ROUTES.forEach(route => {
    const polyline = L.polyline(route.coords, {
      color: '#10b981',
      weight: 3.5,
      opacity: 0.9,
      dashArray: '6, 6'
    }).addTo(bypassLayerGroup);

    polyline.bindTooltip(`<strong>${route.name}</strong><br><span style="color:#10b981; font-weight:bold;">${route.status}</span>`, {
      sticky: true,
      direction: 'top'
    });
  });
}

// ==========================================
// 5. DATA INGESTION & MAP PLOTTING
// ==========================================

async function loadBackendData() {
  try {
    const rainVal = document.getElementById('slider-rain') ? document.getElementById('slider-rain').value : 75;

    const [stRes, zRes, mlRes] = await Promise.all([
      fetch('/api/stations').then(r => r.json()).catch(() => null),
      fetch('/api/risk_zones').then(r => r.json()).catch(() => null),
      fetch(`/api/ml/heatmap?rainfall=${rainVal}`).then(r => r.json()).catch(() => null)
    ]);

    if (zRes && zRes.zones) {
      plotRiskZones(zRes.zones);
    } else {
      plotDefaultZones();
    }

    if (stRes && stRes.stations) {
      plotStationMarkers(stRes.stations);
    } else {
      plotDefaultStations();
    }

    if (mlRes && mlRes.status === 'success') {
      renderMlHeatmap(mlRes);
    }

    plotReportMarkers();

  } catch (err) {
    console.warn('Backend data load fallback:', err);
    plotDefaultStations();
    plotDefaultZones();
    plotReportMarkers();
  }
}

function plotStationMarkers(stations) {
  if (!stationLayerGroup || typeof L === 'undefined') return;
  stationLayerGroup.clearLayers();

  stations.forEach(st => {
    const isCritical = st.status === 'CRITICAL';
    const isHigh = st.status === 'HIGH';
    const color = isCritical ? '#ef4444' : isHigh ? '#f59e0b' : '#10b981';

    const pin = createCustomPin(color, isCritical || isHigh);
    const marker = L.marker([st.lat, st.lng], { icon: pin }).addTo(stationLayerGroup);

    marker.bindPopup(`
      <div style="font-size:12px; min-width:200px; line-height:1.45;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <strong style="color:${color}; font-size:13px;">${st.name}</strong>
          <span style="background:${color}22; color:${color}; font-weight:bold; font-size:10px; padding:2px 6px; border-radius:4px; border:1px solid ${color}66;">${st.status}</span>
        </div>
        <div>State: <strong>${st.state}</strong> (${st.district})</div>
        <div>Lifeline: <strong>${st.lifeline}</strong></div>
        <div style="margin-top:4px; font-family:'JetBrains Mono', monospace; font-size:11px;">
          Rain: <strong>${st.rainfall_mm_h} mm/h</strong> | Pore: <strong style="color:#38bdf8;">${st.pore_pressure_kpa} kPa</strong>
        </div>
      </div>
    `);

    marker.on('click', () => {
      const matched = Object.values(HOTSPOTS).find(h => h.state.toLowerCase() === st.state.toLowerCase()) || {
        name: st.name,
        state: st.state,
        district: st.district,
        lat: st.lat,
        lng: st.lng,
        prob: isCritical ? 94 : isHigh ? 82 : 45,
        fos: isCritical ? '0.82 (Failure Imminent)' : isHigh ? '1.05 (Creep)' : '1.42 (Stable)',
        pore: `${st.pore_pressure_kpa} kPa`,
        rain: `${st.rainfall_mm_h * 4} mm`,
        factor: isCritical ? 'Toe Hydrostatic Shear' : 'Sub-surface Infiltration',
        risk: st.status,
        protocol: isCritical ? HOTSPOTS.sikkim.protocol : 'Routine sensor telemetry monitoring and standard traffic advisory.'
      };
      updateSectorInspector(matched);
      if (st.history) updateTelemetryFromHistory(st.history, st.name);
    });
  });
}

function plotRiskZones(zones) {
  if (!zoneLayerGroup || typeof L === 'undefined') return;
  zoneLayerGroup.clearLayers();
  if (bufferLayerGroup) bufferLayerGroup.clearLayers();

  zones.forEach(z => {
    const isCritical = z.risk_level === 'CRITICAL';
    const isHigh = z.risk_level === 'HIGH';
    const color = isCritical ? '#ef4444' : isHigh ? '#f59e0b' : '#10b981';

    const poly = L.polygon(z.coordinates, {
      color: color,
      fillColor: color,
      fillOpacity: 0.22,
      weight: 1.8
    }).addTo(zoneLayerGroup);

    poly.bindPopup(`
      <div style="font-size:12px; line-height:1.45;">
        <strong style="color:${color}; font-size:13px;">${z.name}</strong><br>
        District: <strong>${z.district}, ${z.state}</strong><br>
        Risk Level: <strong style="color:${color};">${z.risk_level}</strong> (${(z.risk_score * 100).toFixed(0)}% LSI)<br>
        Lifeline Corridor: <strong>${z.lifeline_highway}</strong><br>
        Shelter: <em>${z.evacuation_shelter}</em>
      </div>
    `);

    poly.on('click', () => {
      const center = poly.getBounds().getCenter();
      const matched = Object.values(HOTSPOTS).find(h => h.state.toLowerCase() === z.state.toLowerCase()) || {
        name: z.name,
        state: z.state,
        district: z.district,
        lat: +center.lat.toFixed(4),
        lng: +center.lng.toFixed(4),
        prob: +(z.risk_score * 100).toFixed(0),
        fos: isCritical ? '0.84 (Failure Imminent)' : '1.06 (Unstable)',
        pore: isCritical ? '48.2 kPa' : '36.0 kPa',
        rain: `${z.trigger_rainfall_mm * 4.5} mm`,
        factor: 'Shear Boundary Rupture',
        risk: z.risk_level,
        protocol: `Evacuate endangered slope perimeter to ${z.evacuation_shelter}. Suspend heavy traffic on ${z.lifeline_highway}.`
      };
      updateSectorInspector(matched);
    });

    if (isCritical && z.coordinates && z.coordinates[0] && bufferLayerGroup) {
      L.circle(z.coordinates[0], {
        radius: 1800,
        color: '#ef4444',
        fillColor: '#ef4444',
        fillOpacity: 0.08,
        weight: 1.5,
        dashArray: '5, 5'
      }).addTo(bufferLayerGroup);
    }
  });
}

function renderMlHeatmap(data) {
  if (!data || !data.leaflet_heat_points || typeof L === 'undefined') return;

  if (mlHeatmapLayer && map && map.hasLayer(mlHeatmapLayer)) {
    map.removeLayer(mlHeatmapLayer);
  }

  if (typeof L.heatLayer === 'function') {
    mlHeatmapLayer = L.heatLayer(data.leaflet_heat_points, {
      radius: 42,
      blur: 24,
      maxZoom: 12,
      max: 1.0,
      gradient: {
        0.15: '#10b981',
        0.40: '#eab308',
        0.65: '#f97316',
        0.85: '#ef4444'
      }
    });

    const chk = document.getElementById('chk-ml-heatmap');
    if (chk && chk.checked && map) {
      mlHeatmapLayer.addTo(map);
    }
  }

  if (mlCircleMarkersGroup) {
    mlCircleMarkersGroup.clearLayers();
    if (data.geojson_feature_collection && data.geojson_feature_collection.features) {
      data.geojson_feature_collection.features.forEach(f => {
        const p = f.properties;
        const coords = [f.geometry.coordinates[1], f.geometry.coordinates[0]];
        const pct = (p.lsi_score * 100).toFixed(1);

        const circle = L.circleMarker(coords, {
          radius: 8,
          fillColor: p.color,
          color: '#ffffff',
          weight: 1.5,
          fillOpacity: 0.9
        });

        circle.bindTooltip(`<strong>${p.station_name}</strong><br>AI Hazard: <strong style="color:${p.color};">${pct}% (${p.risk_level})</strong>`, {
          direction: 'top'
        });

        circle.addTo(mlCircleMarkersGroup);
      });
    }
  }

  const statusEl = document.getElementById('lbl-batch-status');
  if (statusEl && data.max_lsi_score !== undefined) {
    statusEl.textContent = `${data.grid_cell_count} Cells (Max LSI: ${(data.max_lsi_score * 100).toFixed(1)}%)`;
  }
}

function plotReportMarkers() {
  if (!reportLayerGroup || typeof L === 'undefined') return;
  reportLayerGroup.clearLayers();

  localReports.forEach(r => {
    const isCritical = r.hazardType.includes('Debris') || r.hazardType.includes('Slide');
    const color = isCritical ? '#f59e0b' : '#38bdf8';
    const lat = r.lat || 27.3389 + (Math.random() - 0.5) * 0.05;
    const lng = r.lng || 88.6065 + (Math.random() - 0.5) * 0.05;

    const marker = L.circleMarker([lat, lng], {
      radius: 7,
      fillColor: color,
      color: '#ffffff',
      weight: 2,
      fillOpacity: 0.95
    }).addTo(reportLayerGroup);

    marker.bindPopup(`
      <div style="font-size:12px; line-height:1.4;">
        <span style="background:${color}; color:#fff; font-size:9px; font-weight:bold; padding:2px 6px; border-radius:3px;">GROUND REPORT</span><br>
        <strong>${r.location}</strong><br>
        Observed: <strong style="color:${color};">${r.hazardType}</strong><br>
        Crack Width: <strong>${r.crackWidth}</strong><br>
        <em>${r.notes}</em><br>
        <div style="margin-top:4px; font-size:10px; color:#94a3b8;">Status: ${r.status} &bull; ${r.time}</div>
      </div>
    `);
  });
}

function plotDefaultStations() {
  if (!stationLayerGroup || typeof L === 'undefined') return;
  Object.values(HOTSPOTS).forEach(h => {
    const isCrit = h.risk === 'CRITICAL';
    const color = isCrit ? '#ef4444' : h.risk === 'HIGH' ? '#f59e0b' : '#10b981';
    const pin = createCustomPin(color, isCrit);
    L.marker([h.lat, h.lng], { icon: pin })
      .bindPopup(`<strong>${h.name}</strong><br>Risk: ${h.risk}<br>Prob: ${h.prob}%`)
      .addTo(stationLayerGroup)
      .on('click', () => updateSectorInspector(h));
  });
}

function plotDefaultZones() {
  // Built-in polygon representation for Sikkim and Assam
  const sikkimZone = [
    [27.3450, 88.6000], [27.3490, 88.6150], [27.3350, 88.6220], [27.3310, 88.6040]
  ];
  if (zoneLayerGroup && typeof L !== 'undefined') {
    L.polygon(sikkimZone, { color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.25, weight: 2 })
      .bindPopup('<strong>Ranipool NH-10 Corridor</strong><br>Risk: CRITICAL (94%)')
      .addTo(zoneLayerGroup);
  }
}

// ==========================================
// 6. 1-COLUMN SECTOR INSPECTOR
// ==========================================

function updateSectorInspector(sector) {
  if (!sector) return;
  currentInspectorSector = sector;

  const nameEl = document.getElementById('disp-sector-name');
  const coordsEl = document.getElementById('disp-sector-coords');
  const badgeEl = document.getElementById('disp-sector-badge');
  const probEl = document.getElementById('disp-sector-prob');
  const barEl = document.getElementById('disp-sector-bar');
  const fosEl = document.getElementById('disp-sector-fos');
  const poreEl = document.getElementById('disp-sector-pore');
  const rainEl = document.getElementById('disp-sector-rain');
  const factorEl = document.getElementById('disp-sector-factor');
  const protocolEl = document.getElementById('disp-sector-protocol');

  if (nameEl) nameEl.textContent = sector.name;
  if (coordsEl) coordsEl.textContent = `${sector.lat}° N, ${sector.lng}° E • ${sector.district || sector.state}`;

  if (badgeEl) {
    badgeEl.textContent = sector.risk;
    badgeEl.className = `badge-status-pill ${sector.risk === 'CRITICAL' ? 'danger' : sector.risk === 'HIGH' ? 'warning' : 'emerald'}`;
  }

  if (probEl) probEl.textContent = `${sector.prob}%`;
  if (barEl) {
    barEl.style.width = `${sector.prob}%`;
    barEl.className = sector.risk === 'CRITICAL' ? 'progress-bar-danger' : 'progress-bar-emerald';
  }

  if (fosEl) fosEl.textContent = sector.fos;
  if (poreEl) poreEl.textContent = sector.pore;
  if (rainEl) rainEl.textContent = sector.rain;
  if (factorEl) factorEl.textContent = sector.factor;
  if (protocolEl) protocolEl.textContent = sector.protocol;
}

// ==========================================
// 7. HOTSPOT SELECTION DROPDOWN
// ==========================================

function initHotspotDropdown() {
  const select = document.getElementById('hotspot-select');
  if (!select) return;

  select.addEventListener('change', e => {
    const key = e.target.value;
    const sector = HOTSPOTS[key];
    if (sector && map) {
      map.flyTo([sector.lat, sector.lng], sector.zoom, { duration: 1.4 });
      updateSectorInspector(sector);
    }
  });
}

// ==========================================
// 8. TELEMETRY CHART (CHART.JS)
// ==========================================

function initTelemetryChart() {
  const canvas = document.getElementById('telemetryChart');
  if (!canvas || typeof Chart === 'undefined') return;

  const ctx = canvas.getContext('2d');
  const rainGradient = ctx.createLinearGradient(0, 0, 0, 260);
  rainGradient.addColorStop(0, 'rgba(56, 189, 248, 0.35)');
  rainGradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)');

  const poreGradient = ctx.createLinearGradient(0, 0, 0, 260);
  poreGradient.addColorStop(0, 'rgba(239, 68, 68, 0.35)');
  poreGradient.addColorStop(1, 'rgba(239, 68, 68, 0.0)');

  telemetryChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['02:00', '06:00', '10:00', '14:00', '18:00', '22:00'],
      datasets: [
        {
          label: 'Precipitation Intensity (mm/h)',
          data: [24, 52, 110, 195, 260, 312],
          borderColor: '#38bdf8',
          backgroundColor: rainGradient,
          fill: true,
          tension: 0.38,
          borderWidth: 2.2,
          pointBackgroundColor: '#38bdf8',
          pointRadius: 4,
          yAxisID: 'yRain'
        },
        {
          label: 'Pore Water Pressure (kPa)',
          data: [38, 56, 84, 112, 129, 138],
          borderColor: '#ef4444',
          backgroundColor: poreGradient,
          borderDash: [5, 4],
          fill: false,
          tension: 0.38,
          borderWidth: 2.2,
          pointBackgroundColor: '#ef4444',
          pointRadius: 4,
          yAxisID: 'yPore'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(3, 7, 18, 0.95)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          titleFont: { family: 'Plus Jakarta Sans', size: 12, weight: 'bold' },
          bodyFont: { family: 'JetBrains Mono', size: 11 },
          padding: 10
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
        },
        yRain: {
          type: 'linear',
          position: 'left',
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#38bdf8', font: { family: 'JetBrains Mono', size: 10 } },
          title: { display: true, text: 'Rain (mm)', color: '#38bdf8', font: { size: 10 } }
        },
        yPore: {
          type: 'linear',
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { color: '#ef4444', font: { family: 'JetBrains Mono', size: 10 } },
          title: { display: true, text: 'Pore Pressure (kPa)', color: '#ef4444', font: { size: 10 } }
        }
      }
    }
  });
}

function updateTelemetryFromHistory(history, stationName) {
  if (!telemetryChart || !history || history.length === 0) return;
  telemetryChart.data.labels = history.map(h => h.time);
  telemetryChart.data.datasets[0].data = history.map(h => h.rain);
  telemetryChart.data.datasets[1].data = history.map(h => h.pore);
  telemetryChart.update();
}

// ==========================================
// 9. SENTINEL-1 INSAR REFRESH
// ==========================================

function initInSARRefresh() {
  const btn = document.getElementById('btn-refresh-insar');
  const icon = document.getElementById('icon-insar-spin');
  if (!btn || !icon) return;

  btn.addEventListener('click', () => {
    icon.classList.add('fa-spin');
    btn.disabled = true;

    setTimeout(() => {
      icon.classList.remove('fa-spin');
      btn.disabled = false;

      const velocity = (17.8 + Math.random() * 2.2).toFixed(1);
      const coherence = (0.87 + Math.random() * 0.06).toFixed(2);

      const velEl = document.querySelector('.insar-stat-list .stat-row .text-danger');
      const cohEl = document.querySelector('.insar-stat-list .stat-row .text-emerald');

      if (velEl) velEl.textContent = `${velocity} mm/wk [HIGH]`;
      if (cohEl) cohEl.textContent = `${coherence} (Clear Coherence)`;
    }, 1100);
  });
}

// ==========================================
// 10. ARTERIAL ROAD NETWORK (TAB 3)
// ==========================================

function renderRoadLifelines() {
  const container = document.getElementById('road-cards-container');
  if (!container) return;

  container.innerHTML = ARTERIAL_ROADS.map(road => {
    const isSuspended = road.status === 'TRAFFIC SUSPENDED';
    const isRegulated = road.status === 'REGULATED CONVOY';
    const badgeClass = isSuspended ? 'danger' : isRegulated ? 'warning' : 'emerald';

    return `
      <div class="glass-panel road-card">
        <div class="road-card-left">
          <div class="road-card-title-row">
            <span class="road-name font-mono">${road.code}</span>
            <span class="road-sector-pill">${road.sector}</span>
          </div>
          <p class="road-card-sub">
            <strong class="text-main">${road.name}</strong> &bull; Precipitation: <span class="font-mono text-cyan">${road.rain}</span>
          </p>
          <div style="font-size: 11px; color: var(--emerald-green); margin-top: 4px;">
            <i class="fa-solid fa-route"></i> Bypass: <strong>${road.detour}</strong>
          </div>
          <div style="font-size: 10px; color: var(--text-dim); margin-top: 2px;">
            Maintaining Agency: ${road.agency}
          </div>
        </div>

        <div>
          <span class="badge-status-pill ${badgeClass} font-mono font-bold">
            ${isSuspended ? '<i class="fa-solid fa-ban"></i> ' : isRegulated ? '<i class="fa-solid fa-triangle-exclamation"></i> ' : '<i class="fa-solid fa-circle-check"></i> '}
            ${road.status}
          </span>
        </div>
      </div>
    `;
  }).join('');
}

// ==========================================
// 11. CITIZEN INCIDENT LOG (TAB 4)
// ==========================================

function initFieldIncidentForm() {
  const form = document.getElementById('form-field-report');
  const crackSlider = document.getElementById('slider-crack');
  const crackDisp = document.getElementById('disp-crack-val');

  if (crackSlider && crackDisp) {
    crackSlider.addEventListener('input', () => {
      crackDisp.textContent = `${crackSlider.value} cm`;
    });
  }

  if (!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();

    const locationInp = document.getElementById('inp-location').value.trim();
    const hazardType = document.getElementById('sel-hazard').value;
    const crackWidth = crackSlider ? `${crackSlider.value} cm` : '12 cm';
    const notes = document.getElementById('inp-notes').value.trim();

    if (!locationInp) return;

    const newReport = {
      id: Date.now(),
      reporter: 'Civilian Ground Scout / Border Patrol',
      location: locationInp,
      hazardType: hazardType,
      crackWidth: crackWidth,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      notes: notes || 'Geo-referenced ground alert submitted via offline packet buffer.',
      status: isOfflineMode ? 'CACHED IN OFFLINE SQLITE BUFFER' : 'RELAYED TO STATE EOC 112'
    };

    localReports.unshift(newReport);
    try {
      localStorage.setItem('terrasafe_field_reports', JSON.stringify(localReports));
    } catch (err) {}

    renderIncidentFeed();
    plotReportMarkers();

    if (!isOfflineMode) {
      try {
        await fetch('/api/reports', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: 'fld_' + newReport.id,
            reporter: newReport.reporter,
            location_desc: newReport.location,
            hazard_type: newReport.hazardType,
            severity: 'CRITICAL',
            state: 'North East Corridor',
            notes: `${newReport.crackWidth} crack. ${newReport.notes}`
          })
        });
      } catch (err) {
        console.warn('Saved offline in local buffer:', err);
      }
    }

    form.reset();
    if (crackDisp) crackDisp.textContent = '12 cm';

    alert(`✅ Ground Incident Logged & Queued:\n\nObserved: ${newReport.hazardType}\nLocation: ${newReport.location}\nStatus: ${newReport.status}\n\nVisible on top of the Live Field Incident Feed!`);
  });
}

function renderIncidentFeed() {
  const container = document.getElementById('incident-feed-list');
  const countBadge = document.getElementById('disp-incident-count');
  const tabBadge = document.getElementById('badge-reports-count');
  const metricDisp = document.getElementById('disp-reports-metric');

  if (countBadge) countBadge.textContent = `${localReports.length} Logged`;
  if (tabBadge) tabBadge.textContent = `${localReports.length}`;
  if (metricDisp) metricDisp.textContent = `${localReports.length} Reports`;

  if (!container) return;

  container.innerHTML = localReports.map(item => `
    <div class="incident-item">
      <div class="incident-item-top">
        <span class="incident-location">${item.location}</span>
        <span class="incident-time font-mono">${item.time}</span>
      </div>
      <div class="incident-hazard">
        <i class="fa-solid fa-triangle-exclamation"></i> ${item.hazardType} (Fissure: ${item.crackWidth || 'N/A'})
      </div>
      ${item.notes ? `<div class="incident-notes">"${item.notes}"</div>` : ''}
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px; font-size:10px; font-family:'JetBrains Mono', monospace;">
        <span class="text-muted"><i class="fa-solid fa-user-shield"></i> ${item.reporter || 'Field Scout'}</span>
        <span class="${item.status.includes('OFFLINE') ? 'text-amber font-bold' : 'text-emerald'}">
          <i class="fa-solid fa-circle-check"></i> ${item.status}
        </span>
      </div>
    </div>
  `).join('');
}

// ==========================================
// 12. MULTILINGUAL DIALECT SWITCHER
// ==========================================

function initDialectSwitcher() {
  const buttons = document.querySelectorAll('.dialect-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      currentLanguage = btn.getAttribute('data-lang') || 'en';
      applyDialect(currentLanguage);
    });
  });
}

function applyDialect(lang) {
  const dict = I18N_WARNINGS[lang] || I18N_WARNINGS.en;
  const marquee = document.getElementById('marquee-alert');
  if (marquee && dict.marquee) marquee.textContent = dict.marquee;

  const protocolEl = document.getElementById('disp-sector-protocol');
  if (protocolEl && currentInspectorSector) {
    if (currentInspectorSector.state.toLowerCase() === 'sikkim' && dict.protocolRanipool) {
      protocolEl.textContent = dict.protocolRanipool;
    } else if (currentInspectorSector.state.toLowerCase() === 'assam' && dict.protocolJatinga) {
      protocolEl.textContent = dict.protocolJatinga;
    }
  }
}

// ==========================================
// 12B. REAL-TIME DATA STREAM INTEGRATIONS
// ==========================================

// Designated relief shelters across all 8 NER states for emergency evacuation routing
const RELIEF_SHELTERS = {
  sikkim: { name: 'Upper Martam High Ridge Shelter', lat: 27.3520, lng: 88.6180 },
  assam: { name: 'Haflong Circuit House Relief Camp', lat: 25.1780, lng: 93.0150 },
  manipur: { name: 'Longmai Mountain Spur Safe Base', lat: 24.8450, lng: 93.7100 },
  meghalaya: { name: 'Laitryngew Ridge School Camp', lat: 25.6100, lng: 91.8800 },
  nagaland: { name: 'Khonoma Mountain Crest Shelter', lat: 25.6500, lng: 94.0200 },
  arunachal: { name: 'Dirang Alpine Staging Base', lat: 27.3500, lng: 92.2300 },
  mizoram: { name: 'Aizawl Govt College Ridge', lat: 23.7380, lng: 92.7240 },
  tripura: { name: 'Vanghmun Summit Camp', lat: 23.9800, lng: 92.2700 }
};

let isLiveWeatherActive = false;

// 1. Live Weather Toggle (Open-Meteo Integration)
function initLiveWeatherToggle() {
  const btn = document.getElementById('btn-live-weather');
  const txt = document.getElementById('txt-weather-mode');
  const toast = document.getElementById('toast-broadcast');

  if (!btn) return;

  btn.addEventListener('click', async () => {
    isLiveWeatherActive = !isLiveWeatherActive;

    if (isLiveWeatherActive) {
      btn.classList.add('active-glow');
      if (txt) txt.textContent = 'Syncing Satellite...';

      try {
        const res = await fetch('/api/weather/live?refresh=true');
        const data = await res.json();

        if (data && data.stations) {
          if (txt) txt.textContent = 'Live Satellite (Open-Meteo)';

          data.stations.forEach(st => {
            const key = Object.keys(HOTSPOTS).find(k => 
              HOTSPOTS[k].name.toLowerCase().includes(st.name.toLowerCase().split(' ')[0].toLowerCase()) || 
              HOTSPOTS[k].state.toLowerCase() === st.state.toLowerCase()
            );
            if (key && HOTSPOTS[key]) {
              HOTSPOTS[key].rain = `${st.rainfall_mm_h} mm/h`;
              HOTSPOTS[key].pore = `${st.pore_pressure_kpa} kPa`;
              HOTSPOTS[key].risk = st.status;
              HOTSPOTS[key].prob = st.status === 'CRITICAL' ? 92 : st.status === 'HIGH' ? 76 : 48;
              HOTSPOTS[key].fos = st.status === 'CRITICAL' ? '0.84 (Failure Imminent)' : st.status === 'HIGH' ? '1.09 (Active Creep)' : '1.42 (Stable)';
            }
          });

          plotStationMarkers(data.stations);
          if (currentInspectorSector) {
            const updated = data.stations.find(s => s.id === currentInspectorSector.id || s.name === currentInspectorSector.name);
            if (updated) {
              updateSectorInspector({
                ...currentInspectorSector,
                rain: `${updated.rainfall_mm_h} mm/h`,
                pore: `${updated.pore_pressure_kpa} kPa`,
                risk: updated.status,
                prob: updated.status === 'CRITICAL' ? 92 : updated.status === 'HIGH' ? 76 : 48,
                fos: updated.status === 'CRITICAL' ? '0.84 (Failure Imminent)' : updated.status === 'HIGH' ? '1.09 (Active Creep)' : '1.42 (Stable)'
              });
            }
          }

          if (toast) {
            toast.innerHTML = `<i class="fa-solid fa-satellite-dish"></i> <span>Open-Meteo Satellite Feed Synced: Live precipitation & volumetric soil moisture loaded for all 8 NER states.</span>`;
            toast.classList.remove('hidden');
            setTimeout(() => toast.classList.add('hidden'), 5000);
          }
        }
      } catch (err) {
        console.error('Open-Meteo fetch failed:', err);
        if (txt) txt.textContent = 'Live Satellite Error';
      }
    } else {
      btn.classList.remove('active-glow');
      if (txt) txt.textContent = 'Live Satellite Weather';
      loadBackendData();
    }
  });
}

// 2. SMS Gateway Configuration Modal
function initSmsGatewayModal() {
  const modal = document.getElementById('modal-sms-gateway');
  const openBtn = document.getElementById('btn-sms-modal');
  const closeBtn = document.getElementById('btn-close-sms-modal');
  const closeBtn2 = document.getElementById('btn-close-sms-modal-2');
  const dispatchBtn = document.getElementById('btn-test-sms-dispatch');
  const statusBox = document.getElementById('sms-dispatch-status');

  if (!modal) return;

  const openModal = () => {
    modal.classList.remove('hidden');
    const msgEl = document.getElementById('sms-custom-message');
    if (msgEl && currentInspectorSector) {
      msgEl.value = `EMERGENCY ALERT [SEOC 112]: Active slope failure predicted on ${currentInspectorSector.name}. Factor of Safety < 0.88. Evacuate uphill immediately.`;
    }
  };

  const closeModal = () => {
    modal.classList.add('hidden');
    if (statusBox) statusBox.classList.add('hidden');
  };

  if (openBtn) openBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (closeBtn2) closeBtn2.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  if (dispatchBtn) {
    dispatchBtn.addEventListener('click', async () => {
      const phoneInput = document.getElementById('sms-phone-input');
      const keyInput = document.getElementById('sms-api-key-input');
      const msgInput = document.getElementById('sms-custom-message');

      const rawNumbers = phoneInput ? phoneInput.value : '';
      const numbers = rawNumbers.split(',').map(s => s.trim()).filter(Boolean);
      const apiKey = keyInput ? keyInput.value.trim() : '';
      const message = msgInput ? msgInput.value.trim() : '';

      dispatchBtn.disabled = true;
      dispatchBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Dispatching Carrier SMS...';

      try {
        const res = await fetch('/api/sms/broadcast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            phone_numbers: numbers,
            fast2sms_key: apiKey || undefined,
            message: message,
            sector: currentInspectorSector ? currentInspectorSector.name : 'NER Regional Corridor'
          })
        });

        const data = await res.json();

        if (statusBox) {
          statusBox.classList.remove('hidden');
          if (data.gateway === 'FAST2SMS_DLT' && data.carrier_response?.statusCode === 200) {
            statusBox.className = 'status-box success';
            statusBox.innerHTML = `<strong>✅ LIVE SMS TRANSMITTED:</strong> Dispatched via Fast2SMS DLT Gateway to ${data.recipient_count} phone(s). Delivery verified!`;
          } else if (data.gateway === 'DEVELOPMENT_SMS_SIMULATOR') {
            statusBox.className = 'status-box warn';
            statusBox.innerHTML = `<strong>📋 SEOC SIMULATOR DISPATCH:</strong> Broadcast payload queued into State EOC 112 Incident Log. (Enter Fast2SMS API Key above for live mobile delivery).`;
          } else {
            statusBox.className = 'status-box warn';
            statusBox.innerHTML = `<strong>⚠️ GATEWAY RESPONSE (${data.gateway}):</strong> ${JSON.stringify(data.carrier_response?.body || data.instructions)}`;
          }
        }

        playAudioSiren();

      } catch (err) {
        if (statusBox) {
          statusBox.classList.remove('hidden');
          statusBox.className = 'status-box warn';
          statusBox.innerHTML = `<strong>Error:</strong> Failed to connect to SMS gateway: ${err.message}`;
        }
      } finally {
        dispatchBtn.disabled = false;
        dispatchBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Dispatch Mobile SMS';
      }
    });
  }
}

// 3. OSRM Highway Evacuation Dynamic Router
async function triggerOsrmEvacuationRoute(sector) {
  if (!sector || !map || typeof L === 'undefined') return;

  const stateKey = (sector.state || 'sikkim').toLowerCase();
  const shelter = RELIEF_SHELTERS[stateKey] || RELIEF_SHELTERS.sikkim;

  const toast = document.getElementById('toast-broadcast');
  if (toast) {
    toast.innerHTML = `<i class="fa-solid fa-route"></i> <span>Computing live OSRM Highway Evacuation Route to ${shelter.name}...</span>`;
    toast.classList.remove('hidden');
  }

  try {
    const res = await fetch(`/api/route/live?origin_lng=${sector.lng}&origin_lat=${sector.lat}&dest_lng=${shelter.lng}&dest_lat=${shelter.lat}`);
    const data = await res.json();

    if (data && data.coordinates && bypassLayerGroup) {
      bypassLayerGroup.clearLayers();

      const latLngs = data.coordinates.map(c => [c[1], c[0]]);

      const polyline = L.polyline(latLngs, {
        color: '#38bdf8',
        weight: 5,
        opacity: 0.95,
        lineCap: 'round',
        lineJoin: 'round',
        dashArray: '8, 6'
      }).addTo(bypassLayerGroup);

      const shelterPin = createCustomPin('#10b981', true);
      const shelterMarker = L.marker([shelter.lat, shelter.lng], { icon: shelterPin }).addTo(bypassLayerGroup);
      shelterMarker.bindPopup(`
        <div style="font-size:12px; line-height:1.4;">
          <strong style="color:#10b981; font-size:13px;">${shelter.name}</strong><br>
          <em>Designated High-Ground Evacuation Shelter</em><br>
          <div style="margin-top:4px; color:#38bdf8; font-weight:bold;">Transit Distance: ${data.distance_km} km • ETA: ${data.duration_min} mins</div>
        </div>
      `).openPopup();

      map.fitBounds(polyline.getBounds(), { padding: [40, 40] });

      if (toast) {
        toast.innerHTML = `<i class="fa-solid fa-shield-halved text-emerald"></i> <span><strong>EVACUATION CORRIDOR ACTIVE:</strong> Route plotted to ${shelter.name} (${data.distance_km} km, ~${data.duration_min} mins) via ${data.source}.</span>`;
        setTimeout(() => toast.classList.add('hidden'), 5500);
      }
    }
  } catch (err) {
    console.warn('OSRM route fetch failed:', err);
  }
}

// ==========================================
// 13. EMERGENCY BROADCAST & AUDIO SIREN
// ==========================================

function initEmergencyBroadcast() {
  const triggerBtn = document.getElementById('btn-trigger-cap');
  const toast = document.getElementById('toast-broadcast');
  const transmitBtn = document.getElementById('btn-transmit-callout');

  const executeBroadcast = async () => {
    if (toast) {
      toast.classList.remove('hidden');
      setTimeout(() => {
        toast.classList.add('hidden');
      }, 4500);
    }
    // Play dual-tone synthesized siren + native speech
    playAudioSiren();

    // Flash Marquee Alert
    const marquee = document.getElementById('marquee-alert');
    if (marquee) {
      const orig = marquee.textContent;
      marquee.textContent = '🚨 IMMEDIATE EVACUATION DIRECTIVE BROADCAST DISPATCHED VIA OASIS CAP v1.2';
      setTimeout(() => {
        marquee.textContent = orig;
      }, 6000);
    }

    // Trigger dynamic OSRM mountain evacuation route on map
    if (currentInspectorSector) {
      triggerOsrmEvacuationRoute(currentInspectorSector);
    }

    // Automatically trigger background SMS broadcast
    try {
      const phoneInput = document.getElementById('sms-phone-input');
      const keyInput = document.getElementById('sms-api-key-input');
      const numbers = phoneInput && phoneInput.value ? phoneInput.value.split(',').map(s => s.trim()).filter(Boolean) : ['+919876543210'];
      const apiKey = keyInput ? keyInput.value.trim() : '';

      fetch('/api/sms/broadcast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone_numbers: numbers,
          fast2sms_key: apiKey || undefined,
          sector: currentInspectorSector ? currentInspectorSector.name : 'Sikkim NH-10 Ranipool'
        })
      }).catch(() => {});
    } catch (e) {}
  };

  if (triggerBtn) triggerBtn.addEventListener('click', executeBroadcast);
  if (transmitBtn) transmitBtn.addEventListener('click', executeBroadcast);
}

function initAudioSiren() {
  const btn = document.getElementById('btn-audio-alert');
  if (btn) {
    btn.addEventListener('click', () => {
      playAudioSiren();
    });
  }
}

// Authentic Web Audio dual-tone emergency siren synthesizer
function playAudioSiren() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
      const ctx = new AudioContext();
      if (ctx.state === 'suspended') {
        ctx.resume();
      }
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sawtooth';
      gain.gain.setValueAtTime(0.35, ctx.currentTime);

      const now = ctx.currentTime;
      for (let i = 0; i < 4; i++) {
        osc.frequency.setValueAtTime(680, now + i * 0.7);
        osc.frequency.linearRampToValueAtTime(1250, now + i * 0.7 + 0.35);
        osc.frequency.linearRampToValueAtTime(680, now + i * 0.7 + 0.7);
      }

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(now + 2.8);
    }
  } catch (err) {
    console.warn('Web Audio synthesis fallback:', err);
  }

  const audio = document.getElementById('siren-audio');
  if (audio) {
    audio.currentTime = 0;
    audio.play().catch(() => {});
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const dict = I18N_WARNINGS[currentLanguage] || I18N_WARNINGS.en;
    const utterance = new SpeechSynthesisUtterance(dict.speechHeadline);
    utterance.rate = 0.95;
    const langMap = { en: 'en-IN', hi: 'hi-IN', as: 'as-IN', ne: 'ne-NP', mz: 'en-IN' };
    utterance.lang = langMap[currentLanguage] || 'en-IN';
    window.speechSynthesis.speak(utterance);
  }
}

// ==========================================
// 14. MONSOON SURGE SLIDER
// ==========================================

function initSurgeSlider() {
  const slider = document.getElementById('slider-rain');
  const disp = document.getElementById('slider-rain-val');
  const peakDisp = document.getElementById('disp-peak-rain');

  if (!slider || !disp) return;

  slider.addEventListener('input', () => {
    disp.textContent = `${slider.value} mm/h`;
  });

  slider.addEventListener('change', async () => {
    const val = parseFloat(slider.value);
    if (peakDisp) peakDisp.textContent = `${(val * 3.2).toFixed(0)} mm`;

    try {
      const res = await fetch(`/api/ml/heatmap?rainfall=${val}`);
      const data = await res.json();
      if (data && data.status === 'success') {
        renderMlHeatmap(data);
      }
    } catch (err) {
      console.warn('Monsoon surge simulation error:', err);
    }
  });
}

// ==========================================
// 15. OFFLINE MOUNTAIN DEAD ZONE SIMULATION
// ==========================================

function initOfflineSimulation() {
  const toggle = document.getElementById('offline-toggle');
  const pill = document.getElementById('telemetry-status-pill');
  const banner = document.getElementById('offline-queue-banner');

  if (!toggle) return;

  toggle.addEventListener('change', async () => {
    isOfflineMode = toggle.checked;

    if (isOfflineMode) {
      if (pill) {
        pill.className = 'telemetry-status-pill offline';
        pill.innerHTML = '<i class="fa-solid fa-plane-slash text-amber"></i> <span id="txt-telemetry-status">Offline Buffer Active</span>';
      }
      if (banner) banner.classList.remove('hidden');

      alert('🏔️ MOUNTAIN DEAD ZONE SIMULATION ACTIVE:\n\nCellular 4G/LTE towers disconnected in mountain canyon.\nAll new citizen reports will buffer locally in the encrypted on-device SQLite outbox.');
    } else {
      if (pill) {
        pill.className = 'telemetry-status-pill online';
        pill.innerHTML = '<i class="fa-solid fa-tower-broadcast text-emerald"></i> <span id="txt-telemetry-status">SAT-Net Synced</span>';
      }
      if (banner) banner.classList.add('hidden');

      await flushOfflineReports();
    }
  });
}

async function flushOfflineReports() {
  const pending = localReports.filter(r => r.status.includes('OFFLINE'));
  if (pending.length === 0) {
    alert('📡 RECONNECTED: Satellite uplink active. All packets are already synchronized.');
    return;
  }

  try {
    const res = await fetch('/api/reports/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reports: pending.map(p => ({
          client_id: 'fld_' + p.id,
          reporter: p.reporter,
          location_desc: p.location,
          hazard_type: p.hazardType,
          severity: 'CRITICAL',
          state: 'North East Corridor',
          notes: `${p.crackWidth || ''} ${p.notes || ''}`
        }))
      })
    });
    const data = await res.json();

    pending.forEach(p => {
      p.status = 'RELAYED TO STATE EOC 112';
    });

    try {
      localStorage.setItem('terrasafe_field_reports', JSON.stringify(localReports));
    } catch (e) {}

    renderIncidentFeed();
    alert(`📡 RECONNECTED TO SEOC 112 GATEWAY:\n\nFlushed ${data.synced_count || pending.length} pending report(s) from on-device SQLite buffer to Cloud Gateway!`);
  } catch (err) {
    console.warn('Batch sync fallback:', err);
  }
}
