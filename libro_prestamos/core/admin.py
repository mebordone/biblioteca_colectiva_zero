from django.contrib import admin

# Register your models here.
from .models import Perfil, Libro, Prestamo

admin.site.register(Perfil)
admin.site.register(Libro)
admin.site.register(Prestamo)