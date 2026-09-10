/**
 * SIH 2026: Landslide Early Warning & Risk Monitoring System (NER)
 * Client UI Controller (app.js)
 * 
 * Coordinates:
 *  - Network simulation toggle
 *  - Form submission -> SyncManager -> IndexedDB -> Cloud
 *  - Real-time rendering of Outbox cards
 *  - Downstream offline cache rendering
 */

import { localDb } from './db.js';
import { syncManager } from './syncManager.js';

// DOM Elements
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const simOfflineToggle = document.getElementById('sim-offline-toggle');
const toggleDesc = document.getElementById('toggle-desc');
const hazardForm = document.getElementById('hazard-form');
const presetLocation = document.getElementById('preset_location');
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');
const outboxList = document.getElementById('outbox-list');
const pendingBadge = document.getElementById('pending-badge');
const syncedBadge = document.getElementById('synced-badge');
const btnForceSync = document.getElementById('btn-force-sync');
const btnClearHistory = document.getElementById('btn-clear-history');
const btnRefreshCache = document.getElementById('btn-refresh-cache');
const cachedAlertsList = document.getElementById('cached-alerts-list');
const cachedZonesList = document.getElementById('cached-zones-list');

// --- INITIALIZATION ---

async function initApp() {
  // 1. Register Service Worker for PWA asset caching
  if ('serviceWorker' in navigator) {
    try {
      const reg = await navigator.serviceWorker.register('/sw.js');
      console.log('[App] ServiceWorker registered with scope:', reg.scope);
    } catch (err) {
      console.warn('[App] ServiceWorker registration failed:', err);
    }
  }

  // 2. Initialize UI State
  updateNetworkStatusUI(syncManager.isOnline());
  await renderOutboxList();
  await renderCachedData();

  // 3. Initial Downstream Cache Fetch
  syncManager.fetchAndCacheDownstreamData();

  // 4. Subscribe to SyncManager events
  syncManager.subscribe((type, data) => {
    console.log(`[Event: ${type}]`, data);
    updateNetworkStatusUI(syncManager.isOnline());
    renderOutboxList();

    if (type === 'risk-zones-cached' || type === 'alerts-cached') {
      renderCachedData();
    }
  });

  setupEventListeners();
}

// --- EVENT LISTENERS ---

function setupEventListeners() {
  // Dead Zone Simulation Toggle (Judges Demo Mode)
  simOfflineToggle.addEventListener('change', (e) => {
    const isSimulated = e.target.checked;
    syncManager.setSimulatedOffline(isSimulated);
    toggleDesc.textContent = isSimulated ? 'FORCE OFFLINE (Dead Zone)' : 'Auto (Real Network)';
    toggleDesc.style.color = isSimulated ? 'var(--danger)' : 'var(--primary)';
  });

  // Preset Location Selector
  presetLocation.addEventListener('change', (e) => {
    const [lat, lng] = e.target.value.split(',');
    latitudeInput.value = lat;
    longitudeInput.value = lng;
  });

  // Form Submit (Offline-First)
  hazardForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const reportData = {
      reporter_name: document.getElementById('reporter_name').value,
      reporter_role: document.getElementById('reporter_role').value,
      hazard_type: document.getElementById('hazard_type').value,
      severity: document.getElementById('severity').value,
      latitude: latitudeInput.value,
      longitude: longitudeInput.value,
      notes: document.getElementById('notes').value
    };

    try {
      await syncManager.submitFieldReport(reportData);
      await renderOutboxList();
      alert(`Report saved! Status: ${syncManager.isOnline() ? 'Transmitted to Cloud' : 'Queued in Offline Outbox'}`);
    } catch (err) {
      alert('Error saving report: ' + err.message);
    }
  });

  // Force Sync Button
  btnForceSync.addEventListener('click', async () => {
    if (!syncManager.isOnline()) {
      alert('Cannot sync: Device is currently in an offline dead zone. Switch to Online mode first.');
      return;
    }
    btnForceSync.disabled = true;
    btnForceSync.textContent = '⏳ Syncing...';
    await syncManager.syncPendingReports();
    btnForceSync.disabled = false;
    btnForceSync.textContent = '🔄 Trigger Sync Now';
    await renderOutboxList();
  });

  // Refresh Downstream Cache Button
  btnRefreshCache.addEventListener('click', async () => {
    btnRefreshCache.textContent = '⏳ Loading...';
    await syncManager.fetchAndCacheDownstreamData();
    await renderCachedData();
    btnRefreshCache.textContent = '📥 Refresh Cache';
  });

  // Clear Synced Reports
  btnClearHistory.addEventListener('click', async () => {
    const all = await localDb.getAllReports();
    const db = await localDb.getDb();
    const tx = db.transaction('outbox_reports', 'readwrite');
    const store = tx.objectStore('outbox_reports');

    all.filter(r => r.status === 'SYNCED').forEach(r => {
      store.delete(r.client_id);
    });

    tx.oncomplete = () => {
      renderOutboxList();
    };
  });
}

