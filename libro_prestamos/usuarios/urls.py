from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    # Cambio de contraseña
    path('password/solicitar/', views.solicitar_cambio_password, name='solicitar_cambio_password'),
    path('password/confirmar/<str:token>/', views.confirmar_cambio_password, name='confirmar_cambio_password'),
    path('password/cambiar/', views.cambiar_password_desde_perfil, name='cambiar_password_desde_perfil'),
    # Cambio de email
    path('email/solicitar/', views.solicitar_cambio_email, name='solicitar_cambio_email'),
    path('email/confirmar/<str:token>/', views.confirmar_cambio_email, name='confirmar_cambio_email'),
    # Seguridad
    path('security/cerrar-sesiones/', views.cerrar_sesiones_todas, name='cerrar_sesiones_todas'),
]
