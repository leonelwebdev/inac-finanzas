"""
URL configuration for lector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.views.decorators.http import require_GET
from django.http import HttpResponse

@require_GET
def admin_sw(request):
    js = r"""
const CACHE_VERSION = "v1.0.0";
const RUNTIME_CACHE = `hftecno-admin-${CACHE_VERSION}`;

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(RUNTIME_CACHE);
    await cache.addAll(["/admin/"]);
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      .filter(k => k.startsWith("hftecno-admin-") && k !== RUNTIME_CACHE)
      .map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Solo manejar GET dentro de /admin/
  if (req.method !== "GET") return;
  if (!url.pathname.startsWith("/admin/")) return;

  const acceptsHTML = req.headers.get("accept")?.includes("text/html");
  const isStatic = url.pathname.startsWith("/static/");

  if (acceptsHTML) {
    event.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        const cache = await caches.open(RUNTIME_CACHE);
        cache.put(req, fresh.clone());
        return fresh;
      } catch (e) {
        const cached = await caches.match(req);
        return cached || caches.match("/admin/");
      }
    })());
    return;
  }

  if (isStatic) {
    event.respondWith((async () => {
      const cached = await caches.match(req);
      if (cached) return cached;
      const fresh = await fetch(req);
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(req, fresh.clone());
      return fresh;
    })());
    return;
  }
});
"""
    return HttpResponse(js, content_type="application/javascript")

urlpatterns = [
    path("admin/sw.js", admin_sw, name="admin_sw"),
    path('admin/', admin.site.urls),
]

# Redirigir siempre la raíz "/" a "/admin"
urlpatterns += [
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]
