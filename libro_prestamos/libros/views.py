from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import Libro
from .forms import LibroForm, CargaMasivaForm
from .utils import procesar_excel_libros, generar_plantilla_excel

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
        from prestamos.models import Prestamo
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
