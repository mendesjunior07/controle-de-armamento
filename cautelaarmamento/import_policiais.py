##### QUANDO FOR ACRESCENTAR OS DADOS DOS POLICIAIS #####

import sys
import os
import pandas as pd

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# Configura o Django
import django
django.setup()

from cautelaarmamento.models import Policial

caminho_arquivo = r"cautelaarmamento/policiais.xlsx"

def importar_policiais(caminho_arquivo):
    try:
        # Lê o arquivo Excel no caminho especificado
        df = pd.read_excel(caminho_arquivo)
        print(f"Dados carregados do arquivo: {len(df)} registros encontrados.")

        # Converte e normaliza colunas para evitar erros
        df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce')
        df['autorizacao_arma'] = df['autorizacao_arma'].fillna(False).astype(bool)

        # Itera pelas linhas do DataFrame e cria os objetos
        for _, row in df.iterrows():
            try:
                policial = Policial.objects.create(
                    nome_completo=row['nome_completo'],
                    nome_guerra=row.get('nome_guerra', None),  # Aceita valores nulos
                    posto_graduacao=row['posto_graduacao'],
                    matricula=row['matricula'],
                    rgpm=row['rgpm'],
                    lotacao=row['lotacao'],
                    data_nascimento=row['data_nascimento'],
                    cpf=row['cpf'],
                    autorizacao_arma=row['autorizacao_arma']
                )
                print(f"Policial {policial.nome_completo} adicionado com sucesso.")
            except Exception as e:
                print(f"Erro ao adicionar o policial {row['nome_completo']}: {e}")
        
        print("Importação concluída com sucesso!")
    except Exception as e:
        print(f"Erro geral ao importar policiais: {e}")

# Executa a importação
if __name__ == "__main__":
    importar_policiais(caminho_arquivo)



# import os
# import django
# import pandas as pd

# # Configure o Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "controle_de_armamento.settings")  # Substitua pelo seu nome de projeto
# django.setup()

# # Agora, você pode importar o modelo
# from cautelaarmamento.models import Policial  # Substitua pelo nome correto do seu app

# # Caminho do arquivo
# caminho_arquivo = r"cautelaarmamento/policiais.xlsx"

# def importar_policiais(caminho_arquivo):
#     # Lê o arquivo Excel
#     df = pd.read_excel(caminho_arquivo)

#     # Itera pelas linhas do DataFrame e cria os objetos
#     for _, row in df.iterrows():
#         Policial.objects.create(
#             nome_completo=row['nome_completo'],
#             nome_guerra=row.get('nome_guerra', None),  # Aceita valores nulos
#             posto_graduacao=row['posto_graduacao'],
#             matricula=row['matricula'],
#             rgpm=row['rgpm'],
#             lotacao=row['lotacao'],
#             data_nascimento=row['data_nascimento'],
#             cpf=row['cpf']
#         )
#     print("Importação concluída com sucesso!")

# # Execute a função
# importar_policiais(caminho_arquivo)






# import pandas as pd
# import uuid  # Para gerar identificadores únicos
# from cautelaarmamento.models import Subcategoria, Categoria, User

# def importar_policiais(caminho_arquivo):
#     # Carregar o arquivo Excel
#     df = pd.read_excel(caminho_arquivo)

#     # Obter as colunas existentes no DataFrame
#     existing_columns = df.columns

#     # Tratar valores ausentes em colunas de texto
#     text_columns = [
#         'marca', 'modelo', 'placa', 'chassi', 'procedencia', 'fornecedor',
#         'aparencia_visual', 'estado_conservacao', 'cor', 'tamanho', 'localizacao',
#         'destinacao', 'situacao', 'tipo', 'cal', 'ct', 'num_pmma', 'tombo', 'gr', 'observacao'
#     ]
#     for col in text_columns:
#         if col in existing_columns:
#             df[col] = df[col].fillna('')

#     # Tratar colunas numéricas individualmente
#     if 'categoria_id' in existing_columns:
#         df['categoria_id'] = df['categoria_id'].fillna(0).astype(int)  # Preenchendo com 0 e convertendo para int
#     if 'inserido_por_id' in existing_columns:
#         df['inserido_por_id'] = df['inserido_por_id'].fillna(0).astype(int)
#     if 'ano' in existing_columns:
#         df['ano'] = df['ano'].fillna(0).astype(int)

