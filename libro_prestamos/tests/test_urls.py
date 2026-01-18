"""
Tests para las URLs de cambio de contraseña
"""
import pytest
from django.urls import reverse, resolve
from usuarios import views as usuarios_views
from libros import views as libros_views
from prestamos import views as prestamos_views
from core import views as core_views


@pytest.mark.django_db
class TestPasswordURLs:
    """Tests para verificar que las URLs están correctamente configuradas"""
    
    def test_solicitar_cambio_password_url(self):
        """Test que la URL de solicitar cambio existe"""
        url = reverse('solicitar_cambio_password')
        assert url == '/password/solicitar/'
        
        # Verificar que resuelve a la vista correcta
        resolved = resolve(url)
        assert resolved.func == usuarios_views.solicitar_cambio_password
    
    def test_confirmar_cambio_password_url(self):
        """Test que la URL de confirmar cambio existe"""
        token = 'test-token-12345'
        url = reverse('confirmar_cambio_password', args=[token])
        assert f'/password/confirmar/{token}/' in url
        
        # Verificar que resuelve a la vista correcta
        resolved = resolve(url)
        assert resolved.func == usuarios_views.confirmar_cambio_password
    
    def test_cambiar_password_desde_perfil_url(self):
        """Test que la URL de cambiar desde perfil existe"""
        url = reverse('cambiar_password_desde_perfil')
        assert url == '/password/cambiar/'
        
        # Verificar que resuelve a la vista correcta
        resolved = resolve(url)
        assert resolved.func == usuarios_views.cambiar_password_desde_perfil
    
    def test_solicitar_cambio_email_url(self):
        """Test que la URL de solicitar cambio de email existe"""
        url = reverse('solicitar_cambio_email')
        assert url == '/email/solicitar/'
        
        # Verificar que resuelve a la vista correcta
        resolved = resolve(url)
        assert resolved.func == usuarios_views.solicitar_cambio_email
    
    def test_confirmar_cambio_email_url(self):
        """Test que la URL de confirmar cambio de email existe"""
        token = 'test-token-12345'
        url = reverse('confirmar_cambio_email', args=[token])
        assert f'/email/confirmar/{token}/' in url
        
        # Verificar que resuelve a la vista correcta
        resolved = resolve(url)
        assert resolved.func == usuarios_views.confirmar_cambio_email
        assert resolved.kwargs['token'] == token
    
    def test_cerrar_sesiones_todas_url(self):
        """Test que la URL de cerrar sesiones existe"""
        url = reverse('cerrar_sesiones_todas')
        assert url == '/security/cerrar-sesiones/'
        
        # Verificar que resuelve a la vista correcta
        resolved = resolve(url)
        assert resolved.func == usuarios_views.cerrar_sesiones_todas
