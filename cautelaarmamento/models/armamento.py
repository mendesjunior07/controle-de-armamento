from django.db import models

class Armas(models.Model):
    # ID automático para cada entrada
    numero_ordem = models.AutoField(primary_key=True)
    # Tipo de arma, por exemplo, "Fuzil"
    tipo = models.CharField(max_length=50)
    # Marca da arma, por exemplo, "IMBEL"
    marca = models.CharField(max_length=50)
    # Modelo da arma, por exemplo, "SNIPER AGLC"
    modelo = models.CharField(max_length=100)
    # Calibre da arma, por exemplo, "7.62mm"
    calibre = models.CharField(max_length=10)
    # Informação de CT, se aplicável
    ct = models.CharField(max_length=50, blank=True, null=True)
    numero_arma = models.CharField(max_length=50)  # Número de série da arma
    numero_pmma = models.CharField(
        max_length=50, blank=True, null=True)  # Número PMMA, se aplicável
    localizacao = models.CharField(max_length=100)  # Localização atual da arma
    estado_conservacao = models.CharField(
        max_length=50)  # Estado de conservação da arma
    grupo_responsavel = models.CharField(
        max_length=50, blank=True, null=True)  # Grupo responsável, se aplicável
    # Informação de processo, se aplicável
    processo = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(
        blank=True, null=True)  # Observações adicionais
    # Adicionando um campo cautelado
    cautelado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo} {self.marca} {self.modelo} - {self.numero_arma}"


class Municoes(models.Model):
    # ID automático para cada entrada
    numero_ordem = models.AutoField(primary_key=True)
    # Tipo de armamento, por exemplo, "Lançador de Cartuchos Químicos"
    tipo = models.CharField(max_length=100)
    # Calibre ou lote, se aplicável
    calibre = models.CharField(max_length=50, blank=True, null=True)
    data_recebimento = models.DateField()  # Data de recebimento
    grupo_responsavel = models.CharField(
        max_length=100, blank=True, null=True)  # Grupo responsável (G.R.)
    # Informação de processo (PROC.)
    processo = models.CharField(max_length=100, blank=True, null=True)
    recebida = models.IntegerField()  # Quantidade recebida
    consumida = models.IntegerField(default=0)  # Quantidade consumida
    saldo = models.IntegerField(default=0)  # Saldo restante
    # Quantidade cautelada, se aplicável
    cautelada = models.IntegerField(default=0, blank=True, null=True)
    # Quantidade descarregada, se aplicável
    descarregadas = models.IntegerField(default=0, blank=True, null=True)
    # Destino final, se aplicável
    destino = models.CharField(max_length=100, blank=True, null=True)
    # Situação atual, se aplicável
    situacao = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField(
        max_length=100, blank=True, null=True)  # Referência, se aplicável
    # Campo para indicar se as munições estão cauteladas
    cautelado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo} - {self.numero_ordem}"
