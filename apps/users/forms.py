from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, RoleChoices
from apps.medical.models import PatientProfile

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label="Ім'я", required=False)
    last_name = forms.CharField(label='Прізвище', required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')
        labels = {'username': 'Логін'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = RoleChoices.PATIENT
        if commit:
            user.save()
            PatientProfile.objects.get_or_create(user=user)
        return user
