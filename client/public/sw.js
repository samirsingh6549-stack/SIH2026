/**
 * SIH 2026: Landslide Early Warning & Risk Monitoring System (NER)
 * Service Worker (PWA Offline Capability & Asset Caching)
 */

const CACHE_NAME = 'ner-landslide-cache-v1';

const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/app.css',
  '/src/app.js',
  '/src/db.js',
  '/src/syncManager.js',
  '/manifest.json'
];

// Install Event: Cache Core Static Shell
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installing and caching app shell...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clear Stale Caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activating new service worker...');
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Purging old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Cache-First for Assets, Network-First for API with Fallback
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // If requesting backend API, attempt network first, fallback to cached error
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(JSON.stringify({
          error: 'Offline',
          message: 'Device currently disconnected. Request served from offline boundary.'
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }

  // For static app shell assets: Cache-First, fallback to network
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });
        return networkResponse;
      });
    })
  );
});

// Background Sync (Triggered when browser regains connection)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-field-reports') {
    console.log('[ServiceWorker] Background Sync event triggered: sync-field-reports');
    // Notify clients to invoke syncManager
    event.waitUntil(
      self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          client.postMessage({ type: 'TRIGGER_BACKGROUND_SYNC' });
        });
      })
    );
  }
});
