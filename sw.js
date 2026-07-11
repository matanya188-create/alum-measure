/* Service Worker — עבודה אופליין מלאה. להעלאת גרסה חדשה: להעלות את VERSION. */
const VERSION = "v52";
const CACHE = "alum-measure-" + VERSION;
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-maskable-512.png",
  "./apple-touch-icon.png",
  "./three.min.js",
  "./view.jpg",
  "./wall.jpg",
  "./floor.jpg",
  "./pavers.jpg",
  "./stucco.jpg",
  "./profiles-catalog.pdf",
  "./handles/alma.png","./handles/art_black.png","./handles/art_brass_antique.png","./handles/art_brass_mat.png",
  "./handles/art_silver.png","./handles/art_silver_antique.png","./handles/art_white.png","./handles/astra.png",
  "./handles/bau05xl.png","./handles/bau10.png","./handles/bau18.png","./handles/bau33.png",
  "./handles/bau33xl.png","./handles/bau3479.png","./handles/bau5.png","./handles/bau56.png",
  "./handles/bau56xl.png","./handles/bau66.png","./handles/bau76.png","./handles/bau77.png",
  "./handles/bau99.png","./handles/bauhaus_h.png","./handles/buba4364.png","./handles/chuchit.png",
  "./handles/chuchit4356.png","./handles/claudia.png","./handles/cosi.png","./handles/doxifet.png",
  "./handles/dror.png","./handles/dror4358.png","./handles/flow.png","./handles/glory.png",
  "./handles/gu.png","./handles/k1.png","./handles/k2.png","./handles/lapia.png",
  "./handles/laser3478.png","./handles/miriam.png","./handles/nachliieli.png","./handles/ofroni.png",
  "./handles/pshuosh.png","./handles/q10.png","./handles/rombo.png","./handles/rostia.png",
  "./handles/sasha.png","./handles/snonit.png","./handles/tris.png","./handles/tzufit.png",
  "./handles/zamir.png","./handles/zamir4357.png","./handles/zed.png"
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* network-first לדף עצמו (כדי לקבל עדכונים), cache fallback לאופליין */
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true })
        .then(m => m || caches.match("./index.html")))
  );
});
