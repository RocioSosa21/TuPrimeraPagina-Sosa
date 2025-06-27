from django.contrib import admin
from .models import Autor, Libro, Biblioteca

admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Biblioteca)
