from rest_framework import permissions

class IsStudentParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'student'

class IsTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'tutor'

