from django.contrib import admin
from apps.users.models import RoleChoices
from .models import DoctorProfile, PatientProfile, MedicalRecord, RecordAttachment

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'position', 'status')
    list_filter = ('specialty', 'status')
    search_fields = ('user__email', 'user__username', 'position', 'license_number')

    def save_model(self, request, obj, form, change):
        if obj.user.role != RoleChoices.DOCTOR:
            obj.user.role = RoleChoices.DOCTOR
            if not obj.user.is_superuser:
                obj.user.is_staff = True
            obj.user.save(update_fields=['role', 'is_staff'])
        super().save_model(request, obj, form, change)

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'blood_group')
    search_fields = ('user__email', 'user__username', 'phone')

class RecordAttachmentInline(admin.TabularInline):
    model = RecordAttachment
    extra = 0

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'author', 'record_type', 'visit_date')
    list_filter = ('record_type', 'visit_date')
    search_fields = ('title', 'patient__email', 'author__email')
    inlines = [RecordAttachmentInline]
