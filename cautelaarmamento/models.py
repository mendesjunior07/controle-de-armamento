from django.db import models

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
