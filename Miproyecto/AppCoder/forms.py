from django import forms
from datetime import date
from .models import Autor, Libro, Biblioteca


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        }
    
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



class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
        widgets = {
            'fecha_publicacion': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        }
    
    def clean(self):
        cleaned_data = super().clean()
        isbn1 = cleaned_data.get("isbn")
        if Libro.objects.filter(isbn=isbn1).exists():
            raise forms.ValidationError("Ya existe ese libro, el ISBN ya existe")
    
    def clean_fecha_publicacion(self):
        fecha = self.cleaned_data.get("fecha_publicacion")
        if fecha > date.today():
            raise forms.ValidationError("La fecha de publicacion no puede ser futura.")
        return fecha
    

        
class BibliotecaForm(forms.ModelForm):
    libros = forms.ModelMultipleChoiceField(
        queryset=Libro.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=False
    )
    class Meta:
        model = Biblioteca
        fields = '__all__'
    
class BuscarBibliotecaForm(forms.Form):
    biblioteca = forms.ModelChoiceField(
        queryset=Biblioteca.objects.all(),
        label="Seleccioná una biblioteca",
        empty_label="Elegí una biblioteca",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
