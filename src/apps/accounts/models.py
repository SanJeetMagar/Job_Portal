from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# ---------------------------------
# Custom User Model
# ---------------------------------
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('company', 'Company'),
        ('jobseeker', 'Job Seeker'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    REQUIRED_FIELDS = ['email', 'user_type']

    def __str__(self):
        return f"{self.username} - {self.user_type}"


# ---------------------------------
# Company Profile
# ---------------------------------
class Company(models.Model):
    company_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_profile")
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)


    
    def save(self, *args, **kwargs):
        if not self.company_id:
            self.company_id = "CMP-" + uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name


# ---------------------------------
# Job Seeker Profile
# ---------------------------------
class JobSeeker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobseeker_profile")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
