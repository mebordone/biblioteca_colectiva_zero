from django import forms
from .models import Libro, Perfil
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'autor', 'editorial', 'isbn','descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

from django.contrib.auth.models import User

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

class CargaMasivaForm(forms.Form):
    archivo_excel = forms.FileField(
        label='Archivo Excel',
        help_text='Sube un archivo Excel (.xlsx o .xls) con los libros a cargar',
        widget=forms.FileInput(attrs={'accept': '.xlsx,.xls'})
    )
    
    def clean_archivo_excel(self):
        archivo = self.cleaned_data.get('archivo_excel')
        if archivo:
            # Validar extensión
            nombre = archivo.name.lower()
            if not (nombre.endswith('.xlsx') or nombre.endswith('.xls')):
                raise forms.ValidationError('El archivo debe ser un Excel (.xlsx o .xls)')
            
            # Validar tamaño (5MB máximo)
            if archivo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede ser mayor a 5MB')
        
        return archivo

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