from django.shortcuts import render, redirect
from .forms import AutorForm, LibroForm, BibliotecaForm, BuscarBibliotecaForm
from .models import Biblioteca
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,"AppCoder/index.html")

def libros(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form.add_error(None, "Los datos son incorrectos")

    else:
        form = LibroForm()
    return render(request,"AppCoder/libros.html",context={"form": form})

def autores(request):
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form.add_error(None, "Los datos son incorrectos")

    else:
        form = AutorForm()
    return render(request,"AppCoder/autores.html",context={"form": form})

def bibliotecas(request):
    if request.method == 'POST':
        form = BibliotecaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            libros = form.cleaned_data['libros']

            biblioteca_existente = Biblioteca.objects.filter(
                nombre__iexact=nombre.strip(),
                direccion__iexact=direccion.strip()
            ).first()

            if biblioteca_existente:
                nuevos_libros = [libro for libro in libros if libro not in biblioteca_existente.libros.all()]
                biblioteca_existente.libros.add(*nuevos_libros)
                biblioteca_existente.save()
                messages.info(request, f"La biblioteca '{nombre}' ya existía. Se agregaron {len(nuevos_libros)} libro(s).")
            else:
                biblioteca = form.save()
                messages.success(request, f"Se creó la nueva biblioteca '{biblioteca.nombre}' correctamente.")

            return redirect('bibliotecas') 
        else:
            form.add_error(None, "Los datos son incorrectos")
    else:
        form = BibliotecaForm()
    return render(request, 'AppCoder/bibliotecas.html', {'form': form})

def buscar_biblioteca(request):
    resultado = None
    libros = []
    
    if request.method == 'POST':
        form = BuscarBibliotecaForm(request.POST)
        if form.is_valid():
            biblioteca = form.cleaned_data['biblioteca']
            resultado = biblioteca
            libros = biblioteca.libros.all()
    else:
        form = BuscarBibliotecaForm()

    return render(request, 'AppCoder/buscar_biblioteca.html', {
        'form': form,
        'biblioteca': resultado,
        'libros': libros
    })