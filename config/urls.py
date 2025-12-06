from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Default homepage = Swagger UI
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    
    # API schema
    path("schema/", SpectacularAPIView.as_view(), name="schema"),

    # Optional: Redoc docs
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Apps
    path("api/accounts/", include("src.apps.accounts.urls")),
    path("api/jobs/", include("src.apps.jobs.urls")),

    # JWT Auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Admin
    path("admin/", admin.site.urls),
]


# ------------------------------------------------
# 🔥 VERY IMPORTANT FOR USER PROFILE / COMPANY LOGO / RESUME FILES
# ------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
