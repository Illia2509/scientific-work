from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from apps.users.models import RoleChoices, User
from .models import AccessGrant

@login_required
def grant_access(request, doctor_id):
    if request.user.role != RoleChoices.PATIENT:
        return redirect('dashboard')
    doctor = User.objects.filter(id=doctor_id, role=RoleChoices.DOCTOR).first()
    if not doctor:
        return redirect('profile')
    grant, _ = AccessGrant.objects.get_or_create(patient=request.user, doctor=doctor)
    grant.is_active = True
    grant.expires_at = None
    grant.save()
    return redirect('profile')

@login_required
def revoke_access(request, doctor_id):
    if request.user.role != RoleChoices.PATIENT:
        return redirect('dashboard')
    AccessGrant.objects.filter(patient=request.user, doctor_id=doctor_id).update(is_active=False)
    return redirect('profile')
