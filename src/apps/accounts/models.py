# src/apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

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

class Company(models.Model):
    company_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_profile")

    # visible profile
    company_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True, null=True)     # small tagline
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # contact & meta
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    founded = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    company_size = models.CharField(max_length=100, blank=True, null=True)

    # structured fields
    company_info = models.JSONField(blank=True, null=True)   # free JSON for more structured meta
    # assets
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.company_id:
            self.company_id = "CMP-" + uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

class JobSeeker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobseeker_profile")

    # visible profile
    full_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # structured arrays
    skills = models.JSONField(blank=True, null=True)        # e.g. ["Python", "Django"]
    experience = models.JSONField(blank=True, null=True)    # list of dicts
    education = models.JSONField(blank=True, null=True)     # list of dicts

    # assets
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return self.user.username
