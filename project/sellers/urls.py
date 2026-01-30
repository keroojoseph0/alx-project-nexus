from django.urls import path
from . import views

app_name = 'instructors'


urlpatterns = [
    path('apply/', views.apply_as_seller, name='apply_as_seller'),
]
