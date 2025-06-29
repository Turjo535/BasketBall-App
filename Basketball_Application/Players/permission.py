# permissions.py
from rest_framework import permissions

class Is_Player(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated and has a Player profile
        return request.user.is_authenticated and hasattr(request.user, 'player')
class Is_Coach(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'coach')