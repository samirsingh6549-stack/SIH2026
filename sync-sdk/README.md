# Headless Offline Sync SDK
### SIH 2026: NER Landslide Risk Monitor

This folder is **completely decoupled from any UI**. Your frontend team can copy this `sync-sdk` folder into any frontend project (React, Next.js, Vue, Svelte, Flutter Web, or plain HTML/CSS) and use it immediately.

---

## How Your Frontend Teammate Uses This SDK

### 1. In React / Next.js / Vue
```javascript
import { 
  submitReport, 
  syncNow, 
  getLocalReports, 
  getCachedRiskZones, 
  onSyncEvent, 
  isOnline 
} from './sync-sdk';

// Inside your Form Submit handler:
async function handleSubmit(e) {
  e.preventDefault();
  
  // Saves to IndexedDB immediately, auto-syncs when online!
  const report = await submitReport({
    reporter_name: "Tashi Dorjee",
    reporter_role: "NDRF",
    hazard_type: "Rockfall",
    severity: "HIGH",
    latitude: 27.3389,
    longitude: 88.6065,
    notes: "Boulder roll blocking NH-10 near Ranipool"
  });

  alert(`Report saved! Unique ID: ${report.client_id}`);
}

// Listen to network & sync state to update UI badges:
useEffect(() => {
  const unsubscribe = onSyncEvent((event, data) => {
    if (event === 'network-change') {
      console.log('Online status:', data.isOnline);
    }
    if (event === 'sync-complete') {
      console.log('Synced records to cloud:', data.total_synced);
    }
  });

  return () => unsubscribe();
}, []);
```

---

### 2. Available Methods Reference

| Function | What it does |
| :--- | :--- |
| `submitReport(data)` | Saves report to device storage (offline-first) and triggers sync if online. |
| `syncNow()` | Manually forces an upload of all pending offline records. |
| `getLocalReports()` | Returns all reports on the device (for a "My Submissions" or "Outbox" list). |
| `getCachedRiskZones()` | Returns cached risk polygons/zones so maps render without internet. |
| `getCachedAlerts()` | Returns cached emergency evacuation guidelines. |
| `isOnline()` | Returns `true` if connected to cloud, `false` if in dead zone. |
| `onSyncEvent(cb)` | Subscribes to events: `'network-change'`, `'report-queued'`, `'sync-complete'`. |
| `setSimulatedOffline(bool)`| Toggles simulated dead zone for hackathon presentations. |
