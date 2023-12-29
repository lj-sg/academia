# basededatos/urls.py

from django.urls import path
from .views import registro



urlpatterns = [
    # Otras URL
    path('registro/', registro, name='registro'),
]
