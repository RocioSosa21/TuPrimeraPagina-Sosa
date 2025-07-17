from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, EditarPerfilForm
from django.contrib.auth import logout
from .models import Perfil
from django.contrib import messages

@login_required
def editarPerfil(request):
    perfil, creado = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil, user=request.user, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('index')
        else:
            messages.error(request, 'Ocurrió un error al actualizar el perfil.')
    else:
        form = EditarPerfilForm(instance=perfil, user=request.user, request=request)

    return render(request, 'Usuario/editarPerfil.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'Usuario/registro.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')
