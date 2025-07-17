"""
URL configuration for Miproyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from AppCoder import views as appcoder_views
from Usuario import views as usuario_views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appcoder_views.index, name='index'),
    path('autores/', appcoder_views.autores, name='autores'),
    path('libros/',appcoder_views.libros, name='libros'),
    path('bibliotecas/', appcoder_views.bibliotecas, name='bibliotecas'),
    path('buscar_biblioteca/', appcoder_views.buscar_biblioteca, name='buscar_biblioteca'),
    path('biblioteca/<int:biblioteca_id>/agregar-libro/', appcoder_views.agregar_libro_a_biblioteca, name='agregar_libro_a_biblioteca'),
    path('libro/<int:libro_id>/editar/', appcoder_views.editar_libro, name='editar_libro'),
    path('libro/<int:libro_id>/eliminar/', appcoder_views.eliminar_libro, name='eliminar_libro'),
    path('editarPerfil/', usuario_views.editarPerfil, name='editarPerfil'),
    path('login/', LoginView.as_view(
        template_name='Usuario/login.html',
        redirect_authenticated_user=True,
        next_page='index' 
    ), name='login'),
    path('logout/', usuario_views.cerrar_sesion, name='logout'),
    path('register/', usuario_views.registro, name='register'),
    path('sobre-mi/', appcoder_views.sobre_mi, name='sobre_mi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
