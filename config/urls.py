from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
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

    path("admin/", admin.site.urls),
]
    