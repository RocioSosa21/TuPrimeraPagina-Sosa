from django.shortcuts import render, redirect
from .forms import AutorForm, LibroForm, BibliotecaForm

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
    if request.method == "POST":
        form = BibliotecaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form.add_error(None, "Los datos son incorrectos")

    else:
        form = BibliotecaForm()
    return render(request,"AppCoder/bibliotecas.html",context={"form": form})