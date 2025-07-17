from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatars/', blank=True, null=True)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    