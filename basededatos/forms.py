# basededatos/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=30)
    apellido = forms.CharField(max_length=30)
    telefono = forms.CharField(max_length=15)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'username', 'email', 'password1', 'password2']
