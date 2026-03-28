from django.contrib import admin
from .models import AccessGrant

@admin.register(AccessGrant)
class AccessGrantAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('patient__email', 'doctor__email')
