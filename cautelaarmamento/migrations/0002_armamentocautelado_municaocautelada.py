# Generated by Django 5.1 on 2024-09-10 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cautelaarmamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArmamentoCautelado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cautela', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.categoria')),
                ('cautela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='armamentos', to='cautelaarmamento.cauteladearmamento')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.subcategoria')),
            ],
        ),
        migrations.CreateModel(
            name='MunicaoCautelada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('data_cautela', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.categoriamunicao')),
                ('cautela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municoes', to='cautelaarmamento.cauteladearmamento')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.subcategoriamunicao')),
            ],
        ),
    ]
