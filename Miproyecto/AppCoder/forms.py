from django import forms
from datetime import date
from .models import Autor, Libro, Biblioteca

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ["nombre","apellido","fecha_nacimiento","nacionalidad"]
    
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        if Autor.objects.filter(nombre=nombre, apellido=apellido).exists():
            raise forms.ValidationError("Ya existe un autor con ese nombre y apellido.")
    
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha



# class LibroForm(forms.ModelForm):
#     class Meta:
#         model = Libro
#         fields = ["titulo","genero","fecha_publicacion","isbn","resumen","autor_id"]
        
# class BibliotecaForm(forms.ModelForm):
#     class Meta:
#         model = Biblioteca
#         fields = ["nombre","direccion"]

# class BibliotecaLibros(forms.ModelForm):
#     class Meta:
#         model = Biblioteca
#         fields = ["biblioteca_id","libro_id"]