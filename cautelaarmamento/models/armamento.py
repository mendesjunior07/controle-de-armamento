from django.db import models



class Armas(models.Model):
    numero_ordem = models.AutoField(primary_key=True)  # ID automático para cada entrada
    tipo = models.CharField(max_length=50)  # Tipo de arma, por exemplo, "Fuzil"
    marca = models.CharField(max_length=50)  # Marca da arma, por exemplo, "IMBEL"
    modelo = models.CharField(max_length=100)  # Modelo da arma, por exemplo, "SNIPER AGLC"
    calibre = models.CharField(max_length=10)  # Calibre da arma, por exemplo, "7.62mm"
    ct = models.CharField(max_length=50, blank=True, null=True)  # Informação de CT, se aplicável
    numero_arma = models.CharField(max_length=50)  # Número de série da arma
    numero_pmma = models.CharField(max_length=50, blank=True, null=True)  # Número PMMA, se aplicável
    localizacao = models.CharField(max_length=100)  # Localização atual da arma
    estado_conservacao = models.CharField(max_length=50)  # Estado de conservação da arma
    grupo_responsavel = models.CharField(max_length=50, blank=True, null=True)  # Grupo responsável, se aplicável
    processo = models.CharField(max_length=100, blank=True, null=True)  # Informação de processo, se aplicável
    observacao = models.TextField(blank=True, null=True)  # Observações adicionais

    def __str__(self):
        return f"{self.tipo} {self.marca} {self.modelo} - {self.numero_arma}"

class Municoes(models.Model):
    numero_ordem = models.AutoField(primary_key=True)  # ID automático para cada entrada
    tipo = models.CharField(max_length=100)  # Tipo de armamento, por exemplo, "Lançador de Cartuchos Químicos"
    calibre = models.CharField(max_length=50, blank=True, null=True)  # Calibre ou lote, se aplicável
    data_recebimento = models.DateField()  # Data de recebimento
    grupo_responsavel = models.CharField(max_length=100, blank=True, null=True)  # Grupo responsável (G.R.)
    processo = models.CharField(max_length=100, blank=True, null=True)  # Informação de processo (PROC.)
    recebida = models.IntegerField()  # Quantidade recebida
    consumida = models.IntegerField()  # Quantidade consumida
    saldo = models.IntegerField()  # Saldo restante
    cautelada = models.IntegerField(blank=True, null=True)  # Quantidade cautelada, se aplicável
    descarregadas = models.IntegerField(blank=True, null=True)  # Quantidade descarregada, se aplicável
    destino = models.CharField(max_length=100, blank=True, null=True)  # Destino final, se aplicável
    situacao = models.CharField(max_length=50, blank=True, null=True)  # Situação atual, se aplicável
    referencia = models.CharField(max_length=100, blank=True, null=True)  # Referência, se aplicável

    def __str__(self):
        return f"{self.tipo} - {self.numero_ordem}"