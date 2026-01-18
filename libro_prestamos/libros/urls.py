from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_libros, name='listar_libros'),
    path('my', views.listar_mis_libros, name='listar_mis_libros'),
    path('cargar/', views.cargar_libro, name='cargar_libro'),
    path('cargar-masivo/', views.cargar_libros_masivo, name='cargar_libros_masivo'),
    path('descargar-plantilla/', views.descargar_plantilla_excel, name='descargar_plantilla_excel'),
    path('ver/<int:id>/', views.libro_detalle, name='libro_detalle'),
    path('<int:id>/editar/', views.editar_libro, name='editar_libro'),
    path('<int:id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
]
