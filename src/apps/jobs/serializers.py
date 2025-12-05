from rest_framework import serializers
from .models import Job, Application

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company_username = serializers.CharField(source='company.user.username', read_only=True)
    company_id = serializers.CharField(source="company.company_id", read_only=True)

    posted = serializers.SerializerMethodField()
    application_deadline = serializers.SerializerMethodField()


    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'salary', 'location', 
            'job_type', 'posted', 'requirements', 'responsibilities', 
            'benefits', 'company_info', 'applicants_count', 'saved', 
            'urgent', 'application_deadline', 'remote_policy', 
            'experience_level', 'education', 'created_at',
            'company_name', 'company_username','company_id'
        ]
        read_only_fields = [
            'id', 'company', 'posted', 'applicants_count', 
            'created_at', 'company_name', 'company_username', 'company_id'
        ]

    def get_posted(self, obj):
        if obj.posted:
            return obj.posted.isoformat()
        return None

    def get_application_deadline(self, obj):
        if obj.application_deadline:
            return obj.application_deadline.isoformat()
        return None


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
            'id', 'jobseeker', 'applied_at', 'job_title', 'jobseeker_name', 
            'jobseeker_username', 'company_name'
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
