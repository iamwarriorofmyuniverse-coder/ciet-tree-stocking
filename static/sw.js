/* ==============================================================================
 * CIET Coimbatore — Forest Conservation & Tree Stocking Service Worker (PWA)
 * Supports offline-first field ranger operation across campus sectors.
 * ============================================================================== */

const CACHE_NAME = 'ciet-forestry-v2.2';
const STATIC_ASSETS = [
    '/',
    '/static/manifest.json',
    '/static/offline.html',
    '/static/icons/icon-192.png',
    '/static/icons/icon-512.png',
    '/static/icons/icon-maskable.png',
    'https://cdn.tailwindcss.com',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://unpkg.com/html5-qrcode',
    'https://unpkg.com/lucide@latest'
];

// Install Event: Precache App Shell
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[CIET SW] Precaching app shell and offline assets...');
            return cache.addAll(STATIC_ASSETS).catch((err) => {
                console.warn('[CIET SW] Precache partial error (external CDN):', err);
            });
        }).then(() => self.skipWaiting())
    );
});

// Activate Event: Purge Stale Caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        console.log('[CIET SW] Removing obsolete cache:', key);
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event: Network-First with Cache Fallback for APIs & Offline Fallback for Pages
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Bypass non-GET requests (e.g. drone image uploads, QR scanning)
    if (request.method !== 'GET') {
        return;
    }

    // 1. Navigation requests (HTML pages)
    if (request.mode === 'navigate') {
        event.respondWith(
            fetch(request)
                .then((networkRes) => {
                    // Clone to cache
                    const resClone = networkRes.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, resClone));
                    return networkRes;
                })
                .catch(async () => {
                    const cachedRes = await caches.match(request);
                    if (cachedRes) return cachedRes;
                    // Fallback to offline page
                    return caches.match('/static/offline.html');
                })
        );
        return;
    }

    // 2. Tree Data & Metrics APIs (Network-first with offline cache)
    if (url.pathname.startsWith('/api/trees') || url.pathname.startsWith('/api/metrics')) {
        event.respondWith(
            fetch(request)
                .then((networkRes) => {
                    const resClone = networkRes.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, resClone));
                    return networkRes;
                })
                .catch(() => caches.match(request))
        );
        return;
    }

    // 3. Static assets, icons, tiles (Cache-first with stale-while-revalidate)
    event.respondWith(
        caches.match(request).then((cachedRes) => {
            if (cachedRes) {
                // Fetch fresh in background
                fetch(request).then((networkRes) => {
                    if (networkRes.status === 200) {
                        caches.open(CACHE_NAME).then((cache) => cache.put(request, networkRes));
                    }
                }).catch(() => {});
                return cachedRes;
            }
            return fetch(request).then((networkRes) => {
                if (networkRes.status === 200 && (url.origin === location.origin || url.hostname.includes('unpkg.com'))) {
                    const resClone = networkRes.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, resClone));
                }
                return networkRes;
            });
        })
    );
});