// --- UI RENDERING HELPERS ---

function updateNetworkStatusUI(isOnline) {
  if (isOnline) {
    statusDot.className = 'status-dot online';
    statusText.textContent = 'ONLINE (Connected to Cloud)';
    statusText.style.color = 'var(--success)';
  } else {
    statusDot.className = 'status-dot offline';
    statusText.textContent = 'OFFLINE (Mountain Dead Zone)';
    statusText.style.color = 'var(--danger)';
  }
}

async function renderOutboxList() {
  const reports = await localDb.getAllReports();

  const pendingCount = reports.filter(r => r.status === 'PENDING_SYNC').length;
  const syncedCount = reports.filter(r => r.status === 'SYNCED').length;

  pendingBadge.textContent = `${pendingCount} Pending`;
  syncedBadge.textContent = `${syncedCount} Synced`;

  if (!reports || reports.length === 0) {
    outboxList.innerHTML = `<div class="empty-state">No field reports in local storage. Submit a report on the left to see the sync lifecycle!</div>`;
    return;
  }

  // Sort by newest first
  reports.sort((a, b) => new Date(b.local_created_at) - new Date(a.local_created_at));

  outboxList.innerHTML = reports.map(r => {
    const isPending = r.status === 'PENDING_SYNC';
    const statusClass = isPending ? 'pending' : 'synced';
    const statusLabel = isPending ? '⏳ PENDING SYNC' : '✅ SYNCED TO CLOUD';

    const severityColor = 
      r.severity === 'CRITICAL' ? 'badge-danger' : 
      r.severity === 'HIGH' ? 'badge-warning' : 'badge-success';

    return `
      <div class="report-item-card">
        <div class="report-item-header">
          <span class="hazard-title">${escapeHtml(r.hazard_type)}</span>
          <span class="badge ${severityColor}">${escapeHtml(r.severity)}</span>
        </div>
        <div class="report-uuid">ID: ${r.client_id}</div>
        <div class="report-item-body">
          <div><strong>Reporter:</strong> ${escapeHtml(r.reporter_name)} (${escapeHtml(r.reporter_role)})</div>
          <div><strong>Location:</strong> ${r.latitude.toFixed(4)}, ${r.longitude.toFixed(4)}</div>
          <div><strong>Notes:</strong> ${escapeHtml(r.notes || 'None')}</div>
        </div>
        <div class="report-item-footer">
          <span>Captured: ${new Date(r.local_created_at).toLocaleTimeString()}</span>
          <span class="status-badge ${statusClass}">${statusLabel}</span>
        </div>
      </div>
    `;
  }).join('');
}

async function renderCachedData() {
  // Render Alerts
  const alerts = await localDb.getCachedAlerts();
  if (!alerts || alerts.length === 0) {
    cachedAlertsList.innerHTML = `<div class="empty-state">No alerts cached locally.</div>`;
  } else {
    cachedAlertsList.innerHTML = alerts.map(a => `
      <div class="cache-item">
        <div class="cache-item-title">
          <span>${escapeHtml(a.headline)}</span>
          <span class="badge badge-danger">${escapeHtml(a.severity)}</span>
        </div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">
          ${escapeHtml(a.instructions)}
        </div>
      </div>
    `).join('');
  }

  // Render Risk Zones
  const zones = await localDb.getCachedRiskZones();
  if (!zones || zones.length === 0) {
    cachedZonesList.innerHTML = `<div class="empty-state">No risk zones cached locally.</div>`;
  } else {
    cachedZonesList.innerHTML = zones.map(z => {
      const color = z.risk_level === 'CRITICAL' ? 'badge-danger' : 
                    z.risk_level === 'HIGH' ? 'badge-warning' : 'badge-success';
      return `
        <div class="cache-item">
          <div class="cache-item-title">
            <span>${escapeHtml(z.zone_name)}</span>
            <span class="badge ${color}">${escapeHtml(z.risk_level)} (${z.risk_score})</span>
          </div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">
            District: ${escapeHtml(z.district)}, ${escapeHtml(z.state)}
          </div>
        </div>
      `;
    }).join('');
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Start
initApp();
