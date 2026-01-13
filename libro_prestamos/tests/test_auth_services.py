"""
Tests para los servicios de autenticación (auth_services.py).
"""
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import PasswordResetToken, EmailChangeToken, Perfil
from core.auth_services import (
    solicitar_cambio_password_service,
    confirmar_cambio_password_service,
    cambiar_password_desde_perfil_service,
    solicitar_cambio_email_service,
    confirmar_cambio_email_service
)


class TestSolicitarCambioPasswordService:
    """Tests para solicitar_cambio_password_service"""
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_cambio_password')
    def test_exitoso_con_usuario(self, mock_enviar_email, user):
        """Test caso exitoso con usuario autenticado"""
        mock_enviar_email.return_value = True
        
        token, error = solicitar_cambio_password_service(user=user)
        
        assert token is not None
        assert error is None
        assert isinstance(token, PasswordResetToken)
        mock_enviar_email.assert_called_once()
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_cambio_password')
    def test_exitoso_con_email(self, mock_enviar_email, user):
        """Test caso exitoso con email"""
        mock_enviar_email.return_value = True
        
        token, error = solicitar_cambio_password_service(email=user.email)
        
        assert token is not None
        assert error is None
        mock_enviar_email.assert_called_once()
    
    @pytest.mark.django_db
    def test_usuario_no_existe(self):
        """Test cuando el usuario no existe"""
        token, error = solicitar_cambio_password_service(email='nonexistent@example.com')
        
        # Por seguridad, no revelamos si el email existe
        assert token is None
        assert error is None
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_cambio_password')
    def test_error_envio_email(self, mock_enviar_email, user):
        """Test cuando hay error al enviar email"""
        mock_enviar_email.return_value = False
        
        token, error = solicitar_cambio_password_service(user=user)
        
        assert token is None
        assert error == "Error al enviar email"
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_cambio_password')
    def test_excepcion_envio_email_debug(self, mock_enviar_email, user, settings):
        """Test cuando hay excepción al enviar email en modo DEBUG"""
        settings.DEBUG = True
        mock_enviar_email.side_effect = Exception("Error de conexión")
        
        token, error = solicitar_cambio_password_service(user=user)
        
        assert token is None
        assert isinstance(error, dict)
        assert 'error_type' in error
        assert 'error_message' in error


class TestConfirmarCambioPasswordService:
    """Tests para confirmar_cambio_password_service"""
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_confirmacion_cambio')
    def test_exitoso(self, mock_enviar_email, password_reset_token):
        """Test caso exitoso"""
        mock_enviar_email.return_value = True
        new_password = 'NewSecurePass123!'
        
        user, error = confirmar_cambio_password_service(
            password_reset_token.token,
            new_password
        )
        
        assert user is not None
        assert error is None
        assert user.check_password(new_password)
        # Verificar que el token fue marcado como usado
        password_reset_token.refresh_from_db()
        assert password_reset_token.used is True
    
    @pytest.mark.django_db
    def test_token_invalido(self):
        """Test con token inválido"""
        user, error = confirmar_cambio_password_service(
            'invalid-token-12345',
            'NewPassword123!'
        )
        
        assert user is None
        assert 'inválido' in error.lower() or 'expirado' in error.lower()
    
    @pytest.mark.django_db
    def test_token_expirado(self, expired_token):
        """Test con token expirado"""
        user, error = confirmar_cambio_password_service(
            expired_token.token,
            'NewPassword123!'
        )
        
        assert user is None
        assert 'expirado' in error.lower() or 'utilizado' in error.lower()
    
    @pytest.mark.django_db
    def test_token_usado(self, used_token):
        """Test con token ya usado"""
        user, error = confirmar_cambio_password_service(
            used_token.token,
            'NewPassword123!'
        )
        
        assert user is None
        assert 'expirado' in error.lower() or 'utilizado' in error.lower()