#     # Preenchendo campos de data com pd.NaT
#     if 'data_vencimento' in existing_columns:
#         df['data_vencimento'] = df['data_vencimento'].fillna(pd.NaT)

#     # Iterar sobre cada linha do DataFrame para processar os dados
#     for index, row in df.iterrows():
#         try:
#             # Validar e buscar categoria
#             categoria_id = row.get('categoria_id')
#             if categoria_id is None or categoria_id == 0:
#                 print(f"Linha {index + 1}: categoria_id inválido. Ignorando...")
#                 continue
#             categoria = Categoria.objects.get(id=int(categoria_id))

#             # Validar e buscar usuário
#             inserido_por_id = row.get('inserido_por_id')
#             if inserido_por_id is None or inserido_por_id == 0:
#                 print(f"Linha {index + 1}: inserido_por_id inválido. Ignorando...")
#                 continue
#             inserido_por = User.objects.get(id=int(inserido_por_id))

#             # Tratar valores nulos ou inválidos para o campo `ano`
#             ano = row.get('ano')
#             if ano == 0:
#                 ano = None

#             # Tratar datas inválidas
#             data_vencimento = row.get('data_vencimento')
#             if pd.isnull(data_vencimento) or data_vencimento == pd.NaT:
#                 data_vencimento = None
#             elif isinstance(data_vencimento, str):
#                 try:
#                     data_vencimento = pd.to_datetime(data_vencimento, errors='coerce').date()
#                 except Exception:
#                     print(f"Linha {index + 1}: data_vencimento inválida. Ignorando...")
#                     data_vencimento = None
#             elif isinstance(data_vencimento, pd.Timestamp):
#                 data_vencimento = data_vencimento.date()

#             # Validar campo 'num_arma' - Gerar valor se estiver vazio
#             num_arma = row.get('num_arma')
#             if pd.isnull(num_arma) or num_arma in ['', 'NaN', None]:
#                 # Gerar um identificador único para `num_arma`
#                 num_arma = str(uuid.uuid4())  # Gera um identificador único
#                 print(f"Linha {index + 1}: Campo 'num_arma' estava vazio. Gerado valor: {num_arma}")

#             # Verificar duplicatas no banco de dados
#             if Subcategoria.objects.filter(num_arma=num_arma).exists():
#                 print(f"Linha {index + 1}: Subcategoria com num_arma {num_arma} já existe. Ignorando...")
#                 continue

#             # Criar nova subcategoria
#             subcategoria = Subcategoria(
#                 marca=row.get('marca'),
#                 modelo=row.get('modelo'),
#                 placa=row.get('placa'),
#                 chassi=row.get('chassi'),
#                 ano=ano,
#                 procedencia=row.get('procedencia'),
#                 fornecedor=row.get('fornecedor'),
#                 aparencia_visual=row.get('aparencia_visual'),
#                 estado_conservacao=row.get('estado_conservacao'),
#                 cor=row.get('cor'),
#                 tamanho=row.get('tamanho'),
#                 localizacao=row.get('localizacao'),
#                 destinacao=row.get('destinacao'),
#                 situacao=row.get('situacao'),
#                 tipo=row.get('tipo'),
#                 cal=row.get('cal'),
#                 ct=row.get('ct'),
#                 num_arma=num_arma,
#                 num_pmma=row.get('num_pmma'),
#                 tombo=row.get('tombo'),
#                 gr=row.get('gr'),
#                 data_vencimento=data_vencimento,
#                 observacao=row.get('observacao'),
#                 categoria=categoria,
#                 inserido_por=inserido_por,
#             )
#             subcategoria.save()  # Salvar a nova subcategoria
#             print(f"Linha {index + 1}: Subcategoria {num_arma} importada com sucesso!")

#         except Categoria.DoesNotExist:
#             print(f"Linha {index + 1}: Categoria com ID {categoria_id} não encontrada.")
#         except User.DoesNotExist:
#             print(f"Linha {index + 1}: Usuário com ID {inserido_por_id} não encontrado.")
#         except Exception as e:
#             print(f"Linha {index + 1}: Erro ao importar: {e}")

#     print("Importação concluída!")
