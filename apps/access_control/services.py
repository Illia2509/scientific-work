from .models import AccessGrant

def doctor_has_access(doctor, patient):
    grant = AccessGrant.objects.filter(patient=patient, doctor=doctor, is_active=True).order_by('-created_at').first()
    return bool(grant and grant.is_valid())
