from django.db import models
from django.core.exceptions import ValidationError
import re

from validate_docbr import CPF

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Categoria_municoes(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Subcategoria_municoes(models.Model):
    SITUACAO_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('em_manutencao', 'Em manutenção'),
        ('cautelada', 'Cautelada'),
        # Adicione outras situações conforme necessário
    ]

    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias_municoes')
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES)  # Campo de situação adicionado
    
    
    def __str__(self):
        return f'{self.nome} - {self.get_situacao_display()}'
    
class Subcategoria(models.Model):
    SITUACAO_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('em_manutencao', 'Em manutenção'),
        ('cautelada', 'Cautelada'),
        # Adicione outras situações conforme necessário
    ]

    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias_municoes')
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES)  # Campo de situação adicionado
    
    
    def __str__(self):
        return f'{self.nome} - {self.get_situacao_display()}'


class Subcategoria_municoes(models.Model):


    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    quantidade = models.PositiveIntegerField(null=True, blank=True)
    

    def __str__(self):
        return f'{self.nome} - {self.get_situacao_display()}'




def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)  # Remove todos os caracteres não numéricos
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto > 9:
        resto = 0
    if int(cpf[9]) != resto:
        return False
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto > 9:
        resto = 0
    if int(cpf[10]) != resto:
        return False
    return True

class Policial(models.Model):
    nome_completo = models.CharField(max_length=255)
    nome_guerra = models.CharField(max_length=255, blank=True, null=True)
    posto_graduacao = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    rgpm = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    inclusao = models.DateField(auto_now_add=True)
    cpf = models.CharField(max_length=14, unique=True)

    def clean(self):
        if not validar_cpf(self.cpf):
            raise ValidationError("CPF inválido")

    def __str__(self):
        return self.nome_completo


class CautelaDeArmamento(models.Model):
    SERVICO_CHOICES = [
        ('24HORAS', '24 Horas'),
        ('QTU', 'QTU (12 Horas)'),
        ('GIRO', 'Giro (6 Horas)'),
        ('EXPEDIENTE', 'Expediente (8 Horas)'),
        ('PERMANENTE', 'Permanente'),
    ]
    tipo_servico = models.CharField(max_length=10, choices=SERVICO_CHOICES)
    policial = models.ForeignKey(Policial, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    hora = models.DateTimeField(auto_now_add=True)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.policial.nome_completo} - {self.categoria.nome} - {self.subcategoria.nome} - {self.data} - {self.hora.strftime("%Y-%m-%d %H:%M:%S")}'


class CautelaDeMunicoes(models.Model):

    categoria = models.ForeignKey(Categoria_municoes, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria_municoes, on_delete=models.CASCADE)
    hora = models.DateTimeField(auto_now_add=True)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.policial.nome_completo} - {self.categoria.nome} - {self.subcategoria.nome} - {self.data} - {self.hora.strftime("%Y-%m-%d %H:%M:%S")}'