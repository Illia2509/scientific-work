from django.urls import path
from .views import grant_access, revoke_access
urlpatterns = [
    path('grant/<int:doctor_id>/', grant_access, name='grant_access'),
    path('revoke/<int:doctor_id>/', revoke_access, name='revoke_access'),
]
