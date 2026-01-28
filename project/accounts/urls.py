from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('email-verify/', views.email_verification, name='email_verification'),
    path('resend-verification-code/', views.resend_verification_code, name='resend_verification_code'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
]
