from django.contrib import admin
from .models import User, EmailVerification

# Register your models here.


admin.site.site_header = "Education App Admin"
admin.site.site_title = "Education App Admin Portal"
admin.site.index_title = "Welcome to Education App Admin Portal"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at')
    ordering = ('created_at',)


admin.site.register(EmailVerification)