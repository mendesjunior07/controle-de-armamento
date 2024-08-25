# Generated by Django 5.1 on 2024-08-25 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cautelaarmamento', '0002_alter_vtr_chassi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Armas',
            fields=[
                ('numero_ordem', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=100)),
                ('calibre', models.CharField(max_length=10)),
                ('ct', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_arma', models.CharField(max_length=50)),
                ('numero_pmma', models.CharField(blank=True, max_length=50, null=True)),
                ('localizacao', models.CharField(max_length=100)),
                ('estado_conservacao', models.CharField(max_length=50)),
                ('grupo_responsavel', models.CharField(blank=True, max_length=50, null=True)),
                ('processo', models.CharField(blank=True, max_length=100, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moto',
            fields=[
                ('numero_ordem', models.AutoField(primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=100)),
                ('placa', models.CharField(max_length=10)),
                ('chassi', models.CharField(max_length=50)),
                ('ano', models.CharField(max_length=4)),
                ('proc', models.CharField(max_length=100)),
                ('fornec', models.CharField(blank=True, max_length=100, null=True)),
                ('aparencia_visual', models.CharField(max_length=50)),
                ('destino', models.CharField(max_length=50)),
                ('situacao', models.CharField(max_length=50)),
                ('localizacao', models.CharField(blank=True, max_length=100, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolicialMilitar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=255)),
                ('numero_identificacao', models.CharField(max_length=50, unique=True)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('data_nascimento', models.DateField()),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('patente', models.CharField(max_length=50)),
                ('unidade', models.CharField(max_length=100)),
                ('data_ingresso', models.DateField()),
                ('lotacao_atual', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo'), ('reserva', 'Reserva'), ('reformado', 'Reformado')], default='ativo', max_length=20)),
                ('observacoes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Policial Militar',
                'verbose_name_plural': 'Policiais Militares',
                'ordering': ['nome_completo'],
            },
        ),
    ]
