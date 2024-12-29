from django import forms
from .models import Libro, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'autor', 'editorial', 'isbn']
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