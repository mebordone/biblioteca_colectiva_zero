from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Libro, Prestamo
from .forms import LibroForm, RegistroForm, PerfilForm, CargaMasivaForm
from django.contrib.auth.models import User
from .models import Libro, Prestamo
from django.contrib import messages
from .utils import procesar_excel_libros, generar_plantilla_excel

def home(request):
    return render(request, 'home.html')

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
    libros = libro = Libro.objects.filter(propietario=request.user)
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

        # Validar selección de libro y prestatario
        libro = Libro.objects.filter(id=libro_id, propietario=request.user, estado='disponible').first()
        prestatario = User.objects.filter(username=prestatario_id).first()

        if libro and prestatario:
            # Crear el préstamo
            Prestamo.objects.create(
                libro=libro,
                prestatario=prestatario,
                prestador=request.user
            )
            # Actualizar estado del libro
            libro.estado = 'prestado'
            libro.save()
            return redirect('listar_prestamos')  # Redirige a la lista de préstamos

    # Filtrar libros disponibles del usuario actual
    libros = Libro.objects.filter(propietario=request.user, estado='disponible')
    # Excluir al usuario actual de la lista de usuarios
    usuarios = User.objects.exclude(id=request.user.id)

    return render(request, 'prestamos/crear.html', {'libros': libros, 'usuarios': usuarios})

@login_required
def listar_prestamos(request):
    # Obtener los préstamos de libros prestados por el usuario actual
    prestamos = Prestamo.objects.filter(prestador=request.user, devuelto=False).select_related('libro', 'prestatario')
    return render(request, 'prestamos/listar_prestamos.html', {'prestamos': prestamos})

@login_required
def historial_prestamos(request):
    # Obtener los préstamos de libros prestados por el usuario actual
    prestamos = Prestamo.objects.filter(prestador=request.user).select_related('libro', 'prestatario')
    return render(request, 'prestamos/listar_prestamos.html', {'prestamos': prestamos})

@login_required
def marcar_devuelto(request, prestamo_id):
    # Obtener el préstamo
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, prestador=request.user)

    # Verificar que no esté devuelto
    if prestamo.devuelto:
        messages.warning(request, "Este préstamo ya ha sido marcado como devuelto.")
    else:
        # Actualizar el estado del préstamo y del libro
        prestamo.devuelto = True
        prestamo.libro.estado = 'disponible'
        prestamo.libro.save()
        prestamo.save()
        messages.success(request, f"El libro '{prestamo.libro.nombre}' ha sido marcado como devuelto.")

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
