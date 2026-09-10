import { localDb } from './db.js';

export class SyncEngine {
  constructor(options = {}) {
    this.offlineOverride = false;
    this.syncing = false;
    this.apiBase = options.apiBaseUrl || (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000');
    this.subscribers = new Set();

    if (typeof window !== 'undefined') {
      this._bindNetworkEvents();
      this._startHeartbeat();
    }
  }

  _bindNetworkEvents() {
    window.addEventListener('online', () => {
      this._emit('network-change', { isOnline: this.isOnline() });
      this.syncPending();
      this.pullLatest();
    });

    window.addEventListener('offline', () => {
      this._emit('network-change', { isOnline: false });
    });
  }

  isOnline() {
    if (this.offlineOverride) return false;
    return typeof navigator !== 'undefined' ? navigator.onLine : true;
  }

  setOfflineMode(forceOffline) {
    this.offlineOverride = Boolean(forceOffline);
    this._emit('network-change', { isOnline: this.isOnline() });

    if (this.isOnline()) {
      this.syncPending();
      this.pullLatest();
    }
  }

  // alias
  setSimulatedOffline(forceOffline) {
    this.setOfflineMode(forceOffline);
  }

  subscribe(fn) {
    this.subscribers.add(fn);
    return () => this.subscribers.delete(fn);
  }

  _emit(type, payload) {
    for (const sub of this.subscribers) {
      try {
        sub(type, payload);
      } catch (err) {
        console.error('listener error', err);
      }
    }
  }

  async saveReport(data) {
    const clientId = (typeof crypto !== 'undefined' && crypto.randomUUID)
      ? crypto.randomUUID()
      : 'fld_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8);

    const payload = {
      client_id: clientId,
      reporter_name: data.reporter_name || 'Ground Scout',
      reporter_role: data.reporter_role || 'Field Officer',
      reporter_phone: data.reporter_phone || '',
      hazard_type: data.hazard_type || 'Slope Crack',
      severity: data.severity || 'HIGH',
      latitude: Number(data.latitude) || 0,
      longitude: Number(data.longitude) || 0,
      location_description: data.location_description || '',
      affected_infrastructure: Array.isArray(data.affected_infrastructure) ? data.affected_infrastructure : [],
      notes: data.notes || '',
      local_created_at: new Date().toISOString()
    };

    await localDb.saveToOutbox(payload);
    this._emit('report-queued', payload);

    if (this.isOnline()) {
      this.syncPending();
    }

    return payload;
  }

  // alias
  async submitFieldReport(data) {
    return this.saveReport(data);
  }

  async syncPending() {
    if (this.syncing || !this.isOnline()) return;

    const pending = await localDb.getPendingReports();
    if (!pending.length) return;

    this.syncing = true;
    this._emit('sync-started', { count: pending.length });

    try {
      const res = await fetch(`${this.apiBase}/api/field_reports/batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reports: pending })
      });

      if (!res.ok) {
        throw new Error(`server returned ${res.status}`);
      }

      const body = await res.json();
      const syncedIds = body.synced_ids || [];

      await localDb.markBatchSynced(syncedIds);

      this._emit('sync-complete', {
        synced: body.synced_count || 0,
        duplicates: body.duplicate_count || 0,
        total: syncedIds.length
      });
    } catch (err) {
      console.warn('[sync] sync failed, will retry next interval:', err.message);
      this._emit('sync-failed', { error: err.message });
    } finally {
      this.syncing = false;
    }
  }

  // alias
  async syncPendingReports() {
    return this.syncPending();
  }

  async pullLatest() {
    if (!this.isOnline()) return;

    try {
      const [zonesRes, alertsRes] = await Promise.all([
        fetch(`${this.apiBase}/api/risk_zones`).catch(() => null),
        fetch(`${this.apiBase}/api/alerts`).catch(() => null)
      ]);

      if (zonesRes && zonesRes.ok) {
        const json = await zonesRes.json();
        if (json.data) {
          await localDb.cacheRiskZones(json.data);
          this._emit('risk-zones-cached', json.data);
        }
      }

      if (alertsRes && alertsRes.ok) {
        const json = await alertsRes.json();
        if (json.data) {
          await localDb.cacheAlerts(json.data);
          this._emit('alerts-cached', json.data);
        }
      }
    } catch (err) {
      // silent fail: offline cache will serve the client
    }
  }

  // alias
  async fetchAndCacheDownstreamData() {
    return this.pullLatest();
  }

  _startHeartbeat() {
    setInterval(() => {
      if (this.isOnline() && !this.syncing) {
        this.syncPending();
      }
    }, 20000);
  }
}

export const syncManager = new SyncEngine();
