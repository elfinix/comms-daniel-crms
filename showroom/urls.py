from django.urls import path

from .views import home, showroom_list, vehicle_detail

app_name = "showroom"

urlpatterns = [
    path("", home, name="home"),
    path("inventory/", showroom_list, name="inventory"),
    path("showroom/", showroom_list, name="showroom"),
    path("vehicle/<int:pk>/", vehicle_detail, name="vehicle_detail"),
]
