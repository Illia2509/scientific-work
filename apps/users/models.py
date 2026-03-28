from django.contrib.auth.models import AbstractUser
from django.db import models

class RoleChoices(models.TextChoices):
    PATIENT = 'patient', 'Пацієнт'
    DOCTOR = 'doctor', 'Лікар'
    ADMIN = 'admin', 'Адміністратор'

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.PATIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = RoleChoices.ADMIN
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.email} ({self.role})'
