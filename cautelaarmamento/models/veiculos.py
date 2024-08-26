from django.db import models


class Vtr(models.Model):
    MARCAS = [
        ('TOYOTA', 'Toyota'),
        ('FORD', 'Ford'),
        ('CHEVROLET', 'Chevrolet'),
        ('FIAT', 'Fiat'),
        ('VOLKSWAGEN', 'Volkswagen'),
        ('MITSUBISHI', 'Mitsubishi'),
        ('RENAULT', 'Renault'),
        ('JEEP', 'Jeep'),
        ('HYUNDAI', 'Hyundai'),
        ('HONDA', 'Honda'),
        ('NISSAN', 'Nissan'),
        ('TROLLER', 'Troller'),
    ]

    SITUACOES = [
        ('DISPONIVEL', 'Disponível'),
        ('EM_USO', 'Em uso'),
        ('MANUTENCAO', 'Manutenção'),
        ('BAIXADO', 'Baixado'),
        ('RESERVA', 'Reserva'),
        ('EM_ABASTECIMENTO', 'Em abastecimento'),
        ('EM_DESLOCAMENTO', 'Em deslocamento'),
        ('EM_OPERACAO', 'Em operação'),
        ('RETORNO', 'Retornando'),
        ('EM_REVISAO', 'Em revisão'),
        ('EM_ADAPTACAO', 'Em adaptação'),
        ('DESATIVADO', 'Desativado'),
        ('EM_TREINAMENTO', 'Em treinamento'),
        ('EM_REMOCAO', 'Em remoção'),
        ('SOB_AVALIACAO', 'Sob avaliação'),
        ('EM_VISTORIA', 'Em vistoria'),
    ]
    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    chassi = models.CharField(max_length=50)
    ano = models.IntegerField()
    procedencia = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=100)
    aparencia_visual = models.TextField()
    destino = models.CharField(max_length=100)
    situacao = models.CharField(max_length=50, choices=SITUACOES)
    localizacao = models.CharField(max_length=100)
    observacao = models.TextField(blank=True, null=True)
    locada = models.BooleanField(default=False)
    cautelado = models.BooleanField(default=False)  # Campo adicionado

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'


class Bicicleta(models.Model):
    MARCAS = [
        ('CALOI', 'Caloi'),
        ('MONARK', 'Monark'),
        ('HOUSTON', 'Houston'),
        ('SCOTT', 'Scott'),
        ('TREK', 'Trek'),
        ('GTS', 'GTS'),
        ('SHIMANO', 'Shimano'),
        ('GHOST', 'Ghost'),
    ]

    TIPOS = [
        ('MTB', 'Mountain Bike'),
        ('URBANA', 'Urbana'),
        ('SPEED', 'Speed'),
        ('BMX', 'BMX'),
        ('ELETRICA', 'Elétrica'),
        ('FIXA', 'Fixa'),
        ('HIBRIDA', 'Híbrida'),
    ]

    SITUACOES = [
        ('DISPONIVEL', 'Disponível'),
        ('EM_USO', 'Em uso'),
        ('MANUTENCAO', 'Manutenção'),
        ('BAIXADO', 'Baixado'),
        ('RESERVA', 'Reserva'),
    ]

    marca = models.CharField(max_length=50, choices=MARCAS)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    ano = models.IntegerField()
    cor = models.CharField(max_length=50)
    procedencia = models.CharField(max_length=100)
    doc_ref = models.CharField("Documento de Referência", max_length=100)
    situacao = models.CharField(max_length=50, choices=SITUACOES)
    tombo = models.CharField(max_length=50, unique=True)
    localizacao = models.CharField(max_length=100)
    cautelado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.marca} {self.tipo} - {self.tombo}'


class Moto(models.Model):
    MARCAS = [
        ('HONDA', 'Honda'),
        ('YAMAHA', 'Yamaha'),
        ('SUZUKI', 'Suzuki'),
        ('KAWASAKI', 'Kawasaki'),
        ('BMW', 'BMW'),
        ('HARLEY-DAVIDSON', 'Harley-Davidson'),
    ]

    SITUACOES = [
        ('DISPONIVEL', 'Disponível'),
        ('EM_USO', 'Em uso'),
        ('MANUTENCAO', 'Manutenção'),
        ('BAIXADO', 'Baixado'),
        ('RESERVA', 'Reserva'),
    ]

    numero_ordem = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    chassi = models.CharField(max_length=50)
    ano = models.IntegerField()
    processo = models.CharField(max_length=100)  # Informação do processo
    fornecedor = models.CharField(
        max_length=100, blank=True, null=True)  # Fornecedor
    aparencia_visual = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)
    situacao = models.CharField(max_length=50, choices=SITUACOES)
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    cautelado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'
