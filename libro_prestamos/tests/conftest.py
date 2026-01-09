"""
Configuración compartida para todos los tests
"""
import pytest
from django.contrib.auth.models import User
from core.models import Perfil, PasswordResetToken
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def user(db):
    """Crea un usuario de prueba"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    # Crear perfil asociado
    Perfil.objects.create(
        usuario=user,
        ciudad='Buenos Aires',
        pais='Argentina'
    )
    return user


@pytest.fixture
def another_user(db):
    """Crea otro usuario de prueba"""
    user = User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='otherpass123'
    )
    Perfil.objects.create(
        usuario=user,
        ciudad='Córdoba',
        pais='Argentina'
    )
    return user


@pytest.fixture
def password_reset_token(db, user):
    """Crea un token de cambio de contraseña válido"""
    return PasswordResetToken.create_token(user)


@pytest.fixture
def expired_token(db, user):
    """Crea un token expirado"""
    token = PasswordResetToken.create_token(user)
    token.expires_at = timezone.now() - timedelta(hours=1)
    token.save()
    return token


@pytest.fixture
def used_token(db, user):
    """Crea un token ya usado"""
    token = PasswordResetToken.create_token(user)
    token.mark_as_used()
    return token
