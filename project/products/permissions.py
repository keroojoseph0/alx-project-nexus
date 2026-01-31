from rest_framework.permissions import BasePermission
from accounts.models import Role


class IsSellerOwnerForUpdateDelete(BasePermission):
    message = "Not authorized to modify or delete this product."

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                request.user.is_authenticated and
                request.user.role == Role.SELLER and
                obj.seller == request.user
            )

        return True


class IsAdminOrReadOnly(BasePermission):
    message = "Only admins can modify this resource."

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return (
                request.user.is_authenticated and
                request.user.role == Role.ADMIN
            )
        return True