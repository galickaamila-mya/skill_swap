from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("skills/", include("skills.urls", namespace="skills")),
    path("matching/", include("matching.urls", namespace="matching")),
    path("chat/", include("chat.urls", namespace="chat")),
    path("user/", include("user.urls", namespace="user")),
    path("accounts/", include("allauth.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/", include("skill_swap.api_urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
