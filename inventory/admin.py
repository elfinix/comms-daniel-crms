from django.contrib import admin
from .models import DealershipSetting, SavedVehicle, Vehicle, VehicleImage

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("year", "make", "model", "body_style", "price", "status", "is_featured")
    list_filter = ("status", "body_style", "fuel_type", "transmission", "is_featured")
    search_fields = ("make", "model", "body_style")
    list_editable = ("status", "is_featured")
    inlines = [VehicleImageInline]

@admin.register(SavedVehicle)
class SavedVehicleAdmin(admin.ModelAdmin):
    list_display = ("customer", "vehicle", "created_at")
    search_fields = ("customer__username", "vehicle__make", "vehicle__model")

@admin.register(DealershipSetting)
class DealershipSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "updated_at")
    search_fields = ("key", "value")
