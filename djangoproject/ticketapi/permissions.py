from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        required_group = getattr(view, 'required_group', None)

        if required_group:
            return request.user.groups.filter(name=required_group).exists()
        
        return false

class IsTicketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer_id == request.user