"""
Middleware para invalidar sesiones basado en timestamp
"""
from django.contrib.auth import logout
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class SessionInvalidationMiddleware:
    """
    Middleware que verifica si la sesión del usuario debe ser invalidada
    basándose en el campo session_invalidated_at del perfil.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Solo verificar si el usuario está autenticado
        if request.user.is_authenticated:
            try:
                perfil = request.user.perfil
                
                # Si hay un timestamp de invalidación
                if perfil.session_invalidated_at:
                    # Obtener la fecha de creación de la sesión actual
                    session_key = request.session.session_key
                    if session_key:
                        # Django guarda la fecha de creación en request.session
                        # Si la sesión fue creada antes del timestamp de invalidación, cerrar sesión
                        # Nota: Django no guarda directamente la fecha de creación de la sesión
                        # en la sesión misma, así que usamos una aproximación:
                        # Si el timestamp de invalidación es más reciente que "ahora menos un tiempo razonable",
                        # asumimos que la sesión debe ser invalidada
                        # Una mejor aproximación es verificar si la sesión existe en la base de datos
                        # y comparar su fecha de creación
                        
                        # Intentar obtener la sesión de la base de datos si está configurada
                        try:
                            from django.contrib.sessions.models import Session
                            session = Session.objects.get(session_key=session_key)
                            # Si la sesión fue creada antes del timestamp de invalidación
                            if session.expire_date and perfil.session_invalidated_at:
                                # Comparar fechas (expire_date es cuando expira, pero podemos usar created)
                                # Django no guarda created directamente, así que usamos expire_date - SESSION_COOKIE_AGE
                                from django.conf import settings
                                from datetime import timedelta
                                session_age = getattr(settings, 'SESSION_COOKIE_AGE', 1209600)  # 2 semanas por defecto
                                # Estimar fecha de creación
                                estimated_created = session.expire_date - timedelta(seconds=session_age)
                                
                                if estimated_created < perfil.session_invalidated_at:
                                    logger.info(f"Invalidando sesión {session_key} para usuario {request.user.username}")
                                    logout(request)
                                    return self.get_response(request)
                        except Exception as e:
                            # Si no podemos acceder a la sesión de la BD, usar método alternativo
                            logger.debug(f"No se pudo verificar sesión en BD: {e}")
                            # Método alternativo: invalidar si el timestamp es muy reciente (últimos 5 minutos)
                            # Esto es menos preciso pero funciona sin acceso a la BD de sesiones
                            time_diff = timezone.now() - perfil.session_invalidated_at
                            if time_diff.total_seconds() < 300:  # 5 minutos
                                logger.info(f"Invalidando sesión para usuario {request.user.username} (método alternativo)")
                                logout(request)
                                return self.get_response(request)
            except Exception as e:
                logger.error(f"Error en SessionInvalidationMiddleware: {e}")
        
        response = self.get_response(request)
        return response
