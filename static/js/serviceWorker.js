const assets = [
  "/",
  "static/css/style.css",
  "static/css/style.css/bootstrap.min.css",
  "static/css/prism-okaidia.min.css",
  "static/js/bootstrap.bundle.min.js",
  "static/js/prism.min.js",
  "static/js/prism-javascript.min.js",
  "static/js/prism-python.min.js",
  "static/js/app.js",
  "static/images/logo.png",
  "static/images/favicon.jpg",
  "static/icons/icon-128x128.png",
  "static/icons/icon-192x192.png",
  "static/icons/icon-384x384.png",
  "static/icons/icon-512x512.png",
  "static/icons/desktop_screenshot.png",
  "static/icons/mobile_screenshot.png",
  "static/manifest.json",
];

const CATALOGUE_ASSETS = "catalogue-assets";

self.addEventListener("install", (installEvt) => {
  installEvt.waitUntil(
    caches
      .open(CATALOGUE_ASSETS)
      .then((cache) => {
        console.log("Caching assets");
        return cache.addAll(assets);
      })
      .then(self.skipWaiting())
      .catch((e) => {
        console.log(e);
      })
  );
});

self.addEventListener("activate", (evt) => {
  evt.waitUntil(
    caches
      .keys()
      .then((keyList) => {
        return Promise.all(
          keyList.map((key) => {
            if (key !== CATALOGUE_ASSETS) {
              console.log("Removing old cache:", key);
              return caches.delete(key);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (evt) => {
  evt.respondWith(
    fetch(evt.request).catch(() => {
      return caches.open(CATALOGUE_ASSETS).then((cache) => {
        return cache.match(evt.request);
      });
    })
  );
});

document.getElementById("diaryEntryForm").addEventListener(
  "submit",
  function (event) {
    var form = this;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
      // Find the first invalid element
      var firstInvalidElement = form.querySelector(":invalid");
      if (firstInvalidElement) {
        // Scroll to the first invalid element
        firstInvalidElement.focus();
        firstInvalidElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }
    }
    form.classList.add("was-validated");
  },
  false
);

document.getElementById("diaryEntryForm").addEventListener(
  "submit",
  function (event) {
    var form = this;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
      // Find the first invalid element
      var firstInvalidElement = form.querySelector(":invalid");
      if (firstInvalidElement) {
        // Scroll to the first invalid element
        firstInvalidElement.focus();
        firstInvalidElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }
    }
    form.classList.add("was-validated");
  },
  false
);
