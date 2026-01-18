from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from .models import PasswordResetToken, EmailChangeToken
from .forms import (
    RegistroForm, PerfilForm,
    PasswordChangeRequestForm, PasswordChangeConfirmForm, PasswordChangeFromProfileForm,
    EmailChangeRequestForm, EmailChangeConfirmForm
)
from .services import (
    solicitar_cambio_password_service,
    confirmar_cambio_password_service,
    cambiar_password_desde_perfil_service,
    solicitar_cambio_email_service,
    confirmar_cambio_email_service
)
# Las funciones de email están en utils.py pero no se importan directamente en views
# Se usan a través de services

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
            user = request.user if request.user.is_authenticated else None
            
            # Llamar al servicio
            token, error = solicitar_cambio_password_service(user=user, email=email)
            
            # Manejar respuesta del servicio
            if token:
                # Éxito
                messages.success(request, 
                    'Se ha enviado un enlace a tu correo electrónico para cambiar tu contraseña. '
                    'Por favor revisa tu bandeja de entrada.')
                return redirect('solicitar_cambio_password')
            elif error is None:
                # Usuario no existe (por seguridad, no revelamos)
                messages.success(request, 
                    'Si el correo electrónico existe en nuestro sistema, recibirás un enlace para cambiar tu contraseña.')
                return redirect('solicitar_cambio_password')
            elif isinstance(error, dict):
                # Error con debug_info (modo DEBUG)
                debug_info = error
                error_detail = f"Error: {error.get('error_type', 'Unknown')}: {error.get('error_message', 'Unknown error')}"
                messages.error(request, 
                    f'Error al enviar el email. {error_detail}. Revisa la consola del servidor y la sección de debug abajo para más detalles.')
            else:
                # Error sin debug
                messages.error(request, 
                    'Hubo un error al enviar el email. Por favor intenta nuevamente más tarde.')
                if not settings.DEBUG:
                    return redirect('solicitar_cambio_password')
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
    # Obtener token para mostrar en el formulario
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
            new_password = form.cleaned_data['new_password2']
            
            # Llamar al servicio
            user, error = confirmar_cambio_password_service(token, new_password)
            
            if user:
                messages.success(request, 
                    'Tu contraseña ha sido cambiada exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.')
                return redirect('login')
            else:
                messages.error(request, error or 'Error al cambiar la contraseña.')
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
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            
            # Llamar al servicio
            user, error = cambiar_password_desde_perfil_service(
                request.user, 
                old_password, 
                new_password
            )
            
            if user:
                # Actualizar la sesión para evitar que el usuario sea deslogueado
                update_session_auth_hash(request, user)
                
                messages.success(request, 
                    'Tu contraseña ha sido cambiada exitosamente. Se ha enviado un email de confirmación a tu correo electrónico.')
                return redirect('perfil')
            else:
                # El error ya está en el formulario (validación de contraseña actual)
                # Pero por si acaso, mostrar mensaje
                messages.error(request, error or 'Error al cambiar la contraseña.')
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
            password = form.cleaned_data['password']
            
            # Llamar al servicio
            token, error = solicitar_cambio_email_service(
                request.user, 
                new_email, 
                password
            )
            
            if token:
                messages.success(request, 
                    'Se ha enviado un enlace de confirmación a tu nuevo correo electrónico. '
                    'Por favor revisa tu bandeja de entrada para completar el cambio.')
            else:
                messages.error(request, error or 'Hubo un error al enviar el email. Por favor intenta nuevamente más tarde.')
            
            return redirect('perfil')
    else:
        form = EmailChangeRequestForm(request.user)
    
    return render(request, 'users/solicitar_cambio_email.html', {'form': form})


def confirmar_cambio_email(request, token):
    """
    Vista para confirmar y cambiar el email usando el token.
    """
    # Obtener token para mostrar información en el formulario
    try:
        email_token = EmailChangeToken.objects.get(token=token)
    except EmailChangeToken.DoesNotExist:
        messages.error(request, 'El enlace de cambio de correo electrónico es inválido o ha expirado.')
        return redirect('solicitar_cambio_email')
    
    # Validar token
    if not email_token.is_valid():
        messages.error(request, 'El enlace de cambio de correo electrónico es inválido o ha expirado.')
        return redirect('solicitar_cambio_email')
    
    old_email = email_token.user.email
    new_email = email_token.new_email
    
    if request.method == 'POST':
        # Llamar al servicio
        user, old_email_result, new_email_result, error = confirmar_cambio_email_service(token)
        
        if user:
            messages.success(request, 
                f'Tu correo electrónico ha sido cambiado exitosamente de {old_email_result} a {new_email_result}.')
            
            # Si el usuario está autenticado, mantener la sesión
            if request.user.is_authenticated and request.user.id == user.id:
                return redirect('perfil')
            else:
                # Si no está autenticado o es otro usuario, redirigir a login
                return redirect('login')
        else:
            messages.error(request, error or 'Error al cambiar el correo electrónico.')
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
