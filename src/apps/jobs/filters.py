import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    min_salary = django_filters.CharFilter(field_name='salary', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    job_type = django_filters.CharFilter(field_name='job_type', lookup_expr='icontains')
    experience_level = django_filters.CharFilter(field_name='experience_level', lookup_expr='icontains')
    remote = django_filters.CharFilter(field_name='remote_policy', lookup_expr='icontains')
    urgent = django_filters.BooleanFilter(field_name='urgent')
    
    # Filter by date ranges
    posted_after = django_filters.DateFilter(field_name='posted', lookup_expr='gte')
    posted_before = django_filters.DateFilter(field_name='posted', lookup_expr='lte')
    deadline_after = django_filters.DateFilter(field_name='application_deadline', lookup_expr='gte')
    deadline_before = django_filters.DateFilter(field_name='application_deadline', lookup_expr='lte')
    
    class Meta:
        model = Job
        fields = [
            'job_type', 'location', 'experience_level', 
            'education', 'urgent', 'remote_policy'
        ]