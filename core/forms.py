#seguridad

from django import forms
from .models import Seguridad

class SeguridadForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Seguridad
        fields = ['nombre_apellido', 'dni', 'edad', 'fecha_ingreso', 'foto_dni']

        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }