from django.db import models


class PolicialMilitar(models.Model):
    # Dados pessoais
    nome_completo = models.CharField(max_length=255)
    numero_identificacao = models.CharField(
        max_length=50, unique=True)  # ID único para cada PM
    cpf = models.CharField(max_length=14, unique=True)  # CPF formatado (XXX.XXX.XXX-XX)
    data_nascimento = models.DateField()

    # Informações de contato
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)

    # Dados de serviço
    patente = models.CharField(max_length=50)  # Exemplo: "Soldado", "Cabo", "Sargento"
    unidade = models.CharField(max_length=100)  # Unidade onde serve
    data_ingresso = models.DateField()  # Data de ingresso na corporação
    lotacao_atual = models.CharField(
        max_length=100, blank=True, null=True)  # Seção, unidade atual
    # Situação na corporação
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativo', 'Ativo'),
            ('inativo', 'Inativo'),
            ('reserva', 'Reserva'),
            ('reformado', 'Reformado'),
        ],
        default='ativo'
    )

    # Outros dados
    observacoes = models.TextField(blank=True, null=True)  # Campo para observações adicionais

    def __str__(self):
        return f"{self.patente} {self.nome_completo}"

    class Meta:
        verbose_name = "Policial Militar"
        verbose_name_plural = "Policiais Militares"
        ordering = ['nome_completo']
