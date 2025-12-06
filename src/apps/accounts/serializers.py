from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company, JobSeeker

# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

# -------------------------
# Registration Serializer
# -------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type', 'token']

    def create(self, validated_data):
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
        )

        # Automatically create profile
        if user.user_type == 'company':
            Company.objects.create(user=user, company_name=user.username)
        else:
            JobSeeker.objects.create(user=user)

        return user

    def get_token(self, obj) -> dict:
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# -------------------------
# Login Serializer
# -------------------------
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    user_type = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        return {
            'user': user,
            'username': user.username,
            'user_type': user.user_type,
        }

    def get_token(self, obj) -> dict:
        refresh = RefreshToken.for_user(obj['user'])
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# -------------------------
# Company Serializer
# -------------------------
# -------------------------
# Company Update Serializer
# -------------------------
class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Company
        fields = [
            "id", "company_id", "company_name", "tagline", "description", "website",
            "email", "phone", "location", "founded", "industry", "company_size",
            "company_info", "logo", "user"
        ]
        read_only_fields = ["id", "company_id", "user"]

class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    resume = serializers.FileField(required=False, allow_null=True)
    skills = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    experience = serializers.ListField(child=serializers.DictField(), required=False)
    education = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = JobSeeker
        fields = [
            "id", "full_name", "title", "bio", "location",
            "skills", "experience", "education",
            "profile_picture", "resume", "user"
        ]
        read_only_fields = ["id", "user"]