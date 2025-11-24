from rest_framework import generics
from drf_spectacular.utils import extend_schema
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from .permissions import IsCompanyUser, IsJobSeekerUser, IsJobOwner
from .pagination import JobPagination, ApplicationPagination


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
        serializer.save(company=self.request.user.company_profile)


@extend_schema(
    tags=["Jobs"],
    summary="List all job posts",
    description="Returns a paginated list of all jobs, ordered by newest first.",
    responses={200: JobSerializer}
)
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    pagination_class = JobPagination


@extend_schema(
    tags=["Jobs"],
    summary="Retrieve, update, or delete a job",
    description="Retrieve a job post or update/delete it. Only the company who created the job can modify it.",
    request=JobSerializer,
    responses={200: JobSerializer}
)
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsCompanyUser, IsJobOwner]


# ====================================
#            APPLICATIONS
# ====================================

@extend_schema(
    tags=["Applications"],
    summary="Apply to a job",
    description="Only job seekers can apply for jobs.",
    request=ApplicationSerializer,
    responses={201: ApplicationSerializer}
)
class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeekerUser]

    def perform_create(self, serializer):
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

    def get_queryset(self):
        return Application.objects.filter(job__company=self.request.user.company_profile)
