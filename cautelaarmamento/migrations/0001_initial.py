# Generated by Django 5.1 on 2024-08-28 15:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Armas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('numero_de_serie', models.CharField(max_length=100, unique=True)),
                ('disponivel', models.CharField(choices=[('Disponivel', 'Disponível'), ('Indisponivel', 'Indisponível'), ('verificar', 'Verificar'), ('manutencao', 'Manutenção'), ('quebrada', 'Quebrada')], default='Disponivel', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PolicialMilitar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('matricula', models.CharField(max_length=50, unique=True)),
                ('patente', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vtr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('modelo', models.CharField(max_length=100)),
                ('disponivel', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cautela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cautela', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_descautela', models.DateTimeField(blank=True, null=True)),
                ('armamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.armas')),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policialmilitar')),
            ],
        ),
    ]
