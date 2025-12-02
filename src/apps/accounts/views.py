from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    CompanySerializer,
    JobSeekerSerializer,
)
from .models import Company, JobSeeker

# -----------------------------
# USER REGISTER
# -----------------------------
@extend_schema(
    tags=["Auth"],
    request=UserRegistrationSerializer,
    responses={201: UserSerializer}
)
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # JWT token
            refresh = RefreshToken.for_user(user)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            # Set redirect URL based on user type
            redirect_url = "/company/dashboard" if user.user_type == "company" else "/jobseeker/dashboard"

            response_data = {
                "username": user.username,
                "user_type": user.user_type,
                "token": token_data,
                "redirect_url": redirect_url
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# USER LOGIN
# -----------------------------
@extend_schema(
    tags=["Auth"],
    request=UserLoginSerializer,
    responses={200: {"username": str, "user_type": str, "token": dict, "redirect_url": str}}
)
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            # JWT token
            refresh = RefreshToken.for_user(user)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            # Set redirect URL based on user type
            redirect_url = "/company" if user.user_type == "company" else "/jobseeker"

            return Response({
                "username": user.username,
                "user_type": user.user_type,
                "token": token_data,
                "redirect_url": redirect_url
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# USER LOGOUT
# -----------------------------
@extend_schema(
    tags=["Auth"],
    responses={200: {"message": "Logged out successfully"}}
)
class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# -----------------------------
# USER PROFILE
# -----------------------------
@extend_schema(tags=["Profile"])
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data

        # Include related company/jobseeker profile
        if hasattr(request.user, 'company_profile'):
            try:
                user_data['company_profile'] = CompanySerializer(request.user.company_profile).data
                user_data['redirect_url'] = "/company"
            except Company.DoesNotExist:
                user_data['company_profile'] = None
        elif hasattr(request.user, 'jobseeker_profile'):
            try:
                user_data['jobseeker_profile'] = JobSeekerSerializer(request.user.jobseeker_profile).data
                user_data['redirect_url'] = "/jobseeker"
            except JobSeeker.DoesNotExist:
                user_data['jobseeker_profile'] = None

        return Response(user_data, status=status.HTTP_200_OK)


# -----------------------------
# COMPANY PROFILE VIEW
# -----------------------------
@extend_schema(tags=["Profile"])
class CompanyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            company = Company.objects.get(user=request.user)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response(
                {"error": "This user does not have a company profile."},
                status=status.HTTP_404_NOT_FOUND
            )


# -----------------------------
# JOB SEEKER PROFILE VIEW
# -----------------------------
@extend_schema(tags=["Profile"])
class JobSeekerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            jobseeker = JobSeeker.objects.get(user=request.user)
            serializer = JobSeekerSerializer(jobseeker)
            response_data = serializer.data
            response_data['redirect_url'] = "/jobseeker/dashboard"  # Add redirect URL
            return Response(response_data, status=status.HTTP_200_OK)
        except JobSeeker.DoesNotExist:
            return Response(
                {"error": "This user does not have a job seeker profile."},
                status=status.HTTP_404_NOT_FOUND
            )
