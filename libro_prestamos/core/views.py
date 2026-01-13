from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Libro, Prestamo, PasswordResetToken, EmailChangeToken
from .forms import (
    LibroForm, RegistroForm, PerfilForm, CargaMasivaForm,
    PasswordChangeRequestForm, PasswordChangeConfirmForm, PasswordChangeFromProfileForm,
    EmailChangeRequestForm, EmailChangeConfirmForm
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.conf import settings
from .utils import (
    procesar_excel_libros, generar_plantilla_excel,
    enviar_email_cambio_password, enviar_email_confirmacion_cambio,
    enviar_email_cambio_email, enviar_email_confirmacion_cambio_email
)
from .services import crear_prestamo_service, marcar_devuelto_service
import traceback
import logging

logger = logging.getLogger(__name__)

def home(request):
    context = {}
    if request.user.is_authenticated:
        # Estadísticas del usuario
        mis_libros = Libro.objects.filter(propietario=request.user)
        total_libros = mis_libros.count()
        libros_disponibles = mis_libros.filter(estado='disponible').count()
        
        # Préstamos activos (libros que el usuario prestó y aún no se devolvieron)
        prestamos_activos = Prestamo.objects.filter(
            prestador=request.user,
            devuelto=False
        ).count()
        
        # Préstamos recibidos activos (libros que el usuario recibió prestados)
        prestamos_recibidos = Prestamo.objects.filter(
            prestatario=request.user,
            devuelto=False
        ).count()
        
        # Últimos libros agregados (opcional)
        ultimos_libros = mis_libros.order_by('-id')[:5]
        
        context = {
            'total_libros': total_libros,
            'libros_disponibles': libros_disponibles,
            'prestamos_activos': prestamos_activos,
            'prestamos_recibidos': prestamos_recibidos,
            'ultimos_libros': ultimos_libros,
        }
    
    return render(request, 'home.html', context)

# Libros
from django.core.paginator import Paginator
from django.db.models import Q  # Para búsquedas avanzadas

def listar_libros(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    libros = Libro.objects.filter(
        Q(nombre__icontains=query) | Q(autor__icontains=query)
    ) if query else Libro.objects.all()
    
    # Paginación
    paginator = Paginator(libros, 10)  # Mostrar 10 libros por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'libros/lista.html', {
        'libros': page_obj,
        'query': query,
    })

@login_required
def listar_mis_libros(request):
    libros = Libro.objects.filter(propietario=request.user)
    return render(request, 'libros/lista.html', {'libros': libros})


@login_required
def cargar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.propietario = request.user  # Asignar el usuario actual como propietario
            libro.save()
            return redirect('listar_libros')  # Cambia a la vista que prefieras después de guardar
    else:
        form = LibroForm()
    return render(request, 'libros/cargar.html', {'form': form})


def libro_detalle(request, id):
    libro = get_object_or_404(Libro, id=id)
    # Obtener préstamo activo si el libro está prestado
    prestamo_activo = None
    if libro.estado == 'prestado':
        prestamo_activo = Prestamo.objects.filter(
            libro=libro,
            devuelto=False
        ).select_related('prestatario').first()
    
    return render(request, 'libros/libro_detalle.html', {
        'libro': libro,
        'prestamo_activo': prestamo_activo
    })

@login_required
def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.user != libro.propietario:
        return HttpResponseForbidden("No tienes permiso para editar este libro.")
    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libro_detalle', id=libro.id)
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/editar_libro.html', {'form': form, 'libro': libro})

@login_required
def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.user != libro.propietario:
        return HttpResponseForbidden("No tienes permiso para eliminar este libro.")
    if request.method == "POST":
        libro.delete()
        return redirect('listar_libros')
    return render(request, 'libros/eliminar_libro.html', {'libro': libro})

## Prestamos

