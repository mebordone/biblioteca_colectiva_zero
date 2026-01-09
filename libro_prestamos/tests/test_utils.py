"""
Tests para las utilidades de email
"""
import pytest
from unittest.mock import patch, MagicMock
from django.core.mail import send_mail
from django.contrib.auth.models import User
from core.models import PasswordResetToken
from core.utils import enviar_email_cambio_password, enviar_email_confirmacion_cambio


@pytest.mark.django_db
class TestEnviarEmailCambioPassword:
    """Tests para la función enviar_email_cambio_password"""
    
    @patch('core.utils.EmailMessage')
    def test_envia_email_exitosamente(self, mock_email_message, user, password_reset_token):
        """Test que se envía el email correctamente"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.return_value = None
        
        result = enviar_email_cambio_password(user, password_reset_token)
        
        assert result == True
        assert mock_email_message.called
        call_args = mock_email_message.call_args
        
        # Verificar que se llamó con los parámetros correctos
        assert 'Cambio de contrasena' in call_args[1]['subject']
        assert user.email in call_args[1]['to']
        assert mock_email_instance.send.called
    
    @patch('core.utils.EmailMessage')
    def test_maneja_error_de_envio(self, mock_email_message, user, password_reset_token):
        """Test que maneja errores de envío"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.side_effect = Exception("Error de conexión")
        
        result = enviar_email_cambio_password(user, password_reset_token)
        
        assert result == False
    
    @patch('core.utils.render_to_string')
    @patch('core.utils.send_mail')
    def test_genera_url_correcta(self, mock_send_mail, mock_render, user, password_reset_token):
        """Test que genera la URL correcta para el token"""
        mock_send_mail.return_value = True
        mock_render.return_value = '<html>Test</html>'
        
        enviar_email_cambio_password(user, password_reset_token)
        
        # Verificar que render_to_string se llamó con el token
        assert mock_render.called
        # render_to_string(template_name, context_dict)
        # call_args es una tupla: (args, kwargs)
        call_args = mock_render.call_args
        # El contexto es el segundo argumento posicional
        if call_args[0] and len(call_args[0]) > 1:
            context = call_args[0][1]
        elif call_args[1]:
            context = call_args[1].get('context', {})
        else:
            context = {}
        
        assert 'token' in context
        assert context['token'] == password_reset_token


@pytest.mark.django_db
class TestEnviarEmailConfirmacionCambio:
    """Tests para la función enviar_email_confirmacion_cambio"""
    
    @patch('core.utils.EmailMessage')
    def test_envia_email_confirmacion(self, mock_email_message, user):
        """Test que se envía email de confirmación"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.return_value = None
        
        result = enviar_email_confirmacion_cambio(user)
        
        assert result == True
        assert mock_email_message.called
        call_args = mock_email_message.call_args
        
        # Verificar contenido del email
        assert 'cambiada exitosamente' in call_args[1]['subject']
        assert user.email in call_args[1]['to']
    
    @patch('core.utils.EmailMessage')
    def test_maneja_error_de_envio_confirmacion(self, mock_email_message, user):
        """Test que maneja errores en envío de confirmación"""
        mock_email_instance = mock_email_message.return_value
        mock_email_instance.send.side_effect = Exception("Error de conexión")
        
        result = enviar_email_confirmacion_cambio(user)
        
        assert result == False
