from rest_framework.permissions import BasePermission

class IsCompanyUser(BasePermission):
    """Allow access only to users with company_profile"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'company_profile')

class IsJobSeekerUser(BasePermission):
    """Allow access only to users with jobseeker_profile"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'jobseeker_profile')

class IsJobOwner(BasePermission):
    """Allow object-level access only if job belongs to the authenticated company"""
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'company_profile') and obj.company == request.user.company_profile

class IsApplicationOwner(BasePermission):
    """Allow object-level access only if application belongs to the company's job"""
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'company_profile'):
            return obj.job.company == request.user.company_profile
        return False
