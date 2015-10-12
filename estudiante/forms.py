__author__ = 'davidpulloquinga'
# Importamor el model Taller para la creacion del formulario
from django import forms
from models import Taller

class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = "__all__" 