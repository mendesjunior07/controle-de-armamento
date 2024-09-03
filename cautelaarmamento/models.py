from django.db import models
from django.core.exceptions import ValidationError
from validate_docbr import CPF

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Subcategoria(models.Model):
    SITUACAO_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('em_manutencao', 'Em manutenção'),
        # Adicione outras situações conforme necessário
    ]

    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES)  # Campo de situação adicionado

    def __str__(self):
        return f'{self.nome} - {self.get_situacao_display()}'


class Policial(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class CautelaDeArmamento(models.Model):
    policial = models.ForeignKey(Policial, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    hora = models.DateTimeField(auto_now_add=True)  # Campo de hora adicionado
    data = models.DateField(auto_now_add=True)  # Campo de data adicionado

    def __str__(self):
        return f'{self.policial.nome} - {self.categoria.nome} - {self.subcategoria.nome} - {self.data} - {self.hora.strftime("%Y-%m-%d %H:%M:%S")}'


class Pessoa(models.Model):
    nome_completo = models.CharField(max_length=255)
    nome_guerra = models.CharField(max_length=255, blank=True, null=True)  # Pode ser nulo se não houver
    posto_graduacao = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)  # ID automático
    matricula = models.CharField(max_length=20, unique=True)
    rgpm = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    inclusao = models.DateField(auto_now_add=True)  # Data de inclusão automática
    restricao = models.BooleanField(default=False)
    cpf = models.CharField(max_length=14, unique=True)

    def clean(self):
        if not CPF(self.cpf).validate():
            raise ValidationError("CPF inválido")

    def __str__(self):
        return self.nome_completo 

