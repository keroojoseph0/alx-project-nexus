from django.contrib import admin
from .models import SellerApplication, Status
from accounts.models import Role
from accounts.tasks import send_email
from django.db import transaction
from rest_framework import status

# Register your models here.

@admin.register(SellerApplication)
class SellerApplicationAdmin(admin.ModelAdmin):
    list_display = ('seller', 'status')
    list_filter = ('status',)
    search_fields = ('seller__email', 'seller__first_name', 'seller__last_name')
    actions = ['approve_seller', 'reject_seller']
    
    def approve_seller(self, request, queryset):
        for application in queryset:
            user = application.user

            with transaction.atomic():
                user.role = Role.SELLER
                user.save()

                if application.status == Status.APPROVED:
                    continue

                application.status = Status.APPROVED
                application.save()

            # Send email OUTSIDE transaction
            subject = "Seller Approval"
            message = "Congratulations! Your seller application has been approved."
            send_email.delay(user.id, subject, message)

    def reject_seller(self, request, queryset):
        for application in queryset:
            user = application.user

            if application.status == Status.REJECTED:
                    continue

            application.status = Status.REJECTED
            application.save()

            subject = "Seller Application Rejected"
            message = "We regret to inform you that your seller application has been rejected can apply after 30 days"
            send_email.delay(user.id, subject, message)

    approve_seller.short_description = "Approve selected sellers application"
    reject_seller.short_description = "Reject selected sellers application"