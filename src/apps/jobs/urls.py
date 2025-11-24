from django.urls import path
from .views import (
    JobListView,
    JobCreateView,
    JobDetailView,
    ApplicationCreateView,
    ApplicationListView
)

urlpatterns = [
    path('', JobListView.as_view(), name="job-list"),
    path('create/', JobCreateView.as_view(), name="job-create"),
    path('<int:pk>/', JobDetailView.as_view(), name="job-detail"),
    path('apply/', ApplicationCreateView.as_view(), name="apply-job"),
    path('applications/', ApplicationListView.as_view(), name="applications"),
]
