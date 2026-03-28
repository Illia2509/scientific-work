from django.conf import settings
from django.db import models
from apps.users.models import RoleChoices

class DoctorProfile(models.Model):
    class SpecialtyChoices(models.TextChoices):
        SURGEON = 'surgeon', 'Хірург'
        NURSE = 'nurse', 'Медсестра'
        PROCTOLOGIST = 'proctologist', 'Проктолог'
        ONCOLOGIST = 'oncologist', 'Онколог'
        DERMATOLOGIST = 'dermatologist', 'Дерматолог'
        THERAPIST = 'therapist', 'Терапевт'
        CARDIOLOGIST = 'cardiologist', 'Кардіолог'
        NEUROLOGIST = 'neurologist', 'Невролог'

    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Активний'
        ON_LEAVE = 'on_leave', 'У відпустці'
        INACTIVE = 'inactive', 'Неактивний'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=30, choices=SpecialtyChoices.choices)
    position = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    phone = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Профіль лікаря'
        verbose_name_plural = 'Профілі лікарів'


    def save(self, *args, **kwargs):
        if self.user and self.user.role != RoleChoices.DOCTOR:
            self.user.role = RoleChoices.DOCTOR
            if not self.user.is_superuser:
                self.user.is_staff = True
            self.user.save(update_fields=['role', 'is_staff'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.email} - {self.get_specialty_display()}'

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Профіль пацієнта'
        verbose_name_plural = 'Профілі пацієнтів'

    def __str__(self):
        return self.user.email

class MedicalRecord(models.Model):
    class RecordType(models.TextChoices):
        VISIT = 'visit', 'Візит'
        DIAGNOSIS = 'diagnosis', 'Діагноз'
        TEST = 'test', 'Аналіз'
        PRESCRIPTION = 'prescription', 'Призначення'
        NOTE = 'note', 'Нотатка'

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_records')
    title = models.CharField(max_length=200)
    record_type = models.CharField(max_length=20, choices=RecordType.choices)
    description = models.TextField()
    visit_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Медичний запис'
        verbose_name_plural = 'Медичні записи'
        ordering = ['-visit_date', '-created_at']

    def clean(self):
        if self.patient and self.patient.role != RoleChoices.PATIENT:
            raise ValidationError('Пацієнтом може бути лише користувач з роллю patient.')
        if self.author and self.author.role != RoleChoices.DOCTOR:
            raise ValidationError('Автором запису може бути лише лікар.')

    def __str__(self):
        return f'{self.patient.email} - {self.title}'

class RecordAttachment(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='records/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вкладення'
        verbose_name_plural = 'Вкладення'
