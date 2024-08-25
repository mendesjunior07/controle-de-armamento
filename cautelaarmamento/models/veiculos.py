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
        ('TROLLER', 'Troller'),  # Troller é usado por algumas unidades especializadas
    ]
    
    SITUACOES = [
        ('DISPONIVEL', 'Disponível'),
        ('EM_USO', 'Em uso'),
        ('MANUTENCAO', 'Manutenção'),
        ('BAIXADO', 'Baixado'),
        ('RESERVA', 'Reserva'),  # Veículo em reserva para uso futuro
        ('EM_ABASTECIMENTO', 'Em abastecimento'),  # Veículo em processo de reabastecimento
        ('EM_DESLOCAMENTO', 'Em deslocamento'),  # Veículo em trânsito para outra localidade
        ('EM_OPERAÇÃO', 'Em operação'),  # Veículo em uso durante uma operação específica
        ('RETORNO', 'Retornando'),  # Veículo retornando de uma operação ou missão
        ('EM_REVISAO', 'Em revisão'),  # Veículo em revisão técnica programada
        ('EM_ADAPTACAO', 'Em adaptação'),  # Veículo sendo adaptado para novo uso ou missão
        ('DESATIVADO', 'Desativado'),  # Veículo fora de uso e aguardando destinação final
        ('EM_TREINAMENTO', 'Em treinamento'),  # Veículo em uso para treinamento de pessoal
        ('EM_REMOCAO', 'Em remoção'),  # Veículo sendo removido para manutenção ou outra localidade
        ('SOB_AVALIACAO', 'Sob avaliação'),  # Veículo sob avaliação para determinar condição ou destino
        ('EM_VISTORIA', 'Em vistoria'),  # Veículo sendo vistoriado por técnicos ou autoridades
    ]
    
    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=False)
    chassi = models.CharField(max_length=50, unique=False)
    ano = models.IntegerField()
    procedencia = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=100)
    aparencia_visual = models.TextField()
    destino = models.CharField(max_length=100)
    situacao = models.CharField(max_length=50, choices=SITUACOES)
    localizacao = models.CharField(max_length=100)
    observacao = models.TextField(blank=True, null=True)
    locada = models.BooleanField(default=False)

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
        ('HÍBRIDA', 'Híbrida'),
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

    def __str__(self):
        return f'{self.marca} {self.tipo} - {self.tombo}'
    
    class Moto(models.Model):
        numero_ordem = models.AutoField(primary_key=True)  # ID automático para cada entrada
        marca = models.CharField(max_length=50)  # Marca da moto, por exemplo, "Honda"
        modelo = models.CharField(max_length=100)  # Modelo da moto, por exemplo, "CG 160"
        placa = models.CharField(max_length=10)  # Placa da moto, por exemplo, "ABC-1234"
        chassi = models.CharField(max_length=50)  # Número do chassi
        ano = models.CharField(max_length=4)  # Ano do modelo, por exemplo, "2020"
        proc = models.CharField(max_length=100)  # Informação do processo, se aplicável
        fornec = models.CharField(max_length=100, blank=True, null=True)  # Fornecedor, se aplicável
        aparencia_visual = models.CharField(max_length=50)  # Aparência visual, por exemplo, "Caracterizada"
        destino = models.CharField(max_length=50)  # Destino da moto, por exemplo, "Operacional"
        situacao = models.CharField(max_length=50)  # Situação atual, por exemplo, "Operando"
        localizacao = models.CharField(max_length=100, blank=True, null=True)  # Localização atual da moto
        observacao = models.TextField(blank=True, null=True)  # Observações adicionais
