from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to view/edit their objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # For Domain
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For Branch
        if hasattr(obj, 'domain'):
            return obj.domain.user == request.user
        
        # For SubBranch (if check is done on subbranch) or Topic (via sub_branch)
        if hasattr(obj, 'branch'):
            return obj.branch.domain.user == request.user

        # For Topic
        if hasattr(obj, 'sub_branch'):
            return obj.sub_branch.branch.domain.user == request.user
        
        return False
