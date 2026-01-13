"""
Servicios para la lógica de negocio del sistema de préstamos.
Separa la lógica de negocio de las vistas según AGENT.md.
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Libro, Prestamo


def crear_prestamo_service(libro_id, prestatario_id, prestador):
    """
    Servicio para crear un préstamo y actualizar el estado del libro.
    
    Args:
        libro_id: ID del libro a prestar
        prestatario_id: Username del usuario que recibirá el préstamo
        prestador: Usuario que presta el libro
        
    Returns:
        tuple: (prestamo, None) si es exitoso, (None, error_message) si hay error
        
    Raises:
        ValidationError: Si la validación falla
    """
    # Validar que el libro existe, pertenece al prestador y está disponible
    libro = Libro.objects.filter(
        id=libro_id,
        propietario=prestador,
        estado='disponible'
    ).first()
    
    if not libro:
        return None, "El libro no existe, no te pertenece o no está disponible."
    
    # Validar que el prestatario existe
    prestatario = User.objects.filter(username=prestatario_id).first()
    
    if not prestatario:
        return None, "El usuario prestatario no existe."
    
    # Validar que no se preste a sí mismo
    if prestador.id == prestatario.id:
        return None, "No puedes prestar un libro a ti mismo."
    
    # Crear el préstamo
    prestamo = Prestamo.objects.create(
        libro=libro,
        prestatario=prestatario,
        prestador=prestador
    )
    
    # Actualizar estado del libro
    libro.estado = 'prestado'
    libro.save()
    
    return prestamo, None


def marcar_devuelto_service(prestamo_id, prestador):
    """
    Servicio para marcar un préstamo como devuelto y actualizar el estado del libro.
    
    Args:
        prestamo_id: ID del préstamo a marcar como devuelto
        prestador: Usuario que prestó el libro (para validación)
        
    Returns:
        tuple: (prestamo, None) si es exitoso, (None, error_message) si hay error
        
    Raises:
        Prestamo.DoesNotExist: Si el préstamo no existe
    """
    # Obtener el préstamo
    try:
        prestamo = Prestamo.objects.get(id=prestamo_id, prestador=prestador)
    except Prestamo.DoesNotExist:
        return None, "El préstamo no existe o no tienes permiso para marcarlo como devuelto."
    
    # Verificar que no esté ya devuelto
    if prestamo.devuelto:
        return prestamo, "Este préstamo ya ha sido marcado como devuelto."
    
    # Actualizar el estado del préstamo y del libro
    prestamo.devuelto = True
    prestamo.libro.estado = 'disponible'
    prestamo.libro.save()
    prestamo.save()
    
    return prestamo, None
