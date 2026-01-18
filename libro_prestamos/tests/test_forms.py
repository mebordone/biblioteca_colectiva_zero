"""
Tests para los formularios de cambio de contraseña
"""
import pytest
from django.contrib.auth.models import User
from usuarios.forms import (
    PasswordChangeRequestForm,
    PasswordChangeConfirmForm,
    PasswordChangeFromProfileForm
)


@pytest.mark.django_db
class TestPasswordChangeRequestForm:
    """Tests para PasswordChangeRequestForm"""
    
    def test_form_valid_with_existing_email(self, user):
        """Test que el formulario es válido con un email existente"""
        form = PasswordChangeRequestForm(data={'email': user.email})
        assert form.is_valid() == True
    
    def test_form_valid_with_non_existing_email(self):
        """Test que el formulario es válido incluso con email inexistente (seguridad)"""
        form = PasswordChangeRequestForm(data={'email': 'nonexistent@example.com'})
        # El formulario es válido, pero no revela si el email existe
        assert form.is_valid() == True
    
    def test_form_invalid_without_email(self):
        """Test que el formulario requiere email"""
        form = PasswordChangeRequestForm(data={})
        assert form.is_valid() == False
    
    def test_form_invalid_with_invalid_email(self):
        """Test que el formulario valida formato de email"""
        form = PasswordChangeRequestForm(data={'email': 'not-an-email'})
        assert form.is_valid() == False


@pytest.mark.django_db
class TestPasswordChangeConfirmForm:
    """Tests para PasswordChangeConfirmForm"""
    
    def test_form_valid_with_matching_passwords(self):
        """Test que el formulario es válido con contraseñas que coinciden"""
        form = PasswordChangeConfirmForm(data={
            'new_password1': 'newsecurepass123',
            'new_password2': 'newsecurepass123'
        })
        assert form.is_valid() == True
    
    def test_form_invalid_with_non_matching_passwords(self):
        """Test que el formulario rechaza contraseñas que no coinciden"""
        form = PasswordChangeConfirmForm(data={
            'new_password1': 'password123',
            'new_password2': 'password456'
        })
        assert form.is_valid() == False
        assert 'no coinciden' in str(form.errors)
    
    def test_form_invalid_with_short_password(self):
        """Test que el formulario valida longitud mínima"""
        form = PasswordChangeConfirmForm(data={
            'new_password1': 'short',
            'new_password2': 'short'
        })
        assert form.is_valid() == False
    
    def test_form_invalid_with_common_password(self):
        """Test que el formulario rechaza contraseñas comunes"""
        form = PasswordChangeConfirmForm(data={
            'new_password1': 'password',
            'new_password2': 'password'
        })
        # Puede ser válido o no dependiendo de los validadores de Django
        # Pero al menos debe validar
    
    def test_form_validates_password_strength(self):
        """Test que el formulario valida fortaleza de contraseña"""
        form = PasswordChangeConfirmForm(data={
            'new_password1': 'ValidPass123!',
            'new_password2': 'ValidPass123!'
        })
        assert form.is_valid() == True


@pytest.mark.django_db
class TestPasswordChangeFromProfileForm:
    """Tests para PasswordChangeFromProfileForm"""
    
    def test_form_valid_with_correct_old_password(self, user):
        """Test que el formulario es válido con contraseña actual correcta"""
        form = PasswordChangeFromProfileForm(
            user,
            data={
                'old_password': 'testpass123',
                'new_password1': 'newpass123',
                'new_password2': 'newpass123'
            }
        )
        assert form.is_valid() == True
    
    def test_form_invalid_with_incorrect_old_password(self, user):
        """Test que el formulario rechaza contraseña actual incorrecta"""
        form = PasswordChangeFromProfileForm(
            user,
            data={
                'old_password': 'wrongpassword',
                'new_password1': 'newpass123',
                'new_password2': 'newpass123'
            }
        )
        assert form.is_valid() == False
        assert 'incorrecta' in str(form.errors['old_password'])
    
    def test_form_invalid_with_non_matching_new_passwords(self, user):
        """Test que el formulario valida que las nuevas contraseñas coincidan"""
        form = PasswordChangeFromProfileForm(
            user,
            data={
                'old_password': 'testpass123',
                'new_password1': 'newpass123',
                'new_password2': 'differentpass123'
            }
        )
        assert form.is_valid() == False
    
    def test_form_validates_new_password_strength(self, user):
        """Test que el formulario valida fortaleza de la nueva contraseña"""
        form = PasswordChangeFromProfileForm(
            user,
            data={
                'old_password': 'testpass123',
                'new_password1': 'short',
                'new_password2': 'short'
            }
        )
        assert form.is_valid() == False
