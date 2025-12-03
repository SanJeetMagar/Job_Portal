from django.urls import path
from .views import (
    JobListView,
    JobCreateView,
    JobDetailView,
    JobUpdateView,
    JobDeleteView,
    CompanyJobListView,
    ApplicationCreateView,
    ApplicationListView,
    ApplicationUpdateView,
    MyApplicationsListView
)

urlpatterns = [
    # Job URLs
    path('', JobListView.as_view(), name="job-list"),
    path('create/', JobCreateView.as_view(), name="job-create"),
    path('<int:pk>/', JobDetailView.as_view(), name="job-detail"),
    path('<int:pk>/update/', JobUpdateView.as_view(), name="job-update"),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name="job-delete"),
    path('my-jobs/', CompanyJobListView.as_view(), name="my-jobs"),
    
    # Application URLs
    path('apply/', ApplicationCreateView.as_view(), name="apply-job"),
    path('applications/', ApplicationListView.as_view(), name="applications"),
    path('applications/<int:pk>/update/', ApplicationUpdateView.as_view(), name="application-update"),
    path('my-applications/', MyApplicationsListView.as_view(), name="my-applications"),
]