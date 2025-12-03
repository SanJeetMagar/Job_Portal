from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from .permissions import IsCompanyUser, IsJobSeekerUser, IsJobOwner, IsApplicationOwner
from .pagination import JobPagination, ApplicationPagination
from .filters import JobFilter



# ====================================
#                JOBS
# ====================================

@extend_schema(
    tags=["Jobs"],
    summary="Create a new job post",
    description="Only company users can create job posts.",
    request=JobSerializer,
    responses={201: JobSerializer}
)
class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser]

    def perform_create(self, serializer):
        # Automatically assign the company from the authenticated user
        serializer.save(company=self.request.user.company_profile)


@extend_schema(
    tags=["Jobs"],
    summary="List all job posts",
    description="Returns a paginated list of all jobs with filtering, searching, and ordering options.",
    responses={200: JobSerializer}
)
class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    pagination_class = JobPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'location', 'company__company_name']
    ordering_fields = ['created_at', 'salary', 'posted', 'applicants_count']
    ordering = ['-created_at']

    def get_queryset(self):
        # Optionally filter by company if company_id parameter is provided
        company_id = self.request.query_params.get('company_id')
        if company_id:
            return Job.objects.filter(company_id=company_id)
        return Job.objects.all()


@extend_schema(
    tags=["Jobs"],
    summary="Retrieve a job",
    description="Retrieve detailed information about a specific job.",
    responses={200: JobSerializer}
)
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Jobs"],
    summary="Update a job",
    description="Only the company who created the job can update it.",
    request=JobSerializer,
    responses={200: JobSerializer}
)
class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser, IsJobOwner]


@extend_schema(
    tags=["Jobs"],
    summary="Delete a job",
    description="Only the company who created the job can delete it.",
    responses={204: None}
)
class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser, IsJobOwner]


@extend_schema(
    tags=["Jobs"],
    summary="List jobs posted by current company",
    description="Returns a list of jobs posted by the authenticated company user.",
    responses={200: JobSerializer}
)
class CompanyJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser]
    pagination_class = JobPagination

    def get_queryset(self):
        # Return only jobs posted by the current company
        return Job.objects.filter(company=self.request.user.company_profile)


# ====================================
#            APPLICATIONS
# ====================================

@extend_schema(
    tags=["Applications"],
    summary="Apply to a job",
    description="Only job seekers can apply for jobs. The jobseeker is automatically assigned from the authenticated user.",
    request=ApplicationSerializer,
    responses={201: ApplicationSerializer}
)
class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeekerUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if already applied
        job = serializer.validated_data['job']
        if Application.objects.filter(job=job, jobseeker=request.user.jobseeker_profile).exists():
            return Response(
                {"error": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Automatically assign the jobseeker from the authenticated user
        serializer.save(jobseeker=self.request.user.jobseeker_profile)


@extend_schema(
    tags=["Applications"],
    summary="List job applications",
    description="Company users can view all applications submitted to their job posts.",
    responses={200: ApplicationSerializer}
)
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    pagination_class = ApplicationPagination
    permission_classes = [IsCompanyUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['job', 'status']
    ordering_fields = ['applied_at', 'status']
    ordering = ['-applied_at']

    def get_queryset(self):
        # Return only applications for jobs belonging to the current company
        return Application.objects.filter(job__company=self.request.user.company_profile)


@extend_schema(
    tags=["Applications"],
    summary="Update application status",
    description="Company users can update the status of applications for their jobs.",
    request=ApplicationSerializer,
    responses={200: ApplicationSerializer}
)
class ApplicationUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsCompanyUser, IsApplicationOwner]
    
    def partial_update(self, request, *args, **kwargs):
        # Only allow updating status field for company users
        if 'status' not in request.data or len(request.data) > 1:
            return Response(
                {"error": "Only the 'status' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)


@extend_schema(
    tags=["Applications"],
    summary="List my applications",
    description="Job seekers can view all applications they have submitted.",
    responses={200: ApplicationSerializer}
)
class MyApplicationsListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeekerUser]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        # Return only applications submitted by the current jobseeker
        return Application.objects.filter(jobseeker=self.request.user.jobseeker_profile)