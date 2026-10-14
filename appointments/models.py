from django.conf import settings
from django.db import models
from inventory.models import Vehicle


class AppointmentSlot(models.Model):
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.starts_at.strftime('%b %d, %Y %I:%M %p')}"


class Appointment(models.Model):
    reference = models.CharField(max_length=32, unique=True)
    kind = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reference} - {self.kind} ({self.status})"
