"""
Tests para el modelo EmailChangeToken
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from core.models import EmailChangeToken, Perfil


@pytest.fixture
def user(db):
    """Fixture para crear un usuario de prueba"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    # Crear perfil asociado
    Perfil.objects.create(
        usuario=user,
        ciudad='Buenos Aires',
        pais='Argentina'
    )
    return user


@pytest.mark.django_db
class TestEmailChangeToken:
    """Tests para el modelo EmailChangeToken"""
    
    def test_create_token(self, user):
        """Test que se puede crear un token"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        assert token is not None
        assert token.user == user
        assert token.new_email == 'newemail@example.com'
        assert token.token is not None
        assert len(token.token) > 0
        assert token.used == False
        assert token.expires_at > timezone.now()
    
    def test_token_is_unique(self, user):
        """Test que los tokens generados son únicos"""
        token1 = EmailChangeToken.create_token(user, 'email1@example.com')
        token2 = EmailChangeToken.create_token(user, 'email2@example.com')
        
        assert token1.token != token2.token
    
    def test_token_length(self, user):
        """Test que el token tiene la longitud correcta"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        # token_urlsafe(32) genera aproximadamente 43 caracteres
        assert len(token.token) >= 32
    
    def test_is_valid_fresh_token(self, user):
        """Test que un token recién creado es válido"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        assert token.is_valid() == True
    
    def test_is_valid_expired_token(self, user):
        """Test que un token expirado no es válido"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        
        assert token.is_valid() == False
    
    def test_is_valid_used_token(self, user):
        """Test que un token usado no es válido"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        token.used = True
        token.save()
        
        assert token.is_valid() == False
    
    def test_mark_as_used(self, user):
        """Test que se puede marcar un token como usado"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        token.used = True
        token.save()
        
        token.refresh_from_db()
        assert token.used == True
    
    def test_create_token_invalidates_previous(self, user):
        """Test que crear un nuevo token invalida los anteriores"""
        token1 = EmailChangeToken.create_token(user, 'email1@example.com')
        token2 = EmailChangeToken.create_token(user, 'email2@example.com')
        
        token1.refresh_from_db()
        assert token1.used == True
        assert token2.used == False
    
    def test_token_expires_in_24_hours(self, user):
        """Test que el token expira en 24 horas"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        expected_expiry = timezone.now() + timedelta(hours=24)
        # Permitir diferencia de hasta 1 minuto
        time_diff = abs((token.expires_at - expected_expiry).total_seconds())
        assert time_diff < 60
    
    def test_str_representation(self, user):
        """Test la representación en string del token"""
        token = EmailChangeToken.create_token(user, 'newemail@example.com')
        
        str_repr = str(token)
        assert user.username in str_repr
        assert 'newemail@example.com' in str_repr
        assert 'Valid' in str_repr
