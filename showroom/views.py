from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from inventory.models import Vehicle


def home(request):
    query = request.GET.get("q", "").strip()
    vehicles = Vehicle.objects.filter(status="available")

    if query:
        vehicles = vehicles.filter(
            Q(make__icontains=query)
            | Q(model__icontains=query)
            | Q(body_style__icontains=query)
            | Q(fuel_type__icontains=query)
        )

    return render(request, "showroom/home.html", {"vehicles": vehicles, "query": query})


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, "showroom/vehicle_detail.html", {"vehicle": vehicle})
