// Cache only the static installation shell, not sensitive health data or Streamlit content.
const CACHE='hermamaai-shell-v1';
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(['./index.html','./manifest.webmanifest'])));self.skipWaiting()});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key)))));self.clients.claim()});
self.addEventListener('fetch',event=>{const url=new URL(event.request.url);if(event.request.method!=='GET'||url.origin!==self.location.origin)return;if(url.pathname.endsWith('/index.html')||url.pathname.endsWith('/manifest.webmanifest')){event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)))}})
