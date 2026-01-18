from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Perfil

class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'ciudad', 'pais']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PasswordChangeRequestForm(forms.Form):
    """Formulario para solicitar cambio de contraseña"""
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico'
        }),
        help_text='Se enviará un enlace a este correo para cambiar tu contraseña'
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar que el email existe en el sistema
            if not User.objects.filter(email=email).exists():
                # Por seguridad, no revelamos si el email existe o no
                # Pero igualmente procesamos para no dar información a atacantes
                pass
        return email

class PasswordChangeConfirmForm(forms.Form):
    """Formulario para confirmar cambio de contraseña con nueva contraseña"""
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text='La contraseña debe tener al menos 8 caracteres'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        }),
        help_text='Repite la contraseña para confirmar'
    )
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Las contraseñas no coinciden')
        
        # Validar fortaleza de contraseña usando validadores de Django
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(password2)
        except ValidationError as e:
            raise ValidationError(e.messages)
        
        return password2

class PasswordChangeFromProfileForm(forms.Form):
    """Formulario para cambiar contraseña desde el perfil (requiere contraseña actual)"""
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña actual'
        })
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text='La contraseña debe tener al menos 8 caracteres'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        }),
        help_text='Repite la contraseña para confirmar'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError('La contraseña actual es incorrecta')
        return old_password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Las contraseñas no coinciden')
        
        # Validar fortaleza de contraseña
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(password2, self.user)
        except ValidationError as e:
            raise ValidationError(e.messages)
        
        return password2


class EmailChangeRequestForm(forms.Form):
    """Formulario para solicitar cambio de email (requiere contraseña actual)"""
    new_email = forms.EmailField(
        label='Nuevo correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nuevo correo electrónico'
        }),
        help_text='Se enviará un enlace de confirmación a este correo'
    )
    password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña actual'
        }),
        help_text='Necesitamos verificar tu identidad'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if new_email:
            # Verificar que el nuevo email sea diferente al actual
            if new_email.lower() == self.user.email.lower():
                raise ValidationError('El nuevo correo electrónico debe ser diferente al actual.')
            
            # Verificar que el email no esté en uso
            from django.contrib.auth.models import User
            if User.objects.filter(email__iexact=new_email).exists():
                raise ValidationError('Este correo electrónico ya está en uso por otro usuario.')
        
        return new_email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not self.user.check_password(password):
            raise ValidationError('La contraseña actual es incorrecta.')
        return password


class EmailChangeConfirmForm(forms.Form):
    """Formulario para confirmar cambio de email (solo muestra información)"""
    # Este formulario no necesita campos, solo se usa para mostrar la confirmación
    pass
