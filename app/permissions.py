from rest_framework import permissions

class IsAdminOrEngineer(permissions.BasePermission):


    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.method in ['POST', 'PUT', 'PATCH']:
                return request.user.is_staff or request.user.groups.filter(name='Engineer').exists() or request.user.groups.filter(name='Admin').exists()

        if request.method == 'DELETE':
            return False

        return False