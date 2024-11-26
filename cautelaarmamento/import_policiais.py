# import pandas as pd
# from cautelaarmamento.models import Policial  # Substitua pelo nome correto do seu app

# caminho_arquivo = r"cautelaarmamento\policiais.xlsx"

# def importar_policiais(caminho_arquivo):
#     # Lê o arquivo Excel no caminho especificado
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


import pandas as pd
from cautelaarmamento.models import Subcategoria, Categoria, User

def importar_policiais(caminho_arquivo):
    # Carregar o arquivo Excel
    df = pd.read_excel(caminho_arquivo)

    # Verificar se todas as colunas esperadas estão presentes
    expected_columns = [
        'categoria_id', 'inserido_por_id', 'marca', 'modelo', 'placa', 'chassi',
        'ano', 'procedencia', 'fornecedor', 'aparencia_visual', 'estado_conservacao',
        'cor', 'tamanho', 'localizacao', 'destinacao', 'situacao', 'tipo', 'cal',
        'ct', 'num_arma', 'num_pmma', 'tombo', 'gr', 'data_vencimento', 'observacao'
    ]
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Colunas ausentes no Excel: {missing_columns}")

    for index, row in df.iterrows():
        try:
            # Validar e buscar categoria
            categoria_id = row.get('categoria_id')
            if pd.isnull(categoria_id) or not str(categoria_id).isdigit():
                print(f"Linha {index + 1}: categoria_id inválido. Ignorando...")
                continue
            categoria = Categoria.objects.get(id=int(categoria_id))

            # Validar e buscar usuário
            inserido_por_id = row.get('inserido_por_id')
            if pd.isnull(inserido_por_id) or not str(inserido_por_id).isdigit():
                print(f"Linha {index + 1}: inserido_por_id inválido. Ignorando...")
                continue
            inserido_por = User.objects.get(id=int(inserido_por_id))

            # Tratar valores nulos ou inválidos
            ano = row.get('ano')
            if pd.isnull(ano) or not str(ano).isdigit():
                ano = None
            else:
                ano = int(ano)

            # Tratar datas inválidas
            data_vencimento = row.get('data_vencimento')
            if pd.isnull(data_vencimento) or data_vencimento in [None, '']:
                data_vencimento = None
            elif isinstance(data_vencimento, str):
                try:
                    data_vencimento = pd.to_datetime(data_vencimento, errors='coerce').date()
                except Exception:
                    print(f"Linha {index + 1}: data_vencimento inválida. Ignorando...")
                    data_vencimento = None
            elif isinstance(data_vencimento, pd.Timestamp):
                data_vencimento = data_vencimento.date()
            else:
                print(f"Linha {index + 1}: Formato de data_vencimento não reconhecido. Ignorando...")
                data_vencimento = None

            # Verificar duplicatas
            if Subcategoria.objects.filter(num_arma=row.get('num_arma')).exists():
                print(f"Linha {index + 1}: Subcategoria com num_arma {row.get('num_arma')} já existe. Ignorando...")
                continue

            # Criar nova subcategoria
            Subcategoria.objects.create(
                marca=row.get('marca'),
                modelo=row.get('modelo'),
                placa=row.get('placa'),
                chassi=row.get('chassi'),
                ano=ano,
                procedencia=row.get('procedencia'),
                fornecedor=row.get('fornecedor'),
                aparencia_visual=row.get('aparencia_visual'),
                estado_conservacao=row.get('estado_conservacao'),
                cor=row.get('cor'),
                tamanho=row.get('tamanho'),
                localizacao=row.get('localizacao'),
                destinacao=row.get('destinacao'),
                situacao=row.get('situacao'),
                tipo=row.get('tipo'),
                cal=row.get('cal'),
                ct=row.get('ct'),
                num_arma=row.get('num_arma'),
                num_pmma=row.get('num_pmma'),
                tombo=row.get('tombo'),
                gr=row.get('gr'),
                data_vencimento=data_vencimento,
                observacao=row.get('observacao'),
                categoria=categoria,
                inserido_por=inserido_por,
            )
            print(f"Linha {index + 1}: Subcategoria {row.get('num_arma')} importada com sucesso!")
        except Categoria.DoesNotExist:
            print(f"Linha {index + 1}: Categoria com ID {categoria_id} não encontrada.")
        except User.DoesNotExist:
            print(f"Linha {index + 1}: Usuário com ID {inserido_por_id} não encontrado.")
        except Exception as e:
            print(f"Linha {index + 1}: Erro ao importar: {e}")

    print("Importação concluída!")
