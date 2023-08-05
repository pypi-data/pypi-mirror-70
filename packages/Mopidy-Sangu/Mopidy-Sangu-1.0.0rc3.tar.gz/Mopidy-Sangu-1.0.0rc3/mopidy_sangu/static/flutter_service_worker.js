'use strict';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "favicon.ico": "874092d0198d11661312715c601739ce",
"main.dart.js": "adb568caf6ddfba02ca79538b0f3a89c",
"assets/fonts/MaterialIcons-Regular.ttf": "56d3ffdef7a25659eab6a68a3fbfaf16",
"assets/FontManifest.json": "01700ba55b08a6141f33e168c4a6c22f",
"assets/LICENSE": "3b7bd347677c32711fc3dd7be0b64f07",
"assets/images/jellyfin.png": "74676c043b2b5f6918172280d927e0d7",
"assets/images/soundcloud.png": "d6e6ad2e333f4e31dcb72c1b12db56b2",
"assets/images/spotify.png": "2de93a8478c8d2c30e7b689e08cb9d43",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "115e937bb829a890521f72d2e664b632",
"assets/AssetManifest.json": "2efbb41d7877d10aac9d091f58ccd7b9",
"manifest.json": "d298d8128dd8e21615195d6d8f9b93f0",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"index.html": "f5e98f05731e286ee56211c5fe7a954f",
"/": "f5e98f05731e286ee56211c5fe7a954f"
};

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheName) {
      return caches.delete(cacheName);
    }).then(function (_) {
      return caches.open(CACHE_NAME);
    }).then(function (cache) {
      return cache.addAll(Object.keys(RESOURCES));
    })
  );
});

self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
