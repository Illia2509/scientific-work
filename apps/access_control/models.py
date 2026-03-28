from django.conf import settings
from django.db import models
from django.utils import timezone

class AccessGrant(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='granted_accesses')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_accesses')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Прив’язка пацієнт-лікар'
        verbose_name_plural = 'Прив’язки пацієнт-лікар'
        constraints = [models.UniqueConstraint(fields=['patient', 'doctor'], name='unique_patient_doctor_grant')]

    def __str__(self):
        return f'{self.patient.email} -> {self.doctor.email}'

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at <= timezone.now():
            return False
        return True
