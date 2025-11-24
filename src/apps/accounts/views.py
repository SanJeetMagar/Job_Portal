from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    CompanySerializer,
    JobSeekerSerializer,
)

# USER REGISTER
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
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# USER LOGIN
@extend_schema(
    tags=["Auth"],
    request=UserLoginSerializer,
    responses={200: {"message": "Login successful"}}
)
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# USER LOGOUT
@extend_schema(
    tags=["Auth"],
    responses={200: {"message": "Logged out successfully"}}
)
class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

# USER PROFILE
@extend_schema(tags=["Profile"])
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

# COMPANY PROFILE VIEW
@extend_schema(tags=["Profile"])
class CompanyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "company_profile"):
            return Response({"error": "Not a company user."}, status=400)
        return Response(CompanySerializer(request.user.company_profile).data)

# JOB SEEKER PROFILE VIEW
@extend_schema(tags=["Profile"])
class JobSeekerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "jobseeker_profile"):
            return Response({"error": "Not a job seeker user."}, status=400)
        return Response(JobSeekerSerializer(request.user.jobseeker_profile).data)
