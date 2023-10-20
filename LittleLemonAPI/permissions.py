from rest_framework import permissions
from django.contrib.auth.models import User, Group

from . import views

class IsManager(permissions.BasePermission):
    message = "Only managers are allowed"

    def has_permission(self, request, view):
        return views.userIsManager(request.user)
    
class IsDeliveryCrew(permissions.BasePermission):
    message = "Only delivery crew members are allowed"

    def has_permission(self, request, view):
        return views.userIsDelivery(request.user)