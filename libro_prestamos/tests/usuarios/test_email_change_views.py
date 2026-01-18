"""
Tests para las vistas de cambio de email
"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from usuarios.models import EmailChangeToken, Perfil
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def user(db):
    """Fixture para crear un usuario de prueba"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    Perfil.objects.create(
        usuario=user,
        ciudad='Buenos Aires',
        pais='Argentina'
    )
    return user


@pytest.mark.django_db
class TestSolicitarCambioEmail:
    """Tests para la vista solicitar_cambio_email"""
    
    def test_get_request_requires_login(self, client):
        """Test que requiere login"""
        response = client.get(reverse('solicitar_cambio_email'))
        
        assert response.status_code == 302  # Redirect to login
    
    def test_get_request_authenticated(self, client, user):
        """Test que usuarios autenticados pueden acceder"""
        client.force_login(user)
        response = client.get(reverse('solicitar_cambio_email'))
        
        assert response.status_code == 200
        assert 'form' in response.context
    
    @pytest.mark.django_db
    def test_post_request_creates_token(self, client, user):
        """Test que crea token y envía email cuando el formulario es válido"""
        client.force_login(user)
        
        response = client.post(reverse('solicitar_cambio_email'), {
            'new_email': 'newemail@example.com',
            'password': 'testpass123'
        })
        
        assert response.status_code == 302
        assert response.url == reverse('perfil')
        assert EmailChangeToken.objects.filter(user=user, new_email='newemail@example.com').exists()
    
    def test_post_request_invalid_password(self, client, user):
        """Test que rechaza contraseña incorrecta"""
        client.force_login(user)
        
        response = client.post(reverse('solicitar_cambio_email'), {
            'new_email': 'newemail@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert not EmailChangeToken.objects.filter(user=user).exists()
    
    def test_post_request_same_email(self, client, user):
        """Test que rechaza el mismo email"""
        client.force_login(user)
        
        response = client.post(reverse('solicitar_cambio_email'), {
            'new_email': user.email,
            'password': 'testpass123'
        })
        
        assert response.status_code == 200
        assert 'form' in response.context


@pytest.mark.django_db
class TestConfirmarCambioEmail:
    """Tests para la vista confirmar_cambio_email"""
    
    def test_get_request_with_valid_token(self, client, user):
        """Test que muestra formulario con token válido"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        response = client.get(reverse('confirmar_cambio_email', args=[token.token]))
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'old_email' in response.context
        assert 'new_email' in response.context
    
    def test_get_request_with_invalid_token(self, client):
        """Test que rechaza token inválido"""
        response = client.get(reverse('confirmar_cambio_email', args=['invalid-token']))
        
        assert response.status_code == 302
        assert response.url == reverse('solicitar_cambio_email')
    
    def test_get_request_with_expired_token(self, client, user):
        """Test que rechaza token expirado"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        
        response = client.get(reverse('confirmar_cambio_email', args=[token.token]))
        
        assert response.status_code == 302
        assert response.url == reverse('solicitar_cambio_email')
    
    def test_get_request_with_used_token(self, client, user):
        """Test que rechaza token usado"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        token.used = True
        token.save()
        
        response = client.get(reverse('confirmar_cambio_email', args=[token.token]))
        
        assert response.status_code == 302
        assert response.url == reverse('solicitar_cambio_email')
    
    def test_post_request_valid_token_changes_email(self, client, user):
        """Test que cambia el email con token válido"""
        old_email = user.email
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        response = client.post(reverse('confirmar_cambio_email', args=[token.token]))
        
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.email == 'newemail@example.com'
        assert user.email != old_email
        
        token.refresh_from_db()
        assert token.used == True
    
    def test_post_request_authenticated_user_stays_logged_in(self, client, user):
        """Test que usuario autenticado mantiene sesión después de cambiar email"""
        client.force_login(user)
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        response = client.post(reverse('confirmar_cambio_email', args=[token.token]))
        
        assert response.status_code == 302
        assert response.url == reverse('perfil')
        # Verificar que sigue autenticado
        response = client.get(reverse('perfil'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestCerrarSesionesTodas:
    """Tests para la vista cerrar_sesiones_todas"""
    
    def test_get_request_requires_login(self, client):
        """Test que requiere login"""
        response = client.get(reverse('cerrar_sesiones_todas'))
        
        assert response.status_code == 302  # Redirect to login
    
    def test_get_request_authenticated(self, client, user):
        """Test que usuarios autenticados pueden acceder"""
        client.force_login(user)
        response = client.get(reverse('cerrar_sesiones_todas'))
        
        assert response.status_code == 200
    
    def test_post_request_updates_timestamp(self, client, user):
        """Test que actualiza session_invalidated_at"""
        client.force_login(user)
        
        assert user.perfil.session_invalidated_at is None
        
        response = client.post(reverse('cerrar_sesiones_todas'))
        
        assert response.status_code == 302
        assert response.url == reverse('perfil')
        
        user.perfil.refresh_from_db()
        assert user.perfil.session_invalidated_at is not None
