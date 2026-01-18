from django.db import models
from django.contrib.auth.models import User

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
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.autor}"
