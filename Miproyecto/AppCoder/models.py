from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    genero = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    resumen = models.TextField(blank=True)

    def __str__(self):
        return self.titulo
    
class Biblioteca(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    libros = models.ManyToManyField(Libro, related_name='bibliotecas')

    def __str__(self):
        return self.nombre
    
