import { localDb } from './db.js';
import { syncManager } from './syncManager.js';
import { LANGUAGES, TRANSLATIONS, getTranslation } from './i18n.js';

export async function submitReport(reportData) {
  return syncManager.saveReport(reportData);
}

export async function syncNow() {
  return syncManager.syncPending();
}

export async function getLocalReports() {
  return localDb.getAllReports();
}

export async function getCachedRiskZones() {
  return localDb.getCachedRiskZones();
}

export async function getCachedAlerts() {
  return localDb.getCachedAlerts();
}

export function onSyncEvent(callback) {
  return syncManager.subscribe(callback);
}

export function isOnline() {
  return syncManager.isOnline();
}

export function setSimulatedOffline(isOffline) {
  syncManager.setOfflineMode(isOffline);
}

export { syncManager, localDb, LANGUAGES, TRANSLATIONS, getTranslation };
