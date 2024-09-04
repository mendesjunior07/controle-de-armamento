# Generated by Django 5.1 on 2024-09-04 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Policial',
            fields=[
                ('nome_completo', models.CharField(max_length=255)),
                ('nome_guerra', models.CharField(blank=True, max_length=255, null=True)),
                ('posto_graduacao', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('rgpm', models.CharField(max_length=20, unique=True)),
                ('lotacao', models.CharField(max_length=255)),
                ('data_nascimento', models.DateField()),
                ('inclusao', models.DateField(auto_now_add=True)),
                ('restricao', models.BooleanField(default=False)),
                ('cpf', models.CharField(max_length=14, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('situacao', models.CharField(choices=[('disponivel', 'Disponível'), ('indisponivel', 'Indisponível'), ('em_manutencao', 'Em manutenção')], max_length=20)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='cautelaarmamento.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='CautelaDeArmamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.DateTimeField(auto_now_add=True)),
                ('data', models.DateField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.categoria')),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policial')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.subcategoria')),
            ],
        ),
    ]
