from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Perfil
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from datetime import date


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresá una dirección de email válida.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña"
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=False)
    biografia = forms.CharField(label="Biografía", widget=forms.Textarea(attrs={'rows': 3}), required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Perfil
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.request = kwargs.pop('request', None) 
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            if hasattr(self.user, 'perfil'):
                self.fields['biografia'].initial = self.user.perfil.biografia or ''
                self.fields['fecha_nacimiento'].initial = self.user.perfil.fecha_nacimiento

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if self.user.check_password(password):
                raise forms.ValidationError("La nueva contraseña no puede ser igual a la anterior.")
            try:
                validate_password(password, self.user)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if imagen.size > 2 * 1024 * 1024: 
                raise forms.ValidationError("La imagen no puede superar los 2 MB.")
        return imagen

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = perfil.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            update_session_auth_hash(self.request, user) 
        if commit:
            user.save()
            perfil.biografia = self.cleaned_data.get('biografia', '')
            perfil.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
            perfil.save()
        return perfil