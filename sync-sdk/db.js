// local indexeddb wrapper for offline storage
const DB_NAME = 'ner_landslide_db';
const DB_VERSION = 1;

class OfflineStorage {
  constructor() {
    this.db = null;
    this._ready = this._init();
  }

  async _init() {
    return new Promise((resolve, reject) => {
      const idb = typeof window !== 'undefined' ? window.indexedDB : globalThis.indexedDB;
      if (!idb) {
        return reject(new Error('IndexedDB not supported in this environment'));
      }

      const req = idb.open(DB_NAME, DB_VERSION);

      req.onupgradeneeded = (e) => {
        const db = e.target.result;

        // queue for reports taken while offline
        if (!db.objectStoreNames.contains('outbox')) {
          const outbox = db.createObjectStore('outbox', { keyPath: 'client_id' });
          outbox.createIndex('status', 'status', { unique: false });
          outbox.createIndex('created_at', 'local_created_at', { unique: false });
        }

        // cached risk zones for offline map view
        if (!db.objectStoreNames.contains('risk_zones')) {
          const zones = db.createObjectStore('risk_zones', { keyPath: 'zone_code' });
          zones.createIndex('risk_level', 'risk_level', { unique: false });
        }

        // cached evacuation alerts
        if (!db.objectStoreNames.contains('alerts')) {
          db.createObjectStore('alerts', { keyPath: 'id' });
        }
      };

      req.onsuccess = () => {
        this.db = req.result;
        resolve(this.db);
      };

      req.onerror = () => reject(req.error);
    });
  }

  async getDb() {
    if (!this.db) await this._ready;
    return this.db;
  }

  async saveToOutbox(report) {
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readwrite');
      const store = tx.objectStore('outbox');

      const record = {
        ...report,
        status: 'PENDING_SYNC',
        attempts: 0
      };

      const req = store.put(record);
      req.onsuccess = () => resolve(record);
      req.onerror = () => reject(req.error);
    });
  }

  // alias for backward compatibility
  async saveReportToOutbox(report) {
    return this.saveToOutbox(report);
  }

  async getPendingReports() {
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readonly');
      const store = tx.objectStore('outbox');
      const idx = store.index('status');
      const req = idx.getAll('PENDING_SYNC');

      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  }

  async getAllReports() {
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readonly');
      const req = tx.objectStore('outbox').getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  }

  async markBatchSynced(clientIds, serverTime) {
    if (!clientIds || clientIds.length === 0) return;
    const db = await this.getDb();

    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', 'readwrite');
      const store = tx.objectStore('outbox');
      const syncedAt = serverTime || new Date().toISOString();

      clientIds.forEach(id => {
        const getReq = store.get(id);
        getReq.onsuccess = () => {
          const item = getReq.result;
          if (item) {
            item.status = 'SYNCED';
            item.synced_at = syncedAt;
            store.put(item);
          }
        };
      });

      tx.oncomplete = () => resolve(true);
      tx.onerror = () => reject(tx.error);
    });
  }

  async cacheRiskZones(zones) {
    if (!zones || !zones.length) return;
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('risk_zones', 'readwrite');
      const store = tx.objectStore('risk_zones');
      zones.forEach(z => store.put(z));
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => reject(tx.error);
    });
  }

  async getCachedRiskZones() {
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('risk_zones', 'readonly');
      const req = tx.objectStore('risk_zones').getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  }

  async cacheAlerts(alerts) {
    if (!alerts || !alerts.length) return;
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('alerts', 'readwrite');
      const store = tx.objectStore('alerts');
      alerts.forEach(a => store.put(a));
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => reject(tx.error);
    });
  }

  async getCachedAlerts() {
    const db = await this.getDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('alerts', 'readonly');
      const req = tx.objectStore('alerts').getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  }
}

export const localDb = new OfflineStorage();
