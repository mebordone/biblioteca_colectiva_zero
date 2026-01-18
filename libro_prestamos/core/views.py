from django.shortcuts import render
from libros.models import Libro
from prestamos.models import Prestamo

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

def preguntas_frecuentes(request):
    """Vista para mostrar la página de preguntas frecuentes"""
    return render(request, 'preguntas_frecuentes.html')

def sobre_nosotros(request):
    """Vista para mostrar la página sobre nosotros"""
    return render(request, 'sobre_nosotros.html')

def como_ayudar(request):
    """Vista para mostrar la página de cómo ayudar a la Biblioteca Colectiva"""
    return render(request, 'como_ayudar.html')
