from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    CompanyJobListView,
    CompanyJobCreateView,
    CompanyJobDetailView,
    CompanyJobUpdateView,
    CompanyJobDeleteView,
    ApplicationCreateView,
    ApplicationListView,
    ApplicationUpdateView,
    MyApplicationsListView,
)

urlpatterns = [
    # Public / jobseeker endpoints
    path("", JobListView.as_view(), name="job-list"),
    path("<int:pk>/", JobDetailView.as_view(), name="job-detail"),

    # Company endpoints
    path("company/", CompanyJobListView.as_view(), name="company-job-list"),
    path("company/create/", CompanyJobCreateView.as_view(), name="company-job-create"),
    path("company/<int:pk>/", CompanyJobDetailView.as_view(), name="company-job-detail"),
    path("company/<int:pk>/update/", CompanyJobUpdateView.as_view(), name="company-job-update"),
    path("company/<int:pk>/delete/", CompanyJobDeleteView.as_view(), name="company-job-delete"),

    # Applications
    path("apply/", ApplicationCreateView.as_view(), name="apply-job"),
    path("applications/", ApplicationListView.as_view(), name="application-list"),
    path("applications/<int:pk>/update/", ApplicationUpdateView.as_view(), name="application-update"),
    path("my-applications/", MyApplicationsListView.as_view(), name="my-applications"),
]
