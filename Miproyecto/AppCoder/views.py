from django.shortcuts import render, redirect
from .forms import AutorForm

# Create your views here.
def index(request):
    return render(request,"AppCoder/index.html")

def libros(request):
    return render(request,"AppCoder/libros.html")

def libros_create(request):
    return render(request, "AppCoder/libros.html")

def autores(request):
    return render(request, "AppCoder/autores.html")

def autores_create(request):
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
    return render(request,"AppCoder/bibliotecas.html")