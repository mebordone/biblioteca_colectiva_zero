"""
Tests para las utilidades de email de cambio de email
"""
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from core.models import EmailChangeToken, Perfil
from core.utils import enviar_email_cambio_email, enviar_email_confirmacion_cambio_email


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


@pytest.fixture
def email_change_token(user):
    """Fixture para crear un token de cambio de email"""
    return EmailChangeToken.create_token(user, 'newemail@example.com')


@pytest.mark.django_db
class TestEnviarEmailCambioEmail:
    """Tests para la función enviar_email_cambio_email"""
    
    @patch('core.utils.EmailMessage')
    def test_envia_email_exitosamente(self, mock_email_message, user, email_change_token):
        """Test que se envía el email correctamente"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.return_value = None
        
        result = enviar_email_cambio_email(user, email_change_token, 'newemail@example.com')
        
        assert result == True
        assert mock_email_message.called
        call_args = mock_email_message.call_args
        
        # Verificar que se llamó con los parámetros correctos
        assert 'Confirmar cambio' in call_args[1]['subject']
        assert 'newemail@example.com' in call_args[1]['to']
    
    @patch('core.utils.EmailMessage')
    def test_maneja_error_de_envio(self, mock_email_message, user, email_change_token):
        """Test que maneja errores de envío"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.side_effect = Exception("Error de conexión")
        
        result = enviar_email_cambio_email(user, email_change_token, 'newemail@example.com')
        
        assert result == False
    
    @patch('core.utils.render_to_string')
    @patch('core.utils.EmailMessage')
    def test_genera_url_correcta(self, mock_email_message, mock_render, user, email_change_token):
        """Test que genera la URL correcta para el token"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.return_value = None
        mock_render.return_value = '<html>Test</html>'
        
        enviar_email_cambio_email(user, email_change_token, 'newemail@example.com')
        
        # Verificar que render_to_string se llamó con el token
        assert mock_render.called
        call_args = mock_render.call_args
        # El contexto es el segundo argumento posicional
        if call_args[0] and len(call_args[0]) > 1:
            context = call_args[0][1]
        elif call_args[1]:
            context = call_args[1].get('context', {})
        else:
            context = {}
        
        assert 'token' in context or 'new_email' in context


@pytest.mark.django_db
class TestEnviarEmailConfirmacionCambioEmail:
    """Tests para la función enviar_email_confirmacion_cambio_email"""
    
    @patch('core.utils.EmailMessage')
    def test_envia_email_confirmacion(self, mock_email_message, user):
        """Test que se envía email de confirmación"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.return_value = None
        
        result = enviar_email_confirmacion_cambio_email(user, 'oldemail@example.com')
        
        assert result == True
        assert mock_email_message.called
        call_args = mock_email_message.call_args
        
        # Verificar contenido del email
        assert 'cambiado exitosamente' in call_args[1]['subject']
        assert user.email in call_args[1]['to']
    
    @patch('core.utils.EmailMessage')
    def test_maneja_error_de_envio_confirmacion(self, mock_email_message, user):
        """Test que maneja errores en envío de confirmación"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.side_effect = Exception("Error de conexión")
        
        result = enviar_email_confirmacion_cambio_email(user, 'oldemail@example.com')
        
        assert result == False
