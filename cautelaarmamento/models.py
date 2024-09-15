from django.db import models
from django.core.exceptions import ValidationError
import re

# Definição da classe Policial
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

# Definição da classe Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Definição da classe CautelaDeArmamento
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
    subcategoria = models.ForeignKey('Subcategoria', on_delete=models.CASCADE)  # Referência futura
    hora = models.DateTimeField(auto_now_add=True)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.policial.nome_completo} - {self.categoria.nome} - {self.subcategoria.nome} - {self.data} - {self.hora.strftime("%Y-%m-%d %H:%M:%S")}'

# Definição da classe Subcategoria
class Subcategoria(models.Model):
    SITUACAO_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('em_manutencao', 'Em manutenção'),
        ('cautelada', 'Cautelada'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias_armamento')
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES)

    # Adicionando os novos campos

    def __str__(self):
        return f'{self.nome} - {self.categoria.nome} - {self.get_situacao_display()}'

# Função de validação de CPF
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = 11 - (soma % 11)
    if resto > 9:
        resto = 0
    if int(cpf[9]) != resto:
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = 11 - (soma % 11)
    if resto > 9:
        resto = 0
    return int(cpf[10]) == resto

# Definição da classe Categoria de Munição
class CategoriaMunicao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Definição da classe Subcategoria de Munição
class SubcategoriaMunicao(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaMunicao, on_delete=models.CASCADE, related_name='subcategorias')
    total_de_municoes = models.IntegerField(default=0)  # Campo para o total de munições

    def __str__(self):
        return self.nome

# Definição da classe Cautela de Munições
class CautelaDeMunicoes(models.Model):
    categoria = models.ForeignKey(CategoriaMunicao, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubcategoriaMunicao, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def __str__(self):
        return f'{self.categoria} - {self.subcategoria} - {self.quantidade}'

# Nova Classe: Item de Munição Cautelada
class MunicaoCautelada(models.Model):
    cautela = models.ForeignKey(CautelaDeArmamento, related_name='municoes', on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaMunicao, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubcategoriaMunicao, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_cautela = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.categoria} - {self.subcategoria} - {self.quantidade} - {self.data_cautela.strftime("%Y-%m-%d %H:%M:%S")}'

# Nova Classe: Item de Armamento Cautelado
class ArmamentoCautelado(models.Model):
    cautela = models.ForeignKey(CautelaDeArmamento, related_name='armamentos', on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    data_cautela = models.DateTimeField(auto_now_add=True)
    nome_guerra = models.ForeignKey(Policial, on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategorias_armamento')  # Nome do policial
    tipo_servico = models.CharField(max_length=10, choices=CautelaDeArmamento.SERVICO_CHOICES, null=True, blank=True)  # Tipo de serviço

    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.categoria.nome} - {self.subcategoria.nome} - {self.data_cautela.strftime("%Y-%m-%d %H:%M:%S")}'
