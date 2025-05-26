from rest_framework import permissions


class CheckIsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'client':
            return True
        return False

class CheckIsFreelancer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'freelancer':
            return True
        return False
