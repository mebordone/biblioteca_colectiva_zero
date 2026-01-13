"""
Servicios para la lógica de negocio de autenticación.
Separa la lógica de negocio de las vistas según AGENT.md.
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
import traceback
import logging
from .models import PasswordResetToken, EmailChangeToken
from .utils import (
    enviar_email_cambio_password,
    enviar_email_confirmacion_cambio,
    enviar_email_cambio_email,
    enviar_email_confirmacion_cambio_email
)

logger = logging.getLogger(__name__)


def solicitar_cambio_password_service(user=None, email=None):
    """
    Servicio para solicitar cambio de contraseña.
    Crea un token y envía email con enlace para cambiar contraseña.
    
    Args:
        user: Usuario autenticado (opcional)
        email: Email del usuario si no está autenticado (opcional)
        
    Returns:
        tuple: (token, None) si es exitoso, (None, error_message) si hay error
        tuple: (None, debug_info) si hay error en modo DEBUG (para mostrar debug)
    """
    # Si no hay usuario, buscar por email
    if not user and email:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Por seguridad, no revelamos si el email existe
            return None, None  # Retornar None, None indica que se debe mostrar mensaje genérico
    
    if not user:
        return None, "Usuario no encontrado"
    
    # Crear token
    try:
        token = PasswordResetToken.create_token(user)
    except Exception as e:
        logger.error(f"Error al crear token de cambio de contraseña: {e}")
        return None, "Error al crear token de cambio de contraseña"
    
    # Enviar email
    try:
        if enviar_email_cambio_password(user, token):
            return token, None
        else:
            return None, "Error al enviar email"
    except Exception as e:
        logger.error(f"Error al enviar email en servicio: {e}")
        logger.error(traceback.format_exc())
        
        # En modo DEBUG, retornar información de debug
        if settings.DEBUG:
            debug_info = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traceback': traceback.format_exc(),
                'user_email': user.email if user else 'N/A',
                'subject': 'Cambio de contrasena - Biblioteca Colectiva',
                'from_email': settings.DEFAULT_FROM_EMAIL,
                'to_email': user.email if user else 'N/A',
            }
            return None, debug_info
        else:
            return None, "Error al enviar email"


def confirmar_cambio_password_service(token_value, new_password):
    """
    Servicio para confirmar y cambiar la contraseña usando el token.
    
    Args:
        token_value: Valor del token de cambio de contraseña
        new_password: Nueva contraseña
        
    Returns:
        tuple: (user, None) si es exitoso, (None, error_message) si hay error
    """
    try:
        reset_token = PasswordResetToken.objects.get(token=token_value)
    except PasswordResetToken.DoesNotExist:
        return None, "El enlace de cambio de contraseña es inválido o ha expirado"
    
    # Validar token
    if not reset_token.is_valid():
        return None, "El enlace de cambio de contraseña ha expirado o ya fue utilizado"
    
    # Cambiar contraseña
    try:
        reset_token.user.set_password(new_password)
        reset_token.user.save()
        
        # Marcar token como usado
        reset_token.mark_as_used()
        
        # Enviar email de confirmación
        enviar_email_confirmacion_cambio(reset_token.user)
        
        return reset_token.user, None
    except Exception as e:
        logger.error(f"Error al cambiar contraseña: {e}")
        logger.error(traceback.format_exc())
        return None, "Error al cambiar contraseña"


def cambiar_password_desde_perfil_service(user, old_password, new_password):
    """
    Servicio para cambiar contraseña desde el perfil (requiere contraseña actual).
    
    Args:
        user: Usuario que quiere cambiar la contraseña
        old_password: Contraseña actual (para validación)
        new_password: Nueva contraseña
        
    Returns:
        tuple: (user, None) si es exitoso, (None, error_message) si hay error
    """
    # Validar contraseña actual
    if not user.check_password(old_password):
        return None, "La contraseña actual es incorrecta"
    
    # Cambiar contraseña
    try:
        user.set_password(new_password)
        user.save()
        
        # Enviar email de confirmación
        enviar_email_confirmacion_cambio(user)
        
        return user, None
    except Exception as e:
        logger.error(f"Error al cambiar contraseña desde perfil: {e}")
        logger.error(traceback.format_exc())
        return None, "Error al cambiar contraseña"


def solicitar_cambio_email_service(user, new_email, password):
    """
    Servicio para solicitar cambio de email.
    Valida contraseña actual y crea token para confirmación.
    
    Args:
        user: Usuario que solicita el cambio
        new_email: Nuevo email
        password: Contraseña actual (para validación)
        
    Returns:
        tuple: (token, None) si es exitoso, (None, error_message) si hay error
    """
    # Validar contraseña actual
    if not user.check_password(password):
        return None, "La contraseña es incorrecta"
    
    # Validar que el nuevo email no esté en uso
    if User.objects.filter(email=new_email).exclude(id=user.id).exists():
        return None, "Este correo electrónico ya está en uso"
    
    # Crear token
    try:
        token = EmailChangeToken.create_token(user, new_email)
    except Exception as e:
        logger.error(f"Error al crear token de cambio de email: {e}")
        return None, "Error al crear token de cambio de email"
    
    # Enviar email con enlace de confirmación
    try:
        if enviar_email_cambio_email(user, token, new_email):
            return token, None
        else:
            return None, "Error al enviar email"
    except Exception as e:
        logger.error(f"Error al enviar email de cambio de email: {e}")
        logger.error(traceback.format_exc())
        return None, "Error al enviar email"


def confirmar_cambio_email_service(token_value):
    """
    Servicio para confirmar y cambiar el email usando el token.
    
    Args:
        token_value: Valor del token de cambio de email
        
    Returns:
        tuple: (user, old_email, new_email, None) si es exitoso, (None, None, None, error_message) si hay error
    """
    try:
        email_token = EmailChangeToken.objects.get(token=token_value)
    except EmailChangeToken.DoesNotExist:
        return None, None, None, "El enlace de cambio de correo electrónico es inválido o ha expirado"
    
    # Validar token
    if not email_token.is_valid():
        return None, None, None, "El enlace de cambio de correo electrónico ha expirado o ya fue utilizado"
    
    user = email_token.user
    old_email = user.email
    new_email = email_token.new_email
    
    # Validar que el nuevo email no esté en uso por otro usuario
    if User.objects.filter(email=new_email).exclude(id=user.id).exists():
        return None, None, None, "Este correo electrónico ya está en uso"
    
    # Cambiar el email
    try:
        user.email = new_email
        user.save()
        
        # Marcar token como usado
        email_token.used = True
        email_token.save()
        
        # Enviar email de confirmación al nuevo email
        enviar_email_confirmacion_cambio_email(user, old_email)
        
        return user, old_email, new_email, None
    except Exception as e:
        logger.error(f"Error al cambiar email: {e}")
        logger.error(traceback.format_exc())
        return None, None, None, "Error al cambiar email"
