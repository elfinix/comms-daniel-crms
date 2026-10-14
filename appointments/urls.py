from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('request/<int:vehicle_id>/', views.request_appointment, name='request_appointment'),
]
