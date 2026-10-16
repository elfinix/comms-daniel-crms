from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from inventory.models import DealershipSetting, Vehicle

DEFAULT_SETTINGS = {
    "dealership_name": "NOBLESSE MOTOR CARS",
    "hero_headline": "Find the car that feels like you.",
    "phone": "+1 (800) 555-NOBLE",
    "concierge_email": "concierge@noblessemotorcars.com",
    "showroom_address": "1000 Luxury Way, Suite 500, Beverly Hills, CA",
    "service_hours": "Monday - Saturday: 9:00 AM - 7:00 PM (By Private Appointment)",
    "warranty_teaser": "36-Month Certified Warranty",
    "financing_rate_teaser": "3.99% Bespoke Tier-1 APR",
    "aerospace_certified": "100% Aerospace Certified",
}


def get_dealership_settings():
    settings_dict = DEFAULT_SETTINGS.copy()
    for s in DealershipSetting.objects.all():
        if s.value:
            settings_dict[s.key] = s.value
    return settings_dict


def home(request):
    """
    Landing Page:
    1. Header (with custom SVG logo)
    2. Hero section (with Shop Now CTA)
    3. Newest Listing
    4. Shopping by Category 1 (Body Style)
    5. Shopping by Category 2 (Powertrain/Fuel)
    6. About Noblesse Motor Cars
    7. About the Developer
    8. Final Call to Action Banner to Shop Now
    9. Footer
    """
    settings_dict = get_dealership_settings()

    # Newest listings (top 4 available vehicles)
    newest_vehicles = Vehicle.objects.filter(status="available").order_by(
        "-is_featured", "-created_at"
    )[:4]

    # Category 1: Body styles dynamically aggregated from DB
    style_aggregates = (
        Vehicle.objects.filter(status="available")
        .values("body_style")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    fallback_images = [
        "/media/vehicles/2026/10/range-rover-autobiography.jpg",
        "/media/vehicles/2026/10/porsche-911-carrera-4s.jpg",
        "/media/vehicles/2026/10/mercedes-amg-s63-e.jpg",
        "/media/vehicles/2026/10/apex-hyperion-aeterna.jpg",
        "/media/vehicles/2026/10/aston-martin-db12.jpg",
    ]

    body_styles = []
    for idx, item in enumerate(style_aggregates):
        name = (item["body_style"] or "").strip()
        if not name:
            continue
        v_sample = Vehicle.objects.filter(body_style=name, status="available").first()
        cover_url = None
        if v_sample:
            first_img = v_sample.images.first()
            if first_img and first_img.image:
                cover_url = first_img.image.url
        if not cover_url:
            cover_url = fallback_images[idx % len(fallback_images)]

        body_styles.append({
            "name": name,
            "title": f"{name} Silhouette" if "silhouette" not in name.lower() and len(name) < 25 else name,
            "desc": f"Explore our curated selection of {name} models, each certified and prepared for immediate delivery.",
            "count": item["count"],
            "image": cover_url,
        })

    # Category 2: Powertrain / Fuel Types dynamically aggregated from DB
    fuel_aggregates = (
        Vehicle.objects.filter(status="available")
        .values("fuel_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    fuel_types = []
    for idx, item in enumerate(fuel_aggregates):
        raw_fuel = (item["fuel_type"] or "").strip()
        if not raw_fuel:
            continue
        clean_name = raw_fuel.lstrip("•-* ").strip()
        v_sample = Vehicle.objects.filter(fuel_type=raw_fuel, status="available").first()
        cover_url = None
        if v_sample:
            first_img = v_sample.images.first()
            if first_img and first_img.image:
                cover_url = first_img.image.url
        if not cover_url:
            cover_url = fallback_images[(idx + 2) % len(fallback_images)]

        f_lower = clean_name.lower()
        if "electric" in f_lower or "ev" in f_lower:
            badge = "Zero Emission"
        elif "hybrid" in f_lower or "hev" in f_lower:
            badge = "Electrified Hybrid"
        elif "turbo" in f_lower:
            badge = "Turbocharged Performance"
        elif "v6" in f_lower or "v8" in f_lower or "gasoline" in f_lower:
            badge = "High-Output Combustion"
        else:
            badge = "Precision Engineered"

        fuel_types.append({
            "name": raw_fuel,
            "title": clean_name,
            "badge": badge,
            "desc": f"High-precision engineering and responsive performance delivering exhilarating dynamics.",
            "count": item["count"],
            "image": cover_url,
        })

    context = {
        "settings": settings_dict,
        "newest_vehicles": newest_vehicles,
        "body_styles": body_styles,
        "fuel_types": fuel_types,
        "total_available": Vehicle.objects.filter(status="available").count(),
    }
    return render(request, "showroom/home.html", context)


def showroom_list(request):
    """
    Dedicated Listing / Showroom Page:
    - Search by keyword
    - Multi-filter by body_style, fuel_type, status, price range
    - Sorting by price, year, mileage
    """
    query = request.GET.get("q", "").strip()
    body_style = request.GET.get("body_style", "").strip()
    fuel_type = request.GET.get("fuel_type", "").strip()
    status_filter = request.GET.get("status", "available").strip()
    sort_by = request.GET.get("sort", "-is_featured").strip()

    vehicles = Vehicle.objects.all()

    if status_filter and status_filter != "all":
        vehicles = vehicles.filter(status=status_filter)

    if query:
        vehicles = vehicles.filter(
            Q(make__icontains=query)
            | Q(model__icontains=query)
            | Q(body_style__icontains=query)
            | Q(fuel_type__icontains=query)
            | Q(description__icontains=query)
        )

    if body_style and body_style != "all":
        vehicles = vehicles.filter(body_style__iexact=body_style)

    if fuel_type and fuel_type != "all":
        vehicles = vehicles.filter(fuel_type__iexact=fuel_type)

    # Sorting
    sort_mapping = {
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-year",
        "mileage": "mileage",
        "-is_featured": "-is_featured",
    }
    order_field = sort_mapping.get(sort_by, "-is_featured")
    vehicles = vehicles.order_by(order_field, "-created_at")

    raw_styles = Vehicle.objects.values_list("body_style", flat=True).distinct().order_by("body_style")
    available_styles = [
        {"name": s, "count": Vehicle.objects.filter(body_style=s).count()}
        for s in raw_styles
    ]

    raw_fuels = Vehicle.objects.values_list("fuel_type", flat=True).distinct().order_by("fuel_type")
    available_fuels = [
        {"name": f, "count": Vehicle.objects.filter(fuel_type=f).count()}
        for f in raw_fuels
    ]

    settings_dict = get_dealership_settings()

    context = {
        "vehicles": vehicles,
        "query": query,
        "selected_body_style": body_style,
        "selected_fuel_type": fuel_type,
        "selected_status": status_filter,
        "selected_sort": sort_by,
        "available_styles": available_styles,
        "available_fuels": available_fuels,
        "settings": settings_dict,
        "total_count": vehicles.count(),
        "total_inventory": Vehicle.objects.count(),
    }
    return render(request, "showroom/inventory_list.html", context)


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    settings_dict = get_dealership_settings()
    related_vehicles = Vehicle.objects.filter(status="available").exclude(pk=pk).order_by("-is_featured")[:3]
    return render(
        request,
        "showroom/vehicle_detail.html",
        {
            "vehicle": vehicle,
            "settings": settings_dict,
            "related_vehicles": related_vehicles,
        },
    )
