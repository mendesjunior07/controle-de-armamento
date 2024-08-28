# from django import forms
# from .models import Cautela, Armas, Municoes, Vtr, Bicicleta, Moto, PolicialMilitar


# class CautelamentodeViatura(forms.ModelForm):
#     class Meta:
#         model = Vtr
#         fields = ['marca']


# class CautelamentodeBicicleta(forms.ModelForm):
#     class Meta:
#         model = Bicicleta
#         fields = ['marca']


# class CautelamentodeMoto(forms.ModelForm):
#     class Meta:
#         model = Moto
#         fields = ['marca']


# class NomedosPms(forms.ModelForm):
#     class Meta:
#         model = PolicialMilitar
#         fields = ['nome_completo']  # Ou outros campos que você deseja incluir


# class CautelamentodeArmas(forms.ModelForm):
#     class Meta:
#         model = Armas
#         fields = ['tipo']


# class CautelamentodeMunicoes(forms.ModelForm):
#     class Meta:
#         model = Municoes
#         fields = ['tipo']


# class CautelaForm(forms.ModelForm):
#     class Meta:
#         model = Cautela
#         fields = ['policial_militar', 'arma', 'municao',
#                   'vtr', 'bicicleta', 'moto', 'observacao']

#     def __init__(self, *args, **kwargs):
#         super(CautelaForm, self).__init__(*args, **kwargs)
#         self.fields['policial_militar'].queryset = PolicialMilitar.objects.all()
#         self.fields['arma'].queryset = Armas.objects.filter(cautelado=False)
#         self.fields['municao'].queryset = Municoes.objects.filter(
#             cautelado=False)
#         self.fields['vtr'].queryset = Vtr.objects.filter(cautelado=False)
#         self.fields['bicicleta'].queryset = Bicicleta.objects.filter(
#             cautelado=False)
#         self.fields['moto'].queryset = Moto.objects.filter(cautelado=False)
