from django.contrib import admin
from .models import Appointment, AppointmentSlot

@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('starts_at', 'ends_at', 'capacity', 'is_active')
    list_filter = ('is_active',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'customer', 'vehicle', 'kind', 'status', 'created_at')
    list_filter = ('kind', 'status')
    search_fields = ('reference', 'customer__username', 'notes')
