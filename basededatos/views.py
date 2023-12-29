# basededatos/views.py
from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    # Lógica de la vista
    return render(request, 'core/inicio.html', {'user': request.user})

def login_view(request):
    # Lógica de la vista de inicio de sesión
    return render(request, 'core/login.html')

def registro_view(request):
    # Lógica de la vista de registro
    return render(request, 'core/registro.html')

def registro(request):
    # Lógica de la vista de registro
    return render(request, 'core/signup.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('core/inicio')