from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    CompanyProfileView,
    JobSeekerProfileView,
    CompanyProfileUpdateView,
    JobSeekerProfileUpdateView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('company-profile/', CompanyProfileView.as_view(), name='company-profile'),
    path('company-profile/update/', CompanyProfileUpdateView.as_view(), name='company-profile-update'),
    path('jobseeker-profile/', JobSeekerProfileView.as_view(), name='jobseeker-profile'),
    path('jobseeker-profile/update/', JobSeekerProfileUpdateView.as_view(), name='jobseeker-profile-update'),
]
