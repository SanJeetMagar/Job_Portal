from rest_framework.permissions import BasePermission


class IsCompanyUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'company_profile')


class IsJobSeekerUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'jobseeker_profile')


class IsJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'company_profile') and obj.company == request.user.company_profile


class IsApplicationOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'company_profile'):
            return obj.job.company == request.user.company_profile
        return False