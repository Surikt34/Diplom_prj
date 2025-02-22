from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from catalog.views import RollbarTestAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("api/catalog/", include("catalog.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/users/", include("users.urls")),
    path("api/orders/", include("orders.urls")),
    path("", include("users.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("test-rollbar/", RollbarTestAPIView.as_view(), name="test-rollbar"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
