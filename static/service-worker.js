const CACHE_NAME = "the-hangover-v1";

const FILES_TO_CACHE = [
    "/",
    "/static/style.css",
    "/static/manifest.json"
];


self.addEventListener("install", function(event) {

    event.waitUntil(

        caches.open(CACHE_NAME)
            .then(function(cache) {

                return cache.addAll(
                    FILES_TO_CACHE
                );

            })

    );

});


self.addEventListener("activate", function(event) {

    event.waitUntil(

        caches.keys()
            .then(function(cacheNames) {

                return Promise.all(

                    cacheNames.map(
                        function(cacheName) {

                            if (
                                cacheName !==
                                CACHE_NAME
                            ) {

                                return caches.delete(
                                    cacheName
                                );

                            }

                        }
                    )

                );

            })

    );

});


self.addEventListener("fetch", function(event) {

    event.respondWith(

        caches.match(event.request)
            .then(function(cachedResponse) {

                if (cachedResponse) {

                    return cachedResponse;

                }

                return fetch(event.request);

            })

    );

});