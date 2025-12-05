from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer, ApplicationStatusUpdateSerializer
from .permissions import IsCompanyUser, IsJobSeekerUser, IsJobOwner, IsApplicationOwner
from .pagination import JobPagination, ApplicationPagination
from .filters import JobFilter

# ====================================
#           JOBS (Public / All)
# ====================================

@extend_schema(
    tags=["Jobs"],
    summary="List all jobs",
    description="Jobseekers can view all job posts across companies.",
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
        return Job.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@extend_schema(
    tags=["Jobs"],
    summary="Retrieve a job",
    description="Retrieve details of a specific job (public view).",
    responses={200: JobSerializer}
)
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

# ====================================
#           COMPANY JOBS
# ====================================

@extend_schema(
    tags=["Company Jobs"],
    summary="List all jobs for current company",
    description="Returns only jobs created by the authenticated company.",
    responses={200: JobSerializer}
)
class CompanyJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser]
    pagination_class = JobPagination

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company_profile)

@extend_schema(
    tags=["Company Jobs"],
    summary="Create a new job",
    description="Create a job post for the authenticated company.",
    request=JobSerializer,
    responses={201: JobSerializer}
)
class CompanyJobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company_profile)

@extend_schema(
    tags=["Company Jobs"],
    summary="Retrieve a job for company",
    description="Get job details only if it belongs to the authenticated company.",
    responses={200: JobSerializer}
)
class CompanyJobDetailView(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser, IsJobOwner]

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company_profile)

@extend_schema(
    tags=["Company Jobs"],
    summary="Update a job",
    description="Update job details only if it belongs to the authenticated company.",
    request=JobSerializer,
    responses={200: JobSerializer}
)
class CompanyJobUpdateView(generics.UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser, IsJobOwner]

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company_profile)

@extend_schema(
    tags=["Company Jobs"],
    summary="Delete a job",
    description="Delete a job only if it belongs to the authenticated company.",
    responses={204: None}
)
class CompanyJobDeleteView(generics.DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser, IsJobOwner]

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company_profile)

# ====================================
#           APPLICATIONS
# ====================================

@extend_schema(
    tags=["Applications"],
    summary="Apply to a job",
    description="Only jobseekers can apply. Checks if already applied.",
    request=ApplicationSerializer,
    responses={201: ApplicationSerializer}
)
class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeekerUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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
        serializer.save(jobseeker=self.request.user.jobseeker_profile)

@extend_schema(
    tags=["Applications"],
    summary="List job applications (company)",
    description="Company users can view applications only for their jobs.",
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
        return Application.objects.filter(job__company=self.request.user.company_profile)

@extend_schema(
    tags=["Applications"],
    summary="Update application status",
    description="Company users can update status only for their applications.",
    request=ApplicationStatusUpdateSerializer,
    responses={200: ApplicationSerializer}
)
class ApplicationUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer  # full serializer for response
    permission_classes = [IsCompanyUser, IsApplicationOwner]

    def partial_update(self, request, *args, **kwargs):
        # Only allow status field
        if 'status' not in request.data or len(request.data) > 1:
            return Response(
                {"error": "Only the 'status' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update only the status
        instance = self.get_object()
        status_serializer = ApplicationStatusUpdateSerializer(
            instance, data=request.data, partial=True
        )
        status_serializer.is_valid(raise_exception=True)
        status_serializer.save()

        # Return the full updated object
        full_serializer = self.get_serializer(instance)
        return Response(full_serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(
    tags=["Applications"],
    summary="List my applications",
    description="Jobseekers can view all applications they submitted.",
    responses={200: ApplicationSerializer}
)
class MyApplicationsListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeekerUser]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        return Application.objects.filter(jobseeker=self.request.user.jobseeker_profile)
