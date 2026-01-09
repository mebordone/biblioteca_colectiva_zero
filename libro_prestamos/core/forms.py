from django import forms
from .models import Libro, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'autor', 'editorial', 'isbn','descripcion']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }

from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'ciudad', 'pais']

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