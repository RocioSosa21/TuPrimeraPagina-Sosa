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

class AgregarLibroABibliotecaForm(forms.Form):
    libro_existente = forms.ModelChoiceField(
        queryset=Libro.objects.all(),
        required=False,
        label="Seleccionar un libro existente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    crear_nuevo = forms.BooleanField(
        required=False,
        label="¿Querés crear un nuevo libro?"
    )
    titulo = forms.CharField(required=False)
    autor = forms.ModelChoiceField(queryset=Autor.objects.all(), required=False)
    genero = forms.CharField(required=False)
    fecha_publicacion = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    isbn = forms.CharField(required=False)
    resumen = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        crear_nuevo = cleaned_data.get("crear_nuevo")

        if crear_nuevo:
            campos_requeridos = ['titulo', 'autor', 'genero', 'fecha_publicacion', 'isbn']
            for campo in campos_requeridos:
                if not cleaned_data.get(campo):
                    raise forms.ValidationError(f"El campo {campo} es obligatorio para crear un nuevo libro.")
                    
            isbn = cleaned_data.get('isbn')
            if Libro.objects.filter(isbn=isbn).exists():
                raise forms.ValidationError("Ya existe un libro con ese ISBN.")
        else:
            if not cleaned_data.get("libro_existente"):
                raise forms.ValidationError("Debés seleccionar un libro existente o crear uno nuevo.")


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
        isbn = cleaned_data.get("isbn")
        if isbn and Libro.objects.filter(isbn=isbn).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ya existe un libro con ese ISBN.")
    
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bibliotecas = Biblioteca.objects.all()
        if bibliotecas.exists():
            self.fields['biblioteca'] = forms.ModelChoiceField(
                queryset=bibliotecas,
                label="Seleccioná una biblioteca",
                empty_label="Elegí una biblioteca",
                widget=forms.Select(attrs={'class': 'form-select'})
            )
        else:
            self.fields['biblioteca'] = forms.ChoiceField(
                choices=[('', 'No hay bibliotecas para mostrar')],
                widget=forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'})
            )