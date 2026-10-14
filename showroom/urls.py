from django.urls import path

from .views import home, vehicle_detail

app_name = "showroom"

urlpatterns = [
    path("", home, name="home"),
    path("vehicle/<int:pk>/", vehicle_detail, name="vehicle_detail"),
]
