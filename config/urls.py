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

    path("admin/", admin.site.urls),
]