class TestCambiarPasswordDesdePerfilService:
    """Tests para cambiar_password_desde_perfil_service"""
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_confirmacion_cambio')
    def test_exitoso(self, mock_enviar_email, user):
        """Test caso exitoso"""
        mock_enviar_email.return_value = True
        old_password = 'testpass123'
        new_password = 'NewSecurePass123!'
        
        # Asegurar que el usuario tiene la contraseña correcta
        user.set_password(old_password)
        user.save()
        
        result_user, error = cambiar_password_desde_perfil_service(
            user,
            old_password,
            new_password
        )
        
        assert result_user is not None
        assert error is None
        assert result_user.check_password(new_password)
        mock_enviar_email.assert_called_once()
    
    @pytest.mark.django_db
    def test_contraseña_actual_incorrecta(self, user):
        """Test cuando la contraseña actual es incorrecta"""
        user.set_password('correct_password')
        user.save()
        
        result_user, error = cambiar_password_desde_perfil_service(
            user,
            'wrong_password',
            'NewPassword123!'
        )
        
        assert result_user is None
        assert 'incorrecta' in error.lower()


class TestSolicitarCambioEmailService:
    """Tests para solicitar_cambio_email_service"""
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_cambio_email')
    def test_exitoso(self, mock_enviar_email, user):
        """Test caso exitoso"""
        mock_enviar_email.return_value = True
        new_email = 'newemail@example.com'
        password = 'testpass123'
        
        user.set_password(password)
        user.save()
        
        token, error = solicitar_cambio_email_service(
            user,
            new_email,
            password
        )
        
        assert token is not None
        assert error is None
        assert isinstance(token, EmailChangeToken)
        assert token.new_email == new_email
        mock_enviar_email.assert_called_once()
    
    @pytest.mark.django_db
    def test_contraseña_incorrecta(self, user):
        """Test cuando la contraseña es incorrecta"""
        user.set_password('correct_password')
        user.save()
        
        token, error = solicitar_cambio_email_service(
            user,
            'newemail@example.com',
            'wrong_password'
        )
        
        assert token is None
        assert 'incorrecta' in error.lower()
    
    @pytest.mark.django_db
    def test_email_ya_en_uso(self, user, another_user):
        """Test cuando el nuevo email ya está en uso"""
        user.set_password('testpass123')
        user.save()
        
        token, error = solicitar_cambio_email_service(
            user,
            another_user.email,  # Email ya en uso
            'testpass123'
        )
        
        assert token is None
        assert 'en uso' in error.lower()


class TestConfirmarCambioEmailService:
    """Tests para confirmar_cambio_email_service"""
    
    @pytest.mark.django_db
    @patch('core.auth_services.enviar_email_confirmacion_cambio_email')
    def test_exitoso(self, mock_enviar_email, user):
        """Test caso exitoso"""
        mock_enviar_email.return_value = True
        old_email = user.email
        new_email = 'newemail@example.com'
        
        # Crear token
        token = EmailChangeToken.create_token(user, new_email)
        
        result_user, result_old_email, result_new_email, error = confirmar_cambio_email_service(
            token.token
        )
        
        assert result_user is not None
        assert error is None
        assert result_old_email == old_email
        assert result_new_email == new_email
        assert result_user.email == new_email
        # Verificar que el token fue marcado como usado
        token.refresh_from_db()
        assert token.used is True
        mock_enviar_email.assert_called_once()
    
    @pytest.mark.django_db
    def test_token_invalido(self):
        """Test con token inválido"""
        user, old_email, new_email, error = confirmar_cambio_email_service(
            'invalid-token-12345'
        )
        
        assert user is None
        assert 'inválido' in error.lower() or 'expirado' in error.lower()
    
    @pytest.mark.django_db
    def test_email_ya_en_uso(self, user, another_user):
        """Test cuando el nuevo email ya está en uso por otro usuario"""
        new_email = another_user.email  # Email ya en uso
        
        token = EmailChangeToken.create_token(user, new_email)
        
        result_user, old_email, new_email_result, error = confirmar_cambio_email_service(
            token.token
        )
        
        assert result_user is None
        assert 'en uso' in error.lower()
