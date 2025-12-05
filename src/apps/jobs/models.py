from django.db import models
from django.utils import timezone
from src.apps.accounts.models import Company, JobSeeker


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)
    posted = models.DateField(default=timezone.now)
    requirements = models.JSONField(blank=True, null=True)
    responsibilities = models.JSONField(blank=True, null=True)
    benefits = models.JSONField(blank=True, null=True)
    company_info = models.JSONField(blank=True, null=True)
    applicants_count = models.IntegerField(default=0)
    saved = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    application_deadline = models.DateField(blank=True, null=True)
    remote_policy = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company.company_name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Reviewed", "Reviewed"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        # Updated: company username → job title
        return f"{self.job.company.user.username} → {self.job.title}"
