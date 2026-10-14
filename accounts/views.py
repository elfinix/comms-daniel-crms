from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from inventory.models import Vehicle, SavedVehicle
from appointments.models import Appointment

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    saved_vehicles = SavedVehicle.objects.filter(customer=request.user).select_related('vehicle')
    appointments = Appointment.objects.filter(customer=request.user).select_related('vehicle', 'slot')
    return render(request, 'accounts/dashboard.html', {
        'saved_vehicles': saved_vehicles,
        'appointments': appointments,
    })

@login_required
def save_vehicle(request, vehicle_id):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        SavedVehicle.objects.get_or_create(customer=request.user, vehicle=vehicle)
    return redirect('showroom:vehicle_detail', pk=vehicle_id)
