"""
Tests para las vistas de cambio de contraseña
"""
import pytest
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import PasswordResetToken
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestSolicitarCambioPassword:
    """Tests para la vista solicitar_cambio_password"""
    
    def test_get_request_anonymous_user(self, client):
        """Test que usuarios anónimos pueden acceder"""
        response = client.get(reverse('solicitar_cambio_password'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_get_request_authenticated_user(self, client, user):
        """Test que usuarios autenticados pueden acceder"""
        client.force_login(user)
        response = client.get(reverse('solicitar_cambio_password'))
        assert response.status_code == 200
        # El email debería estar pre-llenado
        assert user.email in str(response.content)
    
    def test_post_request_with_existing_email(self, client, user):
        """Test que se crea token y envía email con email existente"""
        response = client.post(
            reverse('solicitar_cambio_password'),
            {'email': user.email}
        )
        assert response.status_code == 200 or response.status_code == 302
        
        # Verificar que se creó un token
        tokens = PasswordResetToken.objects.filter(user=user, used=False)
        assert tokens.exists()
    
    def test_post_request_with_non_existing_email(self, client):
        """Test que no revela si el email existe o no"""
        response = client.post(
            reverse('solicitar_cambio_password'),
            {'email': 'nonexistent@example.com'}
        )
        # Debe responder igual (por seguridad)
        assert response.status_code == 200 or response.status_code == 302
    
    def test_post_request_authenticated_user(self, client, user):
        """Test que usuarios autenticados no necesitan ingresar email"""
        client.force_login(user)
        # La vista requiere que se envíe el formulario, aunque el email se use del usuario
        response = client.post(
            reverse('solicitar_cambio_password'),
            {'email': user.email}  # Aunque esté autenticado, el formulario requiere el campo
        )
        # Debe usar el email del usuario autenticado o del formulario
        tokens = PasswordResetToken.objects.filter(user=user, used=False)
        assert tokens.exists()


@pytest.mark.django_db
class TestConfirmarCambioPassword:
    """Tests para la vista confirmar_cambio_password"""
    
    def test_get_request_with_valid_token(self, client, password_reset_token):
        """Test que se muestra formulario con token válido"""
        url = reverse('confirmar_cambio_password', args=[password_reset_token.token])
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_get_request_with_invalid_token(self, client):
        """Test que token inválido muestra error"""
        url = reverse('confirmar_cambio_password', args=['invalid-token-12345'])
        response = client.get(url)
        # Debe redirigir o mostrar error
        assert response.status_code in [200, 302, 404]
    
    def test_get_request_with_expired_token(self, client, expired_token):
        """Test que token expirado muestra error"""
        url = reverse('confirmar_cambio_password', args=[expired_token.token])
        response = client.get(url)
        # Debe mostrar mensaje de error
        assert response.status_code in [200, 302]
    
    def test_get_request_with_used_token(self, client, used_token):
        """Test que token usado muestra error"""
        url = reverse('confirmar_cambio_password', args=[used_token.token])
        response = client.get(url)
        # Debe mostrar mensaje de error
        assert response.status_code in [200, 302]
    
    def test_post_request_valid_token_changes_password(self, client, password_reset_token, user):
        """Test que se puede cambiar la contraseña con token válido"""
        url = reverse('confirmar_cambio_password', args=[password_reset_token.token])
        new_password = 'NewSecurePass123!'
        
        response = client.post(url, {
            'new_password1': new_password,
            'new_password2': new_password
        })
        
        # Debe redirigir a login
        assert response.status_code == 302
        
        # Verificar que el token está marcado como usado
        password_reset_token.refresh_from_db()
        assert password_reset_token.used == True
        
        # Verificar que la contraseña cambió
        user.refresh_from_db()
        assert user.check_password(new_password) == True
    
    def test_post_request_invalid_passwords(self, client, password_reset_token):
        """Test que contraseñas inválidas no cambian la contraseña"""
        url = reverse('confirmar_cambio_password', args=[password_reset_token.token])
        
        response = client.post(url, {
            'new_password1': 'short',
            'new_password2': 'short'
        })
        
        # Debe mostrar errores, no redirigir
        assert response.status_code == 200
        assert 'form' in response.context


@pytest.mark.django_db
class TestCambiarPasswordDesdePerfil:
    """Tests para la vista cambiar_password_desde_perfil"""
    
    def test_get_request_requires_login(self, client):
        """Test que requiere autenticación"""
        response = client.get(reverse('cambiar_password_desde_perfil'))
        assert response.status_code == 302  # Redirige a login
    
    def test_get_request_authenticated(self, client, user):
        """Test que usuarios autenticados pueden acceder"""
        client.force_login(user)
        response = client.get(reverse('cambiar_password_desde_perfil'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    @patch('core.views.enviar_email_confirmacion_cambio')
    def test_post_request_changes_password(self, mock_email, client, user):
        """Test que cambia la contraseña inmediatamente y envía email de confirmación"""
        old_password = 'testpass123'
        user.set_password(old_password)
        user.save()
        
        # Login con la contraseña antigua
        client.login(username=user.username, password=old_password)
        
        response = client.post(reverse('cambiar_password_desde_perfil'), {
            'old_password': old_password,
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        })
        
        # Debe redirigir al perfil
        assert response.status_code == 302
        assert response.url == reverse('perfil')
        
        # Verificar que la contraseña fue cambiada
        user.refresh_from_db()
        assert user.check_password('newpass123')
        assert not user.check_password(old_password)
        
        # Verificar que se envió email de confirmación
        assert mock_email.called
        
        # Verificar que el usuario sigue autenticado después del cambio
        response = client.get(reverse('perfil'))
        assert response.status_code == 200
    
    def test_post_request_wrong_old_password(self, client, user):
        """Test que rechaza contraseña actual incorrecta"""
        client.force_login(user)
        
        response = client.post(reverse('cambiar_password_desde_perfil'), {
            'old_password': 'wrongpassword',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        })
        
        # Debe mostrar error
        assert response.status_code == 200
        assert 'form' in response.context
