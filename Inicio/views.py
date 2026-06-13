
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def apertura(request):
    return render(request, 'usuarios/apertura.html')

def dashboard(request):

    context = {
        "total_vehiculos": Vehiculo.objects.count(),
        "total_usuarios": User.objects.count(),
        "total_tecnicos": User.objects.filter(groups__name="Tecnico").count(),
        "total_servicios": 25,
        "vehiculos": Vehiculo.objects.all()[:10]
    }

    return render(request, "dashboard.html", context)


#funciones de Logueo
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            
            print("Usuario:", user.username)
            print("Grupos:", [g.name for g in user.groups.all()])


            if user.groups.filter(name='Administrador').exists():
                return redirect('admin')

            elif user.groups.filter(name='Administrativo').exists():
                return redirect('principal_admin')

            elif user.groups.filter(name='Tecnico').exists():
                return redirect('principal_tecni')

            return redirect('apertura')

        messages.error(
            request,
            'Usuario o contraseña incorrectos.'
        )

    return render(request, 'registration/login.html')


#funcion de cierre de sesion
def logout_view(request):
    logout(request)
    return redirect('apertura')


#funciones de tecnicos
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Tecnico').exists())

def tecnicos (request):
    return render(request, 'tecnicos/principal_tecni.html')