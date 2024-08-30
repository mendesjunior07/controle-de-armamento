from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PolicialMilitar(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    patente = models.CharField(max_length=50)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
    
class Armas(models.Model):
    STATUS_DISPONIBILIDADE = [
        ('Disponivel', 'Disponível'),
        ('Indisponivel', 'Indisponível'),
        ('verificar', 'Verificar'),
        ('manutencao', 'Manutenção'),
        ('quebrada', 'Quebrada'),
        # Adicione outras opções conforme necessário
    ]
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_de_serie = models.CharField(max_length=100, unique=True)
    disponivel = models.CharField(max_length=20, choices=STATUS_DISPONIBILIDADE)

    
    def __str__(self):
        return f"{self.tipo} - {self.modelo} ({self.numero_de_serie})"

class Vtr(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Cautela(models.Model):
    policial = models.ForeignKey(PolicialMilitar, on_delete=models.CASCADE)
    armamento = models.ForeignKey(Armas, on_delete=models.CASCADE)
    data_cautela = models.DateTimeField(default=timezone.now)
    data_descautela = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Cautela de {self.armamento} por {self.policial} em {self.data_cautela}"

    def descautelar(self):
        self.data_descautela = timezone.now()
        self.armamento.disponivel = True
        self.armamento.save()
        self.save()
