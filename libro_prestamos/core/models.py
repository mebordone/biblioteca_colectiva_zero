from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    session_invalidated_at = models.DateTimeField(null=True, blank=True, help_text='Timestamp para invalidar todas las sesiones anteriores')
    
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
    descripcion = models.TextField(blank=True, null=True)
    
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

class PasswordResetToken(models.Model):
    """Modelo para tokens de cambio de contraseña con confirmación por email"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'used']),
        ]
    
    def __str__(self):
        return f"Token para {self.user.username} - {'Usado' if self.used else 'Activo'}"
    
    @staticmethod
    def generate_token():
        """Genera un token seguro de 32 caracteres"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_token(user):
        """Crea un nuevo token para un usuario"""
        # Invalidar tokens anteriores no usados del mismo usuario
        PasswordResetToken.objects.filter(
            user=user,
            used=False,
            expires_at__gt=timezone.now()
        ).update(used=True)
        
        # Crear nuevo token
        token = PasswordResetToken.generate_token()
        expires_at = timezone.now() + timedelta(hours=24)
        
        return PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
    
    def is_valid(self):
        """Verifica si el token es válido (no usado y no expirado)"""
        if self.used:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True
    
    def mark_as_used(self):
        """Marca el token como usado"""
        self.used = True
        self.save()


class EmailChangeToken(models.Model):
    """
    Token para cambio de email con confirmación por email.
    Similar a PasswordResetToken pero para cambio de email.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_change_tokens')
    new_email = models.EmailField(max_length=254)
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'used']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Establecer expiración a 24 horas desde la creación
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Verifica si el token es válido (no usado y no expirado)"""
        return not self.used and self.expires_at > timezone.now()
    
    @staticmethod
    def generate_token():
        """Genera un token seguro de 32 bytes (43 caracteres URL-safe)"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def create_token(cls, user, new_email):
        """
        Crea un nuevo token para cambio de email.
        Invalida cualquier token anterior para este usuario.
        
        Args:
            user: Usuario que solicita el cambio
            new_email: Nuevo email a confirmar
        
        Returns:
            EmailChangeToken: Token creado
        """
        # Invalida cualquier token anterior para este usuario
        cls.objects.filter(user=user, used=False, expires_at__gt=timezone.now()).update(used=True)
        
        token_value = cls.generate_token()
        # Asegurar unicidad
        while cls.objects.filter(token=token_value).exists():
            token_value = cls.generate_token()
        
        token = cls(user=user, new_email=new_email, token=token_value)
        token.save()
        return token
    
    def __str__(self):
        return f"EmailChangeToken for {self.user.username} -> {self.new_email} - Valid: {self.is_valid()}"
