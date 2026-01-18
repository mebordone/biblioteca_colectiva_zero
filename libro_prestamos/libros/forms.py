from django import forms
from .models import Libro

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
