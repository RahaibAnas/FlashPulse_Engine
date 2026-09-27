from rest_framework import permissions

class IsadminOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == "admin":
            return True
        if request.method in ['GET','OPTIONS','HEAD']:
            return True
        
