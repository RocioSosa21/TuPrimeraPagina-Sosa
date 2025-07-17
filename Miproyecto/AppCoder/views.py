from django.shortcuts import render, redirect
from .forms import AutorForm, LibroForm, BibliotecaForm, BuscarBibliotecaForm, AgregarLibroABibliotecaForm
from .models import Biblioteca, Libro
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class BibliotecaListView(ListView):
    model = Biblioteca
    template_name = 'AppCoder/lista_bibliotecas.html'
    context_object_name = 'bibliotecas'

class BibliotecaDetailView(DetailView):
    model = Biblioteca
    template_name = 'AppCoder/detalle_biblioteca.html'
    context_object_name = 'biblioteca'

class BibliotecaUpdateView(LoginRequiredMixin, UpdateView):
    model = Biblioteca
    form_class = BibliotecaForm
    template_name = 'AppCoder/editar_biblioteca.html'
    success_url = reverse_lazy('lista_bibliotecas')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.libros.set(form.cleaned_data['libros'])  
        return response

class BibliotecaDeleteView(LoginRequiredMixin, DeleteView):
    model = Biblioteca
    template_name = 'AppCoder/eliminar_biblioteca.html'
    success_url = reverse_lazy('lista_bibliotecas')

@login_required
def agregar_libro_a_biblioteca(request, biblioteca_id):
    biblioteca = get_object_or_404(Biblioteca, id=biblioteca_id)

    if request.method == 'POST':
        form = AgregarLibroABibliotecaForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['crear_nuevo']:
                nuevo_libro = Libro.objects.create(
                    titulo=form.cleaned_data['titulo'],
                    autor=form.cleaned_data['autor'],
                    genero=form.cleaned_data['genero'],
                    fecha_publicacion=form.cleaned_data['fecha_publicacion'],
                    isbn=form.cleaned_data['isbn'],
                    resumen=form.cleaned_data['resumen']
                )
                biblioteca.libros.add(nuevo_libro)
                messages.success(request, f"Se agregó el libro '{nuevo_libro.titulo}' a la biblioteca.")
            else:
                libro = form.cleaned_data['libro_existente']
                if libro not in biblioteca.libros.all():
                    biblioteca.libros.add(libro)
                    messages.success(request, f"Se agregó el libro '{libro.titulo}' a la biblioteca.")
                else:
                    messages.info(request, "Ese libro ya estaba en la biblioteca.")
            return redirect('buscar_biblioteca')
    else:
        form = AgregarLibroABibliotecaForm()

    return render(request, 'AppCoder/agregar_libro.html', {
        'form': form,
        'biblioteca': biblioteca
    })


@login_required
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, f"El libro '{libro.titulo}' fue actualizado.")
            return redirect('buscar_biblioteca')
    else:
        form = LibroForm(instance=libro)

    return render(request, "AppCoder/editar_libro.html", {
        "form": form,
        "libro": libro
    })

@login_required
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == "POST":
        titulo = libro.titulo
        libro.delete()
        messages.success(request, f"El libro '{titulo}' fue eliminado correctamente.")
        return redirect('buscar_biblioteca')

    return render(request, "AppCoder/eliminar_libro.html", {
        "libro": libro
    })

def sobre_mi(request):
    return render(request, 'AppCoder/sobre_mi.html')

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
    form = BuscarBibliotecaForm(request.GET or None)
    bibliotecas = []

    if form.is_valid():
        biblioteca = form.cleaned_data.get('biblioteca')
        if biblioteca:
            bibliotecas = [biblioteca] 

    return render(request, 'AppCoder/buscar_biblioteca.html', {
        'form': form,
        'bibliotecas': bibliotecas
    })
