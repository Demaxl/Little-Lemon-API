from rest_framework import permissions
from django.contrib.auth.models import User, Group

class IsManager(permissions.BasePermission):
    message = "Only managers are allowed"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()