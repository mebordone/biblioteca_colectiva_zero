from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    def __str__(self):
        return self.usuario.username

class Libro(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('no_disponible', 'No disponible'),
    ]
    nombre = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='disponible')
    
    def __str__(self):
        return f"{self.nombre} - {self.autor}"

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    prestatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_recibidos')
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_realizados')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    devuelto = models.BooleanField(default=False)
    comentario_devolucion = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.libro} - {self.prestatario}"
