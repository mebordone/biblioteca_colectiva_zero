"""
Tests para los modelos relacionados con cambio de contraseña
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from usuarios.models import PasswordResetToken
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPasswordResetToken:
    """Tests para el modelo PasswordResetToken"""
    
    def test_create_token(self, user):
        """Test que se puede crear un token"""
        token = PasswordResetToken.create_token(user)
        
        assert token is not None
        assert token.user == user
        assert len(token.token) > 0
        assert token.used == False
        assert token.expires_at > timezone.now()
        assert token.expires_at <= timezone.now() + timedelta(hours=24, minutes=1)
    
    def test_token_is_unique(self, user):
        """Test que cada token generado es único"""
        token1 = PasswordResetToken.create_token(user)
        token2 = PasswordResetToken.create_token(user)
        
        assert token1.token != token2.token
    
    def test_token_length(self, user):
        """Test que el token tiene la longitud correcta"""
        token = PasswordResetToken.create_token(user)
        # token_urlsafe(32) genera aproximadamente 43 caracteres
        assert len(token.token) >= 32
    
    def test_is_valid_fresh_token(self, user):
        """Test que un token fresco es válido"""
        token = PasswordResetToken.create_token(user)
        assert token.is_valid() == True
    
    def test_is_valid_expired_token(self, expired_token):
        """Test que un token expirado no es válido"""
        assert expired_token.is_valid() == False
    
    def test_is_valid_used_token(self, used_token):
        """Test que un token usado no es válido"""
        assert used_token.is_valid() == False
    
    def test_mark_as_used(self, password_reset_token):
        """Test que se puede marcar un token como usado"""
        assert password_reset_token.used == False
        password_reset_token.mark_as_used()
        assert password_reset_token.used == True
    
    def test_create_token_invalidates_previous(self, user):
        """Test que crear un nuevo token invalida los anteriores no usados"""
        token1 = PasswordResetToken.create_token(user)
        token2 = PasswordResetToken.create_token(user)
        
        # Refrescar desde BD
        token1.refresh_from_db()
        
        # El primer token debería estar marcado como usado
        assert token1.used == True
        # El segundo token debería estar activo
        assert token2.used == False
        assert token2.is_valid() == True
    
    def test_token_expires_in_24_hours(self, user):
        """Test que el token expira en 24 horas"""
        token = PasswordResetToken.create_token(user)
        expected_expiry = timezone.now() + timedelta(hours=24)
        
        # Permitir diferencia de 1 minuto por tiempo de ejecución
        time_diff = abs((token.expires_at - expected_expiry).total_seconds())
        assert time_diff < 60
    
    def test_str_representation(self, password_reset_token):
        """Test la representación en string del token"""
        str_repr = str(password_reset_token)
        assert 'testuser' in str_repr
        assert 'Activo' in str_repr or 'Usado' in str_repr
