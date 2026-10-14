from django.db import models


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("sold", "Sold"),
    ]

    make = models.CharField(max_length=80)
    model = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    body_style = models.CharField(max_length=40)
    fuel_type = models.CharField(max_length=40)
    transmission = models.CharField(max_length=40)
    mileage = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicles/%Y/%m/")
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Photo for {self.vehicle}"


class SavedVehicle(models.Model):
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="saved_vehicles")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="saved_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["customer", "vehicle"], name="unique_saved_vehicle")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer} saved {self.vehicle}"


class DealershipSetting(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
