from django.db import models
from django.contrib.auth.models import User
from libros.models import Libro

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    prestatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_recibidos')
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_realizados')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    devuelto = models.BooleanField(default=False)
    comentario_devolucion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.libro} - {self.prestatario}"
