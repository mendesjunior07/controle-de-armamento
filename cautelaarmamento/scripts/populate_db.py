# meu_app/scripts/populate_db.py

import os
import django
import random
from faker import Faker
from meu_app.models import Policial, Categoria, Subcategoria, CautelaDeArmamento

# Configuração para usar o Django fora do ambiente de servidor
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

# Criando uma instância da biblioteca Faker
fake = Faker('pt_BR')  # Usando 'pt_BR' para gerar dados em português

# Definindo o número de registros a serem criados
NUM_POLICIAIS = 10
NUM_CATEGORIAS = 5
NUM_SUBCATEGORIAS = 15
NUM_CAUTELAS = 20

# Função para preencher a tabela Policial
def create_policiais():
    for _ in range(NUM_POLICIAIS):
        Policial.objects.create(nome=fake.name())

# Função para preencher a tabela Categoria
def create_categorias():
    for _ in range(NUM_CATEGORIAS):
        Categoria.objects.create(nome=fake.word())

# Função para preencher a tabela Subcategoria
def create_subcategorias():
    categorias = list(Categoria.objects.all())
    situacao_choices = ['disponivel', 'indisponivel', 'em_manutencao']

    for _ in range(NUM_SUBCATEGORIAS):
        categoria = random.choice(categorias)
        situacao = random.choice(situacao_choices)
        Subcategoria.objects.create(nome=fake.word(), categoria=categoria, situacao=situacao)

# Função para preencher a tabela CautelaDeArmamento
def create_cautelas():
    policiais = list(Policial.objects.all())
    categorias = list(Categoria.objects.all())
    subcategorias = list(Subcategoria.objects.all())

    for _ in range(NUM_CAUTELAS):
        policial = random.choice(policiais)
        categoria = random.choice(categorias)
        subcategoria = random.choice(subcategorias)
        CautelaDeArmamento.objects.create(
            policial=policial,
            categoria=categoria,
            subcategoria=subcategoria
        )

# Executando as funções
if __name__ == '__main__':
    create_categorias()
    create_subcategorias()
    create_policiais()
    create_cautelas()
    print("Dados de teste inseridos com sucesso!")
