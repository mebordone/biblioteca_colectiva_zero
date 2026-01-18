"""
Utilidades para envío de emails relacionados con usuarios.
"""
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import traceback
import logging

logger = logging.getLogger(__name__)


def enviar_email_cambio_password(user, token):
    """
    Envía un email con el enlace para cambiar la contraseña.
    
    Args:
        user: Usuario que solicita el cambio
        token: Token de PasswordResetToken
    """
    try:
        logger.debug(f"Iniciando envío de email para usuario: {user.email}")
        # Construir URL de confirmación
        
        # Obtener el dominio actual
        if settings.DEBUG:
            # En desarrollo, siempre usar 127.0.0.1:8000
            domain = '127.0.0.1:8000'
        elif settings.ALLOWED_HOSTS:
            domain = settings.ALLOWED_HOSTS[0]
        else:
            domain = '127.0.0.1:8000'
        
        # Construir URL completa
        protocol = 'https' if not settings.DEBUG else 'http'
        if not domain.startswith('http'):
            base_url = f"{protocol}://{domain}"
        else:
            base_url = domain
        
        reset_path = reverse('confirmar_cambio_password', args=[token.token])
        reset_url = f"{base_url}{reset_path}"
        
        # Renderizar template de email
        logger.debug("Renderizando template de email")
        # Usar subject sin caracteres especiales para evitar problemas con SMTP
        # En desarrollo con consola no importa, pero es buena práctica
        subject = 'Cambio de contrasena - Biblioteca Colectiva'
        try:
            html_message = render_to_string('emails/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
                'token': token,
            })
            logger.debug(f"Template renderizado exitosamente. Longitud HTML: {len(html_message)}")
        except Exception as e:
            logger.error(f"Error al renderizar template: {e}")
            logger.error(traceback.format_exc())
            raise
        
        # Versión texto plano (opcional, para clientes que no soportan HTML)
        logger.debug("Creando mensaje de texto plano")
        plain_message = f"""
Hola {user.get_full_name() or user.username},

Has solicitado cambiar tu contraseña en Biblioteca Colectiva.

Para completar el cambio, haz clic en el siguiente enlace:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email. Tu contraseña no será modificada.

Saludos,
Equipo de Biblioteca Colectiva
"""
        
        # Usar EmailMessage para mejor manejo de UTF-8
        logger.debug(f"Creando EmailMessage. Subject: {subject[:50]}...")
        logger.debug(f"From: {settings.DEFAULT_FROM_EMAIL}, To: {user.email}")
        logger.debug(f"Encoding configurado: UTF-8")
        
        try:
            # Asegurar que el subject esté en UTF-8
            if isinstance(subject, str):
                subject = subject.encode('utf-8').decode('utf-8')
            
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"
            email.encoding = 'utf-8'
            
            # Agregar versión texto plano como alternativa
            email.alternatives = [(plain_message, 'text/plain')]
            
            logger.debug("Enviando email...")
            email.send(fail_silently=False)
            logger.debug("Email enviado exitosamente")
            return True
        except UnicodeEncodeError as ue:
            logger.error(f"Error de codificación Unicode: {ue}")
            logger.error(f"Subject: {repr(subject)}")
            logger.error(f"From: {repr(settings.DEFAULT_FROM_EMAIL)}")
            logger.error(f"To: {repr(user.email)}")
            logger.error(traceback.format_exc())
            raise
        except Exception as e:
            logger.error(f"Error al crear/enviar EmailMessage: {e}")
            logger.error(f"Tipo de error: {type(e).__name__}")
            logger.error(traceback.format_exc())
            raise
    except Exception as e:
        # Log detallado del error
        error_msg = f"Error al enviar email de cambio de contraseña: {e}"
        logger.error(error_msg)
        logger.error(f"Tipo de error: {type(e).__name__}")
        logger.error(f"Usuario: {user.email if user else 'N/A'}")
        logger.error(traceback.format_exc())
        
        # También imprimir en consola para desarrollo
        print(f"\n{'='*60}")
        print(f"ERROR DETALLADO AL ENVIAR EMAIL")
        print(f"{'='*60}")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {e}")
        print(f"Usuario: {user.email if user else 'N/A'}")
        print(f"\nTraceback completo:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        return False


def enviar_email_confirmacion_cambio(user):
    """
    Envía un email de confirmación después de cambiar la contraseña exitosamente.
    
    Args:
        user: Usuario que cambió la contraseña
    """
    try:
        subject = 'Contrasena cambiada exitosamente - Biblioteca Colectiva'
        html_message = render_to_string('emails/password_change_confirmation.html', {
            'user': user,
        })
        
        # Versión texto plano
        plain_message = f"""
Hola {user.get_full_name() or user.username},

Tu contraseña ha sido cambiada exitosamente.

Si no realizaste este cambio, por favor contacta al soporte inmediatamente.

Saludos,
Equipo de Biblioteca Colectiva
"""
        
        # Usar EmailMessage para mejor manejo de UTF-8
        # Asegurar que el subject esté en UTF-8
        if isinstance(subject, str):
            subject = subject.encode('utf-8').decode('utf-8')
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = "html"
        email.encoding = 'utf-8'
        
        # Agregar versión texto plano como alternativa
        email.alternatives = [(plain_message, 'text/plain')]
        
        # Enviar email
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error al enviar email de confirmación: {e}")
        return False


def enviar_email_cambio_email(user, token, new_email):
    """
    Envía un email con el enlace para confirmar el cambio de email.
    
    Args:
        user: Usuario que solicita el cambio
        token: Token de EmailChangeToken
        new_email: Nuevo email a confirmar
    """
    try:
        logger.debug(f"Iniciando envío de email de cambio de email para usuario: {user.email}")
        # Construir URL de confirmación
        
        # Obtener el dominio actual
        if settings.DEBUG:
            # En desarrollo, siempre usar 127.0.0.1:8000
            domain = '127.0.0.1:8000'
        elif settings.ALLOWED_HOSTS:
            domain = settings.ALLOWED_HOSTS[0]
        else:
            domain = '127.0.0.1:8000'
        
        # Construir URL completa
        protocol = 'https' if not settings.DEBUG else 'http'
        if not domain.startswith('http'):
            base_url = f"{protocol}://{domain}"
        else:
            base_url = domain
        
        confirm_path = reverse('confirmar_cambio_email', args=[token.token])
        confirm_url = f"{base_url}{confirm_path}"
        
        # Renderizar template de email
        logger.debug("Renderizando template de email de cambio de email")
        subject = 'Confirmar cambio de correo electrónico - Biblioteca Colectiva'
        try:
            html_message = render_to_string('emails/email_change_request.html', {
                'user': user,
                'new_email': new_email,
                'confirm_url': confirm_url,
                'token': token,
            })
            logger.debug(f"Template renderizado exitosamente. Longitud HTML: {len(html_message)}")
        except Exception as e:
            logger.error(f"Error al renderizar template: {e}")
            logger.error(traceback.format_exc())
            raise
        
        # Versión texto plano
        logger.debug("Creando mensaje de texto plano")
        plain_message = f"""
Hola {user.get_full_name() or user.username},

Has solicitado cambiar tu correo electrónico en Biblioteca Colectiva.

Tu correo actual: {user.email}
Nuevo correo: {new_email}

Para completar el cambio, haz clic en el siguiente enlace:
{confirm_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email. Tu correo electrónico no será modificado.

Saludos,
Equipo de Biblioteca Colectiva
"""
        
        # Usar EmailMessage para mejor manejo de UTF-8
        logger.debug(f"Creando EmailMessage. Subject: {subject[:50]}...")
        logger.debug(f"From: {settings.DEFAULT_FROM_EMAIL}, To: {new_email}")
        logger.debug(f"Encoding configurado: UTF-8")
        
        try:
            # Asegurar que el subject esté en UTF-8
            if isinstance(subject, str):
                subject = subject.encode('utf-8').decode('utf-8')
            
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[new_email],  # Enviar al nuevo email
            )
            email.content_subtype = "html"
            email.encoding = 'utf-8'
            
            # Agregar versión texto plano como alternativa
            email.alternatives = [(plain_message, 'text/plain')]
            
            logger.debug("Enviando email...")
            email.send(fail_silently=False)
            logger.debug("Email enviado exitosamente")
            return True
        except UnicodeEncodeError as ue:
            logger.error(f"Error de codificación Unicode: {ue}")
            logger.error(f"Subject: {repr(subject)}")
            logger.error(f"From: {repr(settings.DEFAULT_FROM_EMAIL)}")
            logger.error(f"To: {repr(new_email)}")
            logger.error(traceback.format_exc())
            raise
        except Exception as e:
            logger.error(f"Error al crear/enviar EmailMessage: {e}")
            logger.error(f"Tipo de error: {type(e).__name__}")
            logger.error(traceback.format_exc())
            raise
    except Exception as e:
        # Log detallado del error
        error_msg = f"Error al enviar email de cambio de email: {e}"
        logger.error(error_msg)
        logger.error(f"Tipo de error: {type(e).__name__}")
        logger.error(f"Usuario: {user.email if user else 'N/A'}")
        logger.error(traceback.format_exc())
        
        # También imprimir en consola para desarrollo
        print(f"\n{'='*60}")
        print(f"ERROR DETALLADO AL ENVIAR EMAIL DE CAMBIO DE EMAIL")
        print(f"{'='*60}")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {e}")
        print(f"Usuario: {user.email if user else 'N/A'}")
        print(f"Nuevo email: {new_email if 'new_email' in locals() else 'N/A'}")
        print(f"\nTraceback completo:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        return False


def enviar_email_confirmacion_cambio_email(user, old_email):
    """
    Envía un email de confirmación después de cambiar el email exitosamente.
    
    Args:
        user: Usuario que cambió el email
        old_email: Email anterior del usuario
    """
    try:
        subject = 'Correo electrónico cambiado exitosamente - Biblioteca Colectiva'
        html_message = render_to_string('emails/email_change_confirmation.html', {
            'user': user,
            'old_email': old_email,
        })
        
        # Versión texto plano
        plain_message = f"""
Hola {user.get_full_name() or user.username},

Tu correo electrónico ha sido cambiado exitosamente.

Correo anterior: {old_email}
Correo nuevo: {user.email}

Si no realizaste este cambio, por favor contacta al soporte inmediatamente.

Saludos,
Equipo de Biblioteca Colectiva
"""
        
        # Usar EmailMessage para mejor manejo de UTF-8
        # Asegurar que el subject esté en UTF-8
        if isinstance(subject, str):
            subject = subject.encode('utf-8').decode('utf-8')
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],  # Enviar al nuevo email
        )
        email.content_subtype = "html"
        email.encoding = 'utf-8'
        
        # Agregar versión texto plano como alternativa
        email.alternatives = [(plain_message, 'text/plain')]
        
        # Enviar email
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error al enviar email de confirmación de cambio de email: {e}")
        return False
