"""
URL configuration for libro_prestamos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path("admin/", admin.site.urls),
    path('libros/', views.listar_libros, name='listar_libros'),
    path('libros/my', views.listar_mis_libros, name='listar_mis_libros'),
    path('libros/cargar/', views.cargar_libro, name='cargar_libro'),
    path('libros/cargar-masivo/', views.cargar_libros_masivo, name='cargar_libros_masivo'),
    path('libros/descargar-plantilla/', views.descargar_plantilla_excel, name='descargar_plantilla_excel'),
    path('libros/ver/<int:id>/', views.libro_detalle, name='libro_detalle'),
    path('libros/<int:id>/editar/', views.editar_libro, name='editar_libro'),
    path('libros/<int:id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    path('prestamos/crear', views.crear_prestamo, name='crear_prestamo'),
    path('prestamos/', views.listar_prestamos, name='listar_prestamos'),
    path('prestamos/historial', views.historial_prestamos, name='historial_prestamos'),
    path('prestamos/marcar_devuelto/<int:prestamo_id>/', views.marcar_devuelto, name='marcar_devuelto'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    # Cambio de contraseña
    path('password/solicitar/', views.solicitar_cambio_password, name='solicitar_cambio_password'),
    path('password/confirmar/<str:token>/', views.confirmar_cambio_password, name='confirmar_cambio_password'),
    path('password/cambiar/', views.cambiar_password_desde_perfil, name='cambiar_password_desde_perfil'),
]
