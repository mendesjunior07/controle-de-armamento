from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import JSONField


class Policial(models.Model):
    nome_completo = models.CharField(max_length=100)
    nome_guerra = models.CharField(max_length=50, blank=True, null=True)  # Campo opcional
    posto_graduacao = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20, unique=True)
    rgpm = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)  # Inclui máscara de CPF se necessário

    def __str__(self):
        # Garantia de retorno consistente mesmo com valores nulos
        nome_guerra = self.nome_guerra if self.nome_guerra else 'Sem Nome de Guerra'
        return f"{self.nome_completo} - {nome_guerra}"


# Modelo para Categoria de Armamento
class Categoria(models.Model):
    nome = models.CharField(max_length=100,unique=True)

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

    # Dados do Veículo/Material
    marca = models.CharField(max_length=100, blank=True, null=True)  # Marca do veículo/arma
    modelo = models.CharField(max_length=100, blank=True, null=True)  # Modelo do veículo/arma
    placa = models.CharField(max_length=20, blank=True, null=True, unique=False)  # Placa do veículo (se aplicável)
    chassi = models.CharField(max_length=100, blank=True, null=True, unique=True)  # Chassi do veículo (se aplicável)
    ano = models.PositiveIntegerField(blank=True, null=True)  # Ano de fabricação

    # Procedência e Fornecedor
    procedencia = models.CharField(max_length=100, blank=True, null=True)  # Procedência do item
    fornecedor = models.CharField(max_length=100, blank=True, null=True)  # Fornecedor do item

    # Aparência e Estado
    aparencia_visual = models.TextField(verbose_name="Aparência Visual", blank=True, null=True)  # Descrição da aparência visual
    estado_conservacao = models.CharField(max_length=100, verbose_name="EST. DE CONSERVAÇÃO", blank=True, null=True)  # Estado de conservação
    cor = models.CharField(max_length=50, blank=True, null=True)  # Cor do item
    tamanho = models.CharField(max_length=50, blank=True, null=True)  # Tamanho do item

    # Localização e Destinação
    localizacao = models.CharField(max_length=200, blank=True, null=True)  # Localização atual
    destinacao = models.CharField(max_length=100, blank=True, null=True)  # Destinação do item
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='disponivel')  # Situação atual do item

    # Informações do Material
    tipo = models.CharField(max_length=50, blank=True, null=True)  # Tipo do material (arma, veículo, etc.)
    cal = models.CharField(max_length=50, blank=True, null=True)  # Calibre (se aplicável)
    ct = models.CharField(max_length=50, blank=True, null=True)  # Certificado Técnico (se aplicável)
    num_arma = models.CharField(max_length=100, verbose_name="Nº ARMA", blank=True, null=True, unique=True)  # Número da arma
    num_pmma = models.CharField(max_length=100, verbose_name="Nº PMMA", blank=True, null=True)  # Número PMMA
    tombo = models.CharField(max_length=100, blank=True, null=True)  # Número de tombo
    gr = models.CharField(max_length=50, verbose_name="GR", blank=True, null=True)  # Guia de Remessa ou campo específico
    
    # Validade e Observações
    data_vencimento = models.DateField(blank=True, null=True)  # Data de vencimento (se aplicável)
    observacao = models.TextField(verbose_name="OBSERVAÇÃO", blank=True, null=True)  # Observações adicionais

    # Relação com Categoria
    categoria = models.ForeignKey('Categoria', related_name='subcategorias_armamento', on_delete=models.CASCADE)

    # Campo para o usuário logado que inseriu os dados
    inserido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Relaciona com o usuário logado
    
    # Campo para a descrição completa
    descricao_completa = models.CharField(max_length=255, blank=True, null=True)

    # Sobrescrevendo o método save para gerar a combinação antes de salvar
    def save(self, *args, **kwargs):
        # Gera a descrição completa combinando os campos
        self.descricao_completa = f"{self.marca or ''} {self.modelo or ''} {self.placa or ''} {self.tipo or ''} {self.cal or ''} - Nº: {self.num_arma or ''}".strip()
        super(Subcategoria, self).save(*args, **kwargs)

    # Método __str__ para garantir que sempre retorne uma string
    def __str__(self):
        return self.descricao_completa or "Subcategoria sem descrição"


# Modelo para Categoria de Munição
class CategoriaMunicao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        # Retornar apenas o nome
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
    confirmado = models.BooleanField(default=False)  # Adiciona campo de confirmação
    confirmado_em = models.DateTimeField(null=True, blank=True)  # Data de confirmação
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
        return f"{self.policial.nome_completo} - {self.tipo_servico} - {self.data_descautelamento} {self.hora_descautelamento}"

class DescautelasCa(models.Model):
    data_hora_cautela = models.DateTimeField()
    policial = models.CharField(max_length=100)
    tipo_servico = models.CharField(max_length=50)
    categoria_armamento = models.CharField(max_length=50, null=True)
    subcategoria_armamento = models.CharField(max_length=50, null=True)
    categoria_municao = models.CharField(max_length=50, null=True)
    subcategoria_municao = models.CharField(max_length=50, null=True)
    quantidade_municao = models.IntegerField()
    situacao_armamento = models.CharField(max_length=50)
    observacao = models.TextField(blank=True, null=True)
    observacoes = models.TextField(null=True, blank=True)  # Adicione este campo
    armeiro = models.CharField(max_length=100)
    armeiro_descautela = models.CharField(max_length=100)
    data_descautelamento = models.DateField()
    hora_descautelamento = models.TimeField()

    def __str__(self):
        return f"Descautela de {self.policial} em {self.data_hora_cautela}"
    

class PassagemDeServico(models.Model):
    registro_cautela_id = models.IntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField(auto_now_add=True)  # Define automaticamente a data atual ao criar o registro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona ao usuário logado
    nome_substituto = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome_substituto} - {self.data_inicio} a {self.data_fim}"