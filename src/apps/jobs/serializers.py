# serializers.py
from rest_framework import serializers
from .models import Job, Application

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company_username = serializers.CharField(source='company.user.username', read_only=True)
    
    # Add custom date fields to handle datetime conversion
    posted = serializers.DateField(format='%Y-%m-%d', required=False)
    application_deadline = serializers.DateField(format='%Y-%m-%d', allow_null=True, required=False)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'salary', 'location', 
            'job_type', 'posted', 'requirements', 'responsibilities', 
            'benefits', 'company_info', 'applicants_count', 'saved', 
            'urgent', 'application_deadline', 'remote_policy', 
            'experience_level', 'education', 'created_at',
            'company_name', 'company_username'
        ]
        read_only_fields = [
            'id', 'company', 'posted', 'applicants_count', 
            'saved', 'created_at', 'company_name', 'company_username'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    jobseeker_name = serializers.CharField(source='jobseeker.user.get_full_name', read_only=True)
    jobseeker_username = serializers.CharField(source='jobseeker.user.username', read_only=True)
    company_name = serializers.CharField(source='job.company.company_name', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'jobseeker', 'cover_letter', 'applied_at', 'status',
            'job_title', 'jobseeker_name', 'jobseeker_username', 'company_name'
        ]
        read_only_fields = [
            'id', 'jobseeker', 'applied_at', 'status',
            'job_title', 'jobseeker_name', 'jobseeker_username', 'company_name'
        ]