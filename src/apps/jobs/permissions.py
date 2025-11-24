from rest_framework import permissions

class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'company'


class IsJobSeekerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'jobseeker'


class IsJobOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.user == request.user
