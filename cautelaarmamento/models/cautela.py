from django.db import models
from .pessoal import PolicialMilitar
from .armamento import Municoes, Armas
from .veiculos import Vtr, Bicicleta, Moto
from django.utils import timezone


class Cautela(models.Model):
    policial_militar = models.ForeignKey(
        PolicialMilitar, on_delete=models.CASCADE)
    arma = models.ForeignKey(
        Armas, on_delete=models.SET_NULL, null=True, blank=True)
    municao = models.ForeignKey(
        Municoes, on_delete=models.SET_NULL, null=True, blank=True)
    vtr = models.ForeignKey(
        Vtr, on_delete=models.SET_NULL, null=True, blank=True)
    bicicleta = models.ForeignKey(
        Bicicleta, on_delete=models.SET_NULL, null=True, blank=True)
    moto = models.ForeignKey(
        Moto, on_delete=models.SET_NULL, null=True, blank=True)
    data_cautela = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    cautelado = models.BooleanField(default=False)
    data_cautela = models.DateTimeField(default=timezone.now)
    data_descautela = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Cautela - {self.policial_militar.nome_completo}'
