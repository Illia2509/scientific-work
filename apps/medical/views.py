from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.users.models import RoleChoices, User
from apps.access_control.models import AccessGrant
from apps.access_control.services import doctor_has_access
from .forms import PatientProfileForm
from .models import DoctorProfile, MedicalRecord, PatientProfile

@login_required
def profile_view(request):
    if request.user.role != RoleChoices.PATIENT:
        return redirect('dashboard')
    profile, _ = PatientProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PatientProfileForm(instance=profile)
    doctors = User.objects.filter(role=RoleChoices.DOCTOR).select_related('doctor_profile').order_by('first_name', 'last_name', 'email')
    active_grants = {g.doctor_id: g for g in AccessGrant.objects.filter(patient=request.user, is_active=True)}
    return render(request, 'medical/profile.html', {
        'form': form,
        'doctors': doctors,
        'active_grants': active_grants,
    })

@login_required
def medical_book_view(request):
    if request.user.role != RoleChoices.PATIENT:
        return redirect('dashboard')
    records = MedicalRecord.objects.filter(patient=request.user).select_related('author', 'author__doctor_profile').prefetch_related('attachments')
    return render(request, 'medical/book.html', {'records': records, 'owner': request.user, 'is_owner': True})

@login_required
def doctor_dashboard(request):
    if request.user.role != RoleChoices.DOCTOR:
        return redirect('dashboard')
    grants = AccessGrant.objects.filter(doctor=request.user, is_active=True).select_related('patient')
    profile = getattr(request.user, 'doctor_profile', None)
    return render(request, 'medical/doctor_dashboard.html', {'grants': grants, 'doctor_profile': profile})

@login_required
def doctor_patient_book(request, patient_id):
    if request.user.role != RoleChoices.DOCTOR:
        return redirect('dashboard')
    patient = get_object_or_404(User, id=patient_id, role=RoleChoices.PATIENT)
    if not doctor_has_access(request.user, patient):
        return redirect('doctor_dashboard')
    records = MedicalRecord.objects.filter(patient=patient).select_related('author', 'author__doctor_profile').prefetch_related('attachments')
    return render(request, 'medical/book.html', {'records': records, 'owner': patient, 'is_owner': False})
