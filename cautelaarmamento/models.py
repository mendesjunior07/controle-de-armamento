from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Modelo para o Policial
class Policial(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Modelo para Categoria de Armamento
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Modelo para Subcategoria de Armamento
class Subcategoria(models.Model):
    SITUACAO_CHOICES = [
        ('disponivel', 'Disponível'),
        ('cautelada', 'Cautelada'),
        ('extraviado', 'Extraviado'),
        ('roubado', 'Roubado'),
        ('quebrado', 'Quebrado'),
        ('furado', 'Furado'),
        ('disparado', 'Disparado'),
    ]
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, related_name='subcategorias_armamento', on_delete=models.CASCADE)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='disponivel')

    def __str__(self):
        return f"{self.nome} ({self.categoria})"


# Modelo para Categoria de Munição
class CategoriaMunicao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Modelo para Subcategoria de Munição
class SubcategoriaMunicao(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaMunicao, related_name='subcategorias', on_delete=models.CASCADE)
    total_de_municoes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.categoria})"


# Modelo para Cautela de Armamento
class CautelaDeArmamento(models.Model):
    SERVICO_CHOICES = [
        ('operacional', 'Operacional'),
        ('administrativo', 'Administrativo')
    ]

    policial = models.ForeignKey(Policial, on_delete=models.CASCADE)
    tipo_servico = models.CharField(max_length=20, choices=SERVICO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    hora_cautela = models.DateTimeField(default=timezone.now)
    armeiro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.policial} - {self.categoria} - {self.subcategoria} ({self.tipo_servico})"


# Modelo para Cautela de Munições
class CautelaDeMunicoes(models.Model):
    policial = models.ForeignKey(Policial, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaMunicao, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubcategoriaMunicao, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.policial} - {self.categoria} - {self.subcategoria} - {self.quantidade} munições"


# Modelo para Registro de Cautela Completa
class RegistroCautelaCompleta(models.Model):
    data_hora = models.DateTimeField(default=timezone.now)
    policial = models.ForeignKey(Policial, on_delete=models.CASCADE)
    tipo_servico = models.CharField(max_length=20)
    categoria_armamento = models.CharField(max_length=100, blank=True, null=True)
    subcategoria_armamento = models.CharField(max_length=100, blank=True, null=True)
    categoria_municao = models.CharField(max_length=100, blank=True, null=True)
    subcategoria_municao = models.CharField(max_length=100, blank=True, null=True)
    quantidade_municao = models.PositiveIntegerField(default=0)
    armeiro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.policial} - {self.tipo_servico} - {self.data_hora}"


# Modelo para Registro de Descautelamento
class RegistroDescautelamento(models.Model):
    data_hora_cautela = models.DateTimeField()
    policial = models.ForeignKey('Policial', on_delete=models.CASCADE)
    tipo_servico = models.CharField(max_length=100)
    categoria_armamento = models.CharField(max_length=100, blank=True, null=True)
    subcategoria_armamento = models.CharField(max_length=100, blank=True, null=True)
    categoria_municao = models.CharField(max_length=100, blank=True, null=True)
    subcategoria_municao = models.CharField(max_length=100, blank=True, null=True)
    quantidade_municao = models.PositiveIntegerField(default=0)
    
    # Novo campo para capturar a situação do armamento
    situacao_armamento = models.CharField(max_length=20, blank=True, null=True)  # Nova situação do armamento

    # Campo para observações adicionais
    observacao = models.TextField(blank=True, null=True)  # Campo para observações
    
    # Atualização dos campos de armeiro
    armeiro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registrodescautelamento_armeiro')
    armeiro_descautela = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registrodescautelamento_armeiro_descautela')

    data_descautelamento = models.DateField(auto_now_add=True)  # Grava automaticamente a data
    hora_descautelamento = models.TimeField(auto_now_add=True)  # Grava automaticamente a hora

    def __str__(self):
        return f"{self.policial.nome} - {self.tipo_servico} - {self.data_descautelamento} {self.hora_descautelamento}"


class DescautelasCa(models.Model):
    data_hora_cautela = models.DateTimeField()
    policial = models.CharField(max_length=100)
    tipo_servico = models.CharField(max_length=50)
    categoria_armamento = models.CharField(max_length=50)
    subcategoria_armamento = models.CharField(max_length=50)
    categoria_municao = models.CharField(max_length=50, null=True)
    subcategoria_municao = models.CharField(max_length=50, null=True)
    quantidade_municao = models.IntegerField()
    situacao_armamento = models.CharField(max_length=50)
    observacao = models.TextField(blank=True, null=True)
    armeiro = models.CharField(max_length=100)
    armeiro_descautela = models.CharField(max_length=100)
    data_descautelamento = models.DateField()
    hora_descautelamento = models.TimeField()

    def __str__(self):
        return f"Descautela de {self.policial} em {self.data_hora_cautela}"