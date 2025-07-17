from rest_framework.permissions import BasePermission

class IsAdminOrStudentParent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        if user.is_staff:
            return True

        if hasattr(user, 'userprofile') and user.userprofile.user_type == 'student':
            return True
        
        return False