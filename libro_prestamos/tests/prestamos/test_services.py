"""
Tests para los servicios de lógica de negocio.
"""
import pytest
from django.contrib.auth.models import User
from libros.models import Libro
from prestamos.models import Prestamo
from prestamos.services import crear_prestamo_service, marcar_devuelto_service


@pytest.mark.django_db
class TestCrearPrestamoService:
    """Tests para el servicio crear_prestamo_service"""
    
    def test_crear_prestamo_exitoso(self, user):
        """Test que se crea un préstamo exitosamente"""
        # Crear otro usuario como prestatario
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        # Crear un libro disponible del usuario
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=user,
            estado='disponible'
        )
        
        # Crear préstamo usando el servicio
        prestamo, error = crear_prestamo_service(libro.id, prestatario.username, user)
        
        assert prestamo is not None
        assert error is None
        assert prestamo.libro == libro
        assert prestamo.prestatario == prestatario
        assert prestamo.prestador == user
        
        # Verificar que el libro cambió de estado
        libro.refresh_from_db()
        assert libro.estado == 'prestado'
    
    def test_crear_prestamo_libro_no_existe(self, user):
        """Test que falla si el libro no existe"""
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        prestamo, error = crear_prestamo_service(999, prestatario.username, user)
        
        assert prestamo is None
        assert error is not None
        assert "no existe" in error.lower() or "no está disponible" in error.lower()
    
    def test_crear_prestamo_libro_no_disponible(self, user):
        """Test que falla si el libro no está disponible"""
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        # Crear un libro prestado
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=user,
            estado='prestado'
        )
        
        prestamo, error = crear_prestamo_service(libro.id, prestatario.username, user)
        
        assert prestamo is None
        assert error is not None
    
    def test_crear_prestamo_libro_de_otro_usuario(self, user):
        """Test que falla si el libro pertenece a otro usuario"""
        otro_usuario = User.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123'
        )
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        # Crear un libro de otro usuario
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=otro_usuario,
            estado='disponible'
        )
        
        prestamo, error = crear_prestamo_service(libro.id, prestatario.username, user)
        
        assert prestamo is None
        assert error is not None
    
    def test_crear_prestamo_prestatario_no_existe(self, user):
        """Test que falla si el prestatario no existe"""
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=user,
            estado='disponible'
        )
        
        prestamo, error = crear_prestamo_service(libro.id, 'usuario_inexistente', user)
        
        assert prestamo is None
        assert error is not None
        assert "no existe" in error.lower()
    
    def test_crear_prestamo_a_si_mismo(self, user):
        """Test que falla si intenta prestar a sí mismo"""
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=user,
            estado='disponible'
        )
        
        prestamo, error = crear_prestamo_service(libro.id, user.username, user)
        
        assert prestamo is None
        assert error is not None
        assert "ti mismo" in error.lower() or "mismo" in error.lower()


@pytest.mark.django_db
class TestMarcarDevueltoService:
    """Tests para el servicio marcar_devuelto_service"""
    
    def test_marcar_devuelto_exitoso(self, user):
        """Test que se marca un préstamo como devuelto exitosamente"""
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=user,
            estado='prestado'
        )
        
        prestamo = Prestamo.objects.create(
            libro=libro,
            prestatario=prestatario,
            prestador=user,
            devuelto=False
        )
        
        # Marcar como devuelto usando el servicio
        resultado, error = marcar_devuelto_service(prestamo.id, user)
        
        assert resultado is not None
        assert error is None
        assert resultado.devuelto is True
        
        # Verificar que el libro cambió de estado
        libro.refresh_from_db()
        assert libro.estado == 'disponible'
    
    def test_marcar_devuelto_ya_devuelto(self, user):
        """Test que retorna mensaje si el préstamo ya está devuelto"""
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=user,
            estado='disponible'
        )
        
        prestamo = Prestamo.objects.create(
            libro=libro,
            prestatario=prestatario,
            prestador=user,
            devuelto=True
        )
        
        resultado, error = marcar_devuelto_service(prestamo.id, user)
        
        assert resultado is not None
        assert error is not None
        assert "ya ha sido marcado" in error.lower() or "ya está" in error.lower()
    
    def test_marcar_devuelto_prestamo_no_existe(self, user):
        """Test que falla si el préstamo no existe"""
        resultado, error = marcar_devuelto_service(999, user)
        
        assert resultado is None
        assert error is not None
        assert "no existe" in error.lower() or "permiso" in error.lower()
    
    def test_marcar_devuelto_otro_prestador(self, user):
        """Test que falla si intenta marcar un préstamo de otro usuario"""
        otro_usuario = User.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123'
        )
        prestatario = User.objects.create_user(
            username='prestatario',
            email='prestatario@test.com',
            password='testpass123'
        )
        
        libro = Libro.objects.create(
            nombre='Test Book',
            autor='Test Author',
            propietario=otro_usuario,
            estado='prestado'
        )
        
        prestamo = Prestamo.objects.create(
            libro=libro,
            prestatario=prestatario,
            prestador=otro_usuario,
            devuelto=False
        )
        
        # Intentar marcar como devuelto siendo otro usuario
        resultado, error = marcar_devuelto_service(prestamo.id, user)
        
        assert resultado is None
        assert error is not None
        assert "no existe" in error.lower() or "permiso" in error.lower()