@login_required
def crear_prestamo(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        prestatario_id = request.POST.get('prestatario')

        # Usar servicio para crear préstamo
        prestamo, error = crear_prestamo_service(libro_id, prestatario_id, request.user)
        
        if prestamo:
            messages.success(request, f"El libro '{prestamo.libro.nombre}' ha sido prestado exitosamente.")
            return redirect('listar_prestamos')
        else:
            messages.error(request, error or "Error al crear el préstamo.")

    # Filtrar libros disponibles del usuario actual
    libros = Libro.objects.filter(propietario=request.user, estado='disponible')
    # Excluir al usuario actual de la lista de usuarios
    usuarios = User.objects.exclude(id=request.user.id)

    return render(request, 'prestamos/crear.html', {'libros': libros, 'usuarios': usuarios})

@login_required
def listar_prestamos(request):
    # Préstamos realizados (libros que yo presté)
    prestamos_realizados = Prestamo.objects.filter(
        prestador=request.user,
        devuelto=False
    ).select_related('libro', 'prestatario')
    
    # Préstamos recibidos (libros que recibí prestados)
    prestamos_recibidos = Prestamo.objects.filter(
        prestatario=request.user,
        devuelto=False
    ).select_related('libro', 'prestador')
    
    return render(request, 'prestamos/listar_prestamos.html', {
        'prestamos_realizados': prestamos_realizados,
        'prestamos_recibidos': prestamos_recibidos,
    })

@login_required
def historial_prestamos(request):
    # Historial de préstamos realizados (todos, incluyendo devueltos)
    historial_realizados = Prestamo.objects.filter(
        prestador=request.user
    ).select_related('libro', 'prestatario').order_by('-fecha_prestamo')
    
    # Historial de préstamos recibidos (todos, incluyendo devueltos)
    historial_recibidos = Prestamo.objects.filter(
        prestatario=request.user
    ).select_related('libro', 'prestador').order_by('-fecha_prestamo')
    
    return render(request, 'prestamos/historial_prestamos.html', {
        'historial_realizados': historial_realizados,
        'historial_recibidos': historial_recibidos,
    })

@login_required
def marcar_devuelto(request, prestamo_id):
    # Usar servicio para marcar préstamo como devuelto
    prestamo, error = marcar_devuelto_service(prestamo_id, request.user)
    
    if prestamo:
        if error:
            messages.warning(request, error)
        else:
            messages.success(request, f"El libro '{prestamo.libro.nombre}' ha sido marcado como devuelto.")
    else:
        messages.error(request, error or "Error al marcar el préstamo como devuelto.")
        return redirect('listar_prestamos')

    return redirect('listar_prestamos')

## Usuarios

def registro_orig(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = RegistroForm()
    return render(request, 'users/registro.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            # Guardar el usuario
            usuario = user_form.save()
            
            # Crear el perfil asociado
            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario  # Asocia el perfil al usuario
            perfil.save()
            
            return redirect('login')  # Redirige a la página de login después del registro
    else:
        user_form = RegistroForm()
        perfil_form = PerfilForm()

    return render(request, 'users/registro.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
    })

# core/views.py
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio o dashboard
        else:
            # Error de login
            return render(request, 'users/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'users/login.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('home')

@login_required
def perfil(request):
    # Obtiene el perfil del usuario actual
    perfil = request.user.perfil

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al mismo perfil tras guardar los cambios
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'users/perfil.html', {'form': form})

## Carga Masiva

@login_required
def cargar_libros_masivo(request):
    """
    Vista para cargar múltiples libros desde un archivo Excel.
    """
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_excel']
            
            # Procesar el archivo Excel
            resultados = procesar_excel_libros(archivo, request.user)
            
            # Mostrar mensajes según resultados
            if resultados['libros_creados']:
                mensaje = f"Se crearon {len(resultados['libros_creados'])} libro(s) exitosamente."
                messages.success(request, mensaje)
            
            if resultados['duplicados']:
                mensaje = f"Se encontraron {len(resultados['duplicados'])} libro(s) duplicado(s) que no se crearon."
                messages.warning(request, mensaje)
            
            if resultados['errores']:
                mensaje = f"Se encontraron {len(resultados['errores'])} error(es) en el archivo."
                messages.error(request, mensaje)
            
            # Renderizar con resultados
            return render(request, 'libros/cargar_masivo.html', {
                'form': CargaMasivaForm(),
                'resultados': resultados,
                'mostrar_resultados': True
            })
    else:
        form = CargaMasivaForm()
    
    return render(request, 'libros/cargar_masivo.html', {
        'form': form,
        'resultados': None,
        'mostrar_resultados': False
    })


@login_required
def descargar_plantilla_excel(request):
    """
    Vista para descargar la plantilla Excel de ejemplo.
    """
    plantilla = generar_plantilla_excel()
    response = HttpResponse(
        plantilla.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="plantilla_libros.xlsx"'
    return response

## Cambio de Contraseña

def solicitar_cambio_password(request):
    """
    Vista para solicitar cambio de contraseña.
    Si el usuario está autenticado, usa su email. Si no, solicita el email.
    """
    debug_info = None
    
    if request.method == 'POST':
        form = PasswordChangeRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Si el usuario está autenticado, usar su email
            if request.user.is_authenticated:
                email = request.user.email
                user = request.user
            else:
                # Buscar usuario por email
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    # Por seguridad, no revelamos si el email existe
                    messages.success(request, 
                        'Si el correo electrónico existe en nuestro sistema, recibirás un enlace para cambiar tu contraseña.')
                    return redirect('solicitar_cambio_password')
            
            # Crear token
            token = PasswordResetToken.create_token(user)
            
            # Enviar email
            try:
                if enviar_email_cambio_password(user, token):
                    messages.success(request, 
                        'Se ha enviado un enlace a tu correo electrónico para cambiar tu contraseña. '
                        'Por favor revisa tu bandeja de entrada.')
                    return redirect('solicitar_cambio_password')
                else:
                    messages.error(request, 
                        'Hubo un error al enviar el email. Por favor intenta nuevamente más tarde.')
                    # En modo DEBUG, no redirigir para mostrar debug
                    if not settings.DEBUG:
                        return redirect('solicitar_cambio_password')
            except Exception as e:
                logger.error(f"Error al enviar email en vista: {e}")
                logger.error(traceback.format_exc())
                
                # En modo DEBUG, guardar información detallada y NO redirigir
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
                    error_detail = f"Error: {type(e).__name__}: {str(e)}"
                    messages.error(request, 
                        f'Error al enviar el email. {error_detail}. Revisa la consola del servidor y la sección de debug abajo para más detalles.')
                else:
                    messages.error(request, 
                        'Hubo un error al enviar el email. Por favor intenta nuevamente más tarde.')
                    return redirect('solicitar_cambio_password')
            
            # Si estamos en DEBUG y hay error, mostrar página con debug_info
            if settings.DEBUG and debug_info:
                context = {
                    'form': PasswordChangeRequestForm(initial={'email': email} if not request.user.is_authenticated else {}),
                    'debug': True,
                    'debug_info': debug_info,
                }
                return render(request, 'users/solicitar_cambio_password.html', context)
    else:
        # Si el usuario está autenticado, pre-llenar el email
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
        
        form = PasswordChangeRequestForm(initial=initial)
    
    # Agregar información de debug si está activado
    context = {
        'form': form,
        'debug': settings.DEBUG,
    }
    if debug_info:
        context['debug_info'] = debug_info
    
    return render(request, 'users/solicitar_cambio_password.html', context)


def confirmar_cambio_password(request, token):
    """
    Vista para confirmar y cambiar la contraseña usando el token.
    """
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'El enlace de cambio de contraseña es inválido o ha expirado.')
        return redirect('solicitar_cambio_password')
    
    # Validar token
    if not reset_token.is_valid():
        messages.error(request, 'El enlace de cambio de contraseña ha expirado o ya fue utilizado.')
        return redirect('solicitar_cambio_password')
    
    if request.method == 'POST':
        form = PasswordChangeConfirmForm(request.POST)
        if form.is_valid():
            # Cambiar contraseña
            new_password = form.cleaned_data['new_password2']
            reset_token.user.set_password(new_password)
            reset_token.user.save()
            
            # Marcar token como usado
            reset_token.mark_as_used()
            
            # Enviar email de confirmación
            enviar_email_confirmacion_cambio(reset_token.user)
            
            messages.success(request, 
                'Tu contraseña ha sido cambiada exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.')
            
            return redirect('login')
    else:
        form = PasswordChangeConfirmForm()
    
    return render(request, 'users/confirmar_cambio_password.html', {
        'form': form,
        'token': reset_token
    })


@login_required
def cambiar_password_desde_perfil(request):
    """
    Vista para cambiar contraseña desde el perfil (requiere contraseña actual).
    Cambia la contraseña inmediatamente y envía email de confirmación.
    """
    if request.method == 'POST':
        form = PasswordChangeFromProfileForm(request.user, request.POST)
        if form.is_valid():
            # Cambiar la contraseña inmediatamente (ya validamos la contraseña actual)
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            
            # Actualizar la sesión para evitar que el usuario sea deslogueado
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            # Enviar email de confirmación del cambio
            enviar_email_confirmacion_cambio(request.user)
            
            messages.success(request, 
                'Tu contraseña ha sido cambiada exitosamente. Se ha enviado un email de confirmación a tu correo electrónico.')
            
            return redirect('perfil')
    else:
        form = PasswordChangeFromProfileForm(request.user)
    
    return render(request, 'users/cambiar_password.html', {'form': form})


## Cambio de Email

@login_required
def solicitar_cambio_email(request):
    """
    Vista para solicitar cambio de email.
    Requiere contraseña actual y valida que el nuevo email sea único.
    """
    if request.method == 'POST':
        form = EmailChangeRequestForm(request.user, request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            
            # Crear token para confirmación por email
            token = EmailChangeToken.create_token(request.user, new_email)
            
            # Enviar email con enlace de confirmación
            if enviar_email_cambio_email(request.user, token, new_email):
                messages.success(request, 
                    'Se ha enviado un enlace de confirmación a tu nuevo correo electrónico. '
                    'Por favor revisa tu bandeja de entrada para completar el cambio.')
            else:
                messages.error(request, 
                    'Hubo un error al enviar el email. Por favor intenta nuevamente más tarde.')
            
            return redirect('perfil')
    else:
        form = EmailChangeRequestForm(request.user)
    
    return render(request, 'users/solicitar_cambio_email.html', {'form': form})


def confirmar_cambio_email(request, token):
    """
    Vista para confirmar y cambiar el email usando el token.
    """
    try:
        email_token = EmailChangeToken.objects.get(token=token)
    except EmailChangeToken.DoesNotExist:
        messages.error(request, 'El enlace de cambio de correo electrónico es inválido o ha expirado.')
        return redirect('solicitar_cambio_email')
    
    # Validar token
    if not email_token.is_valid():
        messages.error(request, 'El enlace de cambio de correo electrónico es inválido o ha expirado.')
        return redirect('solicitar_cambio_email')
    
    user = email_token.user
    old_email = user.email
    new_email = email_token.new_email
    
    if request.method == 'POST':
        # Cambiar el email
        user.email = new_email
        user.save()
        
        # Marcar token como usado
        email_token.used = True
        email_token.save()
        
        # Enviar email de confirmación al nuevo email
        enviar_email_confirmacion_cambio_email(user, old_email)
        
        messages.success(request, 
            f'Tu correo electrónico ha sido cambiado exitosamente de {old_email} a {new_email}.')
        
        # Si el usuario está autenticado, mantener la sesión
        if request.user.is_authenticated and request.user.id == user.id:
            return redirect('perfil')
        else:
            # Si no está autenticado o es otro usuario, redirigir a login
            return redirect('login')
    else:
        # Mostrar formulario de confirmación
        form = EmailChangeConfirmForm()
    
    return render(request, 'users/confirmar_cambio_email.html', {
        'form': form,
        'token': email_token,
        'old_email': old_email,
        'new_email': new_email,
    })


## Cerrar Sesión en Todos los Dispositivos

@login_required
def cerrar_sesiones_todas(request):
    """
    Vista para cerrar sesión en todos los dispositivos.
    Actualiza el timestamp session_invalidated_at en el perfil.
    """
    if request.method == 'POST':
        # Actualizar timestamp para invalidar todas las sesiones anteriores
        perfil = request.user.perfil
        perfil.session_invalidated_at = timezone.now()
        perfil.save()
        
        messages.success(request, 
            'Se han cerrado todas las sesiones en otros dispositivos. '
            'Tu sesión actual permanecerá activa hasta que cierres sesión manualmente.')
        
        return redirect('perfil')
    else:
        # Mostrar página de confirmación
        return render(request, 'users/cerrar_sesiones_todas.html')
