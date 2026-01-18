from django.urls import path
from . import views

urlpatterns = [
    path('crear', views.crear_prestamo, name='crear_prestamo'),
    path('', views.listar_prestamos, name='listar_prestamos'),
    path('historial', views.historial_prestamos, name='historial_prestamos'),
    path('marcar_devuelto/<int:prestamo_id>/', views.marcar_devuelto, name='marcar_devuelto'),
]
