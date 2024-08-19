from django import forms
from .models import Pessoa, Arma, Equipamento

class RegistroForm(forms.Form):
    pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.all())
    arma = forms.ModelChoiceField(queryset=Arma.objects.filter(disponivel=True))
    equipamento = forms.ModelChoiceField(queryset=Equipamento.objects.filter(disponivel=True))
