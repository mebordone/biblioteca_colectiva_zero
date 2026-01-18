from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Prestamo
from .services import crear_prestamo_service, marcar_devuelto_service
from libros.models import Libro

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
