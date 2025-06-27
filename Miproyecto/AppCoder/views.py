from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"AppCoder/index.html")

def libros(request):
    return render(request,"AppCoder/libros.html")

def autores(request):
    return render(request,"AppCoder/autores.html")

def bibliotecas(request):
    return render(request,"AppCoder/bibliotecas.html")