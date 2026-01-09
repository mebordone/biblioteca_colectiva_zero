"""
Backend de email personalizado para desarrollo que maneja UTF-8 correctamente
"""
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.core.mail.message import EmailMessage
import sys
import traceback
import logging
import io
import re

logger = logging.getLogger(__name__)


class UTF8ConsoleEmailBackend(ConsoleEmailBackend):
    """
    Backend de consola que maneja correctamente caracteres UTF-8
    """
    def write_message(self, message):
        """
        Escribe el mensaje a stdout con encoding UTF-8 de forma segura
        """
        try:
            logger.debug("UTF8ConsoleEmailBackend: Iniciando write_message")
            logger.debug(f"Encoding actual de stdout: {getattr(sys.stdout, 'encoding', 'N/A')}")
            logger.debug(f"Subject: {repr(message.subject)}")
            logger.debug(f"From: {repr(message.from_email)}")
            logger.debug(f"To: {repr(message.to)}")
            
            # Asegurar que stdout use UTF-8
            if hasattr(sys.stdout, 'reconfigure'):
                try:
                    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
                    logger.debug("stdout reconfigurado a UTF-8")
                except Exception as e:
                    logger.warning(f"No se pudo reconfigurar stdout: {e}")
            
            # Escribir el email manualmente con manejo seguro de UTF-8
            self._write_email_safe(message)
            logger.debug("Mensaje escrito exitosamente")
            
        except Exception as e:
            logger.error(f"Error en write_message: {e}")
            logger.error(f"Tipo: {type(e).__name__}")
            logger.error(traceback.format_exc())
            # Intentar mostrar información básica
            self._write_email_fallback(message)
            raise
    
    def _write_email_safe(self, message):
        """Escribe el email de forma segura manejando UTF-8"""
        def safe_write(text):
            """Escribe texto de forma segura"""
            try:
                sys.stdout.write(text)
            except UnicodeEncodeError:
                # Si falla, usar replace
                safe_text = text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                sys.stdout.write(safe_text)
        
        safe_write("\n" + "="*70 + "\n")
        safe_write("EMAIL (desde UTF8ConsoleEmailBackend)\n")
        safe_write("="*70 + "\n")
        safe_write(f"Content-Type: {message.content_subtype or 'text/plain'}; charset=utf-8\n")
        safe_write(f"MIME-Version: 1.0\n")
        safe_write(f"Subject: {message.subject}\n")
        safe_write(f"From: {message.from_email}\n")
        safe_write(f"To: {', '.join(message.to)}\n")
        safe_write(f"Date: {message.date}\n" if hasattr(message, 'date') and message.date else "")
        safe_write("\n")
        
        # Escribir el body
        if hasattr(message, 'body'):
            safe_write(message.body)
        
        # Escribir alternatives si existen
        if hasattr(message, 'alternatives') and message.alternatives:
            safe_write("\n" + "-"*70 + "\n")
            safe_write("ALTERNATIVE CONTENT:\n")
            safe_write("-"*70 + "\n")
            for content, mimetype in message.alternatives:
                safe_write(f"\n[{mimetype}]\n")
                safe_write(str(content))
        
        safe_write("\n" + "="*70 + "\n\n")
        sys.stdout.flush()
    
    def _write_email_fallback(self, message):
        """Escribe información básica del email cuando hay error"""
        try:
            print("\n" + "="*70, file=sys.stderr)
            print("EMAIL (versión simplificada - error de codificación)", file=sys.stderr)
            print("="*70, file=sys.stderr)
            print(f"From: {message.from_email}", file=sys.stderr)
            print(f"To: {', '.join(message.to)}", file=sys.stderr)
            # Subject sin caracteres especiales
            safe_subject = message.subject.encode('ascii', errors='replace').decode('ascii')
            print(f"Subject: {safe_subject}", file=sys.stderr)
            print(f"Body length: {len(message.body)} caracteres", file=sys.stderr)
            
            # Intentar extraer el enlace del body
            if hasattr(message, 'body') and message.body:
                url_match = re.search(r'http://[^\s<>"\']+', message.body)
                if url_match:
                    print(f"\nENLACE DE RESET (copia esto):", file=sys.stderr)
                    print(url_match.group(), file=sys.stderr)
            
            print("="*70 + "\n", file=sys.stderr)
        except Exception as e2:
            logger.error(f"Error incluso en fallback: {e2}")
