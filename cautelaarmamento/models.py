from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)

class Arma(models.Model):
    nome = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)

class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
