from rest_framework.permissions import BasePermission

class THeatreAuthentication(BasePermission):
    msg="Unauthorized entry"
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if  request.user.usertype=="theater":
                return True
        return False

class CustomerAuthentication(BasePermission):
    msg="Unauthorized entry"
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if  request.user.usertype=="customer":
                return True
        return False

class AdminAuthentication(BasePermission):
    msg="Unauthorized entry"
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if  request.user.is_superuser:
                return True
        return False



