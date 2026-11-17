from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission for Activity objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the activity belongs to the user through the chain
        return obj.sub_branch.branch.domain.user == request.user
