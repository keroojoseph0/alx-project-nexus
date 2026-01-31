from rest_framework.permissions import BasePermission
from .roles import Role


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == Role.ADMIN
        )
    

class IsSeller(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == Role.SELLER
        )

class IsBuyer(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == Role.BUYER
        )
    