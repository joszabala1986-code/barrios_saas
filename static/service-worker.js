const CACHE_NAME = "planta-digital-v3";
const OFFLINE_URL = "/offline/";

const urlsToCache = [
  "/",
  "/login/",
  "/offline/",
  "/static/css/style.css",
  "/static/img/icon_192.png",
  "/static/img/icon_512.png"
];

const noCacheUrls = [
  "/logout/",
  "/subir-comprobante/",
  "/crear-comunicado/",
  "/subir-contrato/",
  "/api/"
];

// INSTALL
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// ACTIVATE
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(
        names.map(name => {
          if (name !== CACHE_NAME) return caches.delete(name);
        })
      )
    ).then(() => self.clients.claim())
  );
});

// FETCH
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);

  const shouldNotCache = noCacheUrls.some(path =>
    url.pathname.startsWith(path)
  );

  if (shouldNotCache || event.request.method !== "GET") {
    return;
  }

  // Navegación (HTML)
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request)
        .catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // Archivos estáticos
  if (url.pathname.match(/\.(css|js|png|jpg|jpeg|svg|ico|webp)$/)) {
    event.respondWith(
      caches.match(event.request)
        .then(res => res || fetch(event.request))
    );
  }
});