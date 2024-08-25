from django import forms
from .models import Vtr, Bicicleta, PolicialMilitar


class CautelamentodeViatura(forms.ModelForm):
    placa = forms.ModelChoiceField(
        queryset=Vtr.objects.all(),  # Consulta todos os objetos do modelo Vtr
        label='Placa',
        widget=forms.Select(attrs={'class': 'form-control'})  # Personalize o widget, se necessário
    )
    
    class Meta:
        model = Vtr
        fields = ['placa']
    
class CauteladeBicicleta(forms.ModelForm):
    marca = forms.ChoiceField(
        choices=Bicicleta.MARCAS,  # Usa as escolhas definidas no modelo Bicicleta
        label='Marca',
        widget=forms.Select(attrs={'class': 'form-control'})  # Personalize o widget, se necessário
    )

    class Meta:
        model = Bicicleta
        fields = ['marca']  # Inclua outros campos conforme necessário
    
class NomedosPms(forms.ModelForm):
    nome = forms.ModelChoiceField(
        queryset=PolicialMilitar.objects.all(),  # Consulta todos os objetos do modelo PolicialMilitar
        label='Nome',
        widget=forms.Select(attrs={'class': 'form-control'})  # Personalize o widget, se necessário
    )

    class Meta:
        model = PolicialMilitar
        fields = ['nome']  # Apenas o campo nome