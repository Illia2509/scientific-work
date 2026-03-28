from django import forms
from .models import PatientProfile

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'phone', 'date_of_birth', 'address', 'blood_group',
            'allergies', 'chronic_conditions', 'emergency_contact_name', 'emergency_contact_phone'
        ]
        labels = {
            'phone': 'Телефон',
            'date_of_birth': 'Дата народження',
            'address': 'Адреса',
            'blood_group': 'Група крові',
            'allergies': 'Алергії',
            'chronic_conditions': 'Хронічні стани',
            'emergency_contact_name': 'Контактна особа',
            'emergency_contact_phone': 'Телефон контактної особи',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 3}),
        }
