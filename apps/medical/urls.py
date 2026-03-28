from django.urls import path
from .views import profile_view, medical_book_view, doctor_dashboard, doctor_patient_book
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('medical-book/', medical_book_view, name='medical_book'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patient/<int:patient_id>/', doctor_patient_book, name='doctor_patient_book'),
]
