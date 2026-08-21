// Service worker minimal, écrit à la main (pas de next-pwa/workbox — Turbopack
// n'est pas compatible avec leur plugin webpack). Deux strategies seulement :
// - navigations (pages HTML) : reseau d'abord, repli offline.html si hors ligne.
// - assets statiques (_next/static, /icons) : cache d'abord, mise a jour en fond.
// Rien d'autre n'est mis en cache : pas d'API, pas de donnees dynamiques.

const CACHE_VERSION = "v1";
const STATIC_CACHE = `pokedeals-static-${CACHE_VERSION}`;
const OFFLINE_URL = "/offline.html";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.add(OFFLINE_URL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key.startsWith("pokedeals-static-") && key !== STATIC_CACHE)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

function isStaticAsset(url) {
  return (
    url.pathname.startsWith("/_next/static/") ||
    url.pathname.startsWith("/icons/")
  );
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  if (isStaticAsset(url)) {
    event.respondWith(
      caches.open(STATIC_CACHE).then(async (cache) => {
        const cached = await cache.match(request);
        const network = fetch(request)
          .then((response) => {
            if (response.ok) cache.put(request, response.clone());
            return response;
          })
          .catch(() => cached);
        return cached || network;
      })
    );
  }
});

// Notifications push (scraper/notifications_saas.py) : payload JSON
// {title, body, url}. Toute erreur de parsing retombe sur un texte
// generique -- jamais d'echec silencieux de la notification elle-meme.
self.addEventListener("push", (event) => {
  let payload = { title: "PokéDeals", body: "Nouvelle alerte disponible." };
  try {
    if (event.data) payload = { ...payload, ...event.data.json() };
  } catch {
    // payload non-JSON ignoré, on garde le texte générique
  }

  event.waitUntil(
    self.registration.showNotification(payload.title, {
      body: payload.body,
      icon: "/icons/icon-192.png",
      badge: "/icons/icon-192.png",
      data: { url: payload.url || "/dashboard" },
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = event.notification.data?.url || "/dashboard";
  event.waitUntil(
    self.clients
      .matchAll({ type: "window", includeUncontrolled: true })
      .then((clientsArr) => {
        const existant = clientsArr.find((c) => c.url.includes(url));
        if (existant) return existant.focus();
        return self.clients.openWindow(url);
      })
  );
});
