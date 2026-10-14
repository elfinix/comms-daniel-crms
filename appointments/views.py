import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import Vehicle
from .models import Appointment, AppointmentSlot

@login_required
def request_appointment(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    slots = AppointmentSlot.objects.filter(is_active=True).order_by('starts_at')

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        notes = request.POST.get('notes', '')
        kind = request.POST.get('kind', 'test_drive')
        slot = get_object_or_404(AppointmentSlot, pk=slot_id)

        reference = f"APX-{uuid.uuid4().hex[:8].upper()}"
        Appointment.objects.create(
            reference=reference,
            kind=kind,
            status='pending',
            notes=notes,
            customer=request.user,
            vehicle=vehicle,
            slot=slot,
        )
        return redirect('accounts:dashboard')

    return render(request, 'appointments/request.html', {
        'vehicle': vehicle,
        'slots': slots,
    })
