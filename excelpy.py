import pandas as pd
from django.core.management.base import BaseCommand
from cautelaarmamento.models import Subcategoria  # Substitua pelo nome da sua app
from django.contrib.auth.models import User  # Assumindo que o usuário já está registrado no sistema

class Command(BaseCommand):
    help = 'Importa dados do CSV para o modelo Subcategoria'

    def handle(self, *args, **kwargs):
        # Carrega o arquivo CSV
        csv_file_path = '/mnt/data/pistolas_taurus.csv'
        data = pd.read_csv(csv_file_path)

        # Itera sobre as linhas do CSV e cria instâncias de Subcategoria
        for index, row in data.iterrows():
            subcategoria = Subcategoria(
                marca=row.get('marca'),
                modelo=row.get('modelo'),
                placa=row.get('placa'),
                chassi=row.get('chassi'),
                ano=row.get('ano'),
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
                data_vencimento=row.get('data_vencimento'),
                observacao=row.get('observacao'),
                categoria_id=row.get('categoria_id'),  # Assumindo que já há uma categoria associada
                inserido_por=User.objects.get(id=1)  # Altere para o ID correto do usuário
            )

            # Salva a instância no banco de dados
            subcategoria.save()

        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
