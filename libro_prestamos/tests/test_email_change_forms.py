"""
Tests para los formularios de cambio de email
"""
import pytest
from django.contrib.auth.models import User
from core.forms import EmailChangeRequestForm, EmailChangeConfirmForm
from core.models import Perfil


@pytest.fixture
def user(db):
    """Fixture para crear un usuario de prueba"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    Perfil.objects.create(
        usuario=user,
        ciudad='Buenos Aires',
        pais='Argentina'
    )
    return user


@pytest.mark.django_db
class TestEmailChangeRequestForm:
    """Tests para EmailChangeRequestForm"""
    
    def test_form_valid_with_different_email(self, user):
        """Test que el formulario es válido con un email diferente"""
        form = EmailChangeRequestForm(user, data={
            'new_email': 'newemail@example.com',
            'password': 'testpass123'
        })
        
        assert form.is_valid()
        assert form.cleaned_data['new_email'] == 'newemail@example.com'
    
    def test_form_invalid_same_email(self, user):
        """Test que el formulario rechaza el mismo email"""
        form = EmailChangeRequestForm(user, data={
            'new_email': user.email,
            'password': 'testpass123'
        })
        
        assert not form.is_valid()
        assert 'new_email' in form.errors
    
    def test_form_invalid_existing_email(self, user):
        """Test que el formulario rechaza un email ya en uso"""
        # Crear otro usuario con ese email
        User.objects.create_user(
            username='otheruser',
            email='existing@example.com',
            password='pass123'
        )
        
        form = EmailChangeRequestForm(user, data={
            'new_email': 'existing@example.com',
            'password': 'testpass123'
        })
        
        assert not form.is_valid()
        assert 'new_email' in form.errors
    
    def test_form_invalid_wrong_password(self, user):
        """Test que el formulario rechaza contraseña incorrecta"""
        form = EmailChangeRequestForm(user, data={
            'new_email': 'newemail@example.com',
            'password': 'wrongpassword'
        })
        
        assert not form.is_valid()
        assert 'password' in form.errors
    
    def test_form_invalid_without_password(self, user):
        """Test que el formulario requiere contraseña"""
        form = EmailChangeRequestForm(user, data={
            'new_email': 'newemail@example.com',
        })
        
        assert not form.is_valid()
    
    def test_form_invalid_without_email(self, user):
        """Test que el formulario requiere email"""
        form = EmailChangeRequestForm(user, data={
            'password': 'testpass123'
        })
        
        assert not form.is_valid()
    
    def test_form_invalid_invalid_email_format(self, user):
        """Test que el formulario valida formato de email"""
        form = EmailChangeRequestForm(user, data={
            'new_email': 'not-an-email',
            'password': 'testpass123'
        })
        
        assert not form.is_valid()


@pytest.mark.django_db
class TestEmailChangeConfirmForm:
    """Tests para EmailChangeConfirmForm"""
    
    def test_form_has_no_fields(self):
        """Test que el formulario no tiene campos (solo confirmación)"""
        form = EmailChangeConfirmForm()
        
        assert len(form.fields) == 0
