# Generated by Django 5.1 on 2024-10-12 10:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaMunicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DescautelasCa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_cautela', models.DateTimeField()),
                ('policial', models.CharField(max_length=100)),
                ('tipo_servico', models.CharField(max_length=50)),
                ('categoria_armamento', models.CharField(max_length=50, null=True)),
                ('subcategoria_armamento', models.CharField(max_length=50, null=True)),
                ('categoria_municao', models.CharField(max_length=50, null=True)),
                ('subcategoria_municao', models.CharField(max_length=50, null=True)),
                ('quantidade_municao', models.IntegerField()),
                ('situacao_armamento', models.CharField(max_length=50)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('armeiro', models.CharField(max_length=100)),
                ('armeiro_descautela', models.CharField(max_length=100)),
                ('data_descautelamento', models.DateField()),
                ('hora_descautelamento', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Policial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=100)),
                ('nome_guerra', models.CharField(blank=True, max_length=50, null=True)),
                ('posto_graduacao', models.CharField(max_length=50)),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('rgpm', models.CharField(max_length=20, unique=True)),
                ('lotacao', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=14, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroCautelaCompleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_servico', models.CharField(max_length=20)),
                ('categoria_armamento', models.CharField(blank=True, max_length=100, null=True)),
                ('subcategoria_armamento', models.CharField(blank=True, max_length=100, null=True)),
                ('categoria_municao', models.CharField(blank=True, max_length=100, null=True)),
                ('subcategoria_municao', models.CharField(blank=True, max_length=100, null=True)),
                ('quantidade_municao', models.PositiveIntegerField(default=0)),
                ('armeiro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policial')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroDescautelamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_cautela', models.DateTimeField()),
                ('tipo_servico', models.CharField(max_length=100)),
                ('categoria_armamento', models.CharField(blank=True, max_length=100, null=True)),
                ('subcategoria_armamento', models.CharField(blank=True, max_length=100, null=True)),
                ('categoria_municao', models.CharField(blank=True, max_length=100, null=True)),
                ('subcategoria_municao', models.CharField(blank=True, max_length=100, null=True)),
                ('quantidade_municao', models.PositiveIntegerField(default=0)),
                ('situacao_armamento', models.CharField(blank=True, max_length=20, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('data_descautelamento', models.DateField(auto_now_add=True)),
                ('hora_descautelamento', models.TimeField(auto_now_add=True)),
                ('armeiro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrodescautelamento_armeiro', to=settings.AUTH_USER_MODEL)),
                ('armeiro_descautela', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrodescautelamento_armeiro_descautela', to=settings.AUTH_USER_MODEL)),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policial')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('marca', models.CharField(blank=True, max_length=100, null=True)),
                ('modelo', models.CharField(blank=True, max_length=100, null=True)),
                ('cal', models.CharField(blank=True, max_length=50, null=True)),
                ('ct', models.CharField(blank=True, max_length=50, null=True)),
                ('num_arma', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Nº ARMA')),
                ('num_pmma', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nº PMMA')),
                ('localizacao', models.CharField(blank=True, max_length=200, null=True)),
                ('tombo', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_conservacao', models.CharField(blank=True, max_length=100, null=True, verbose_name='EST. DE CONSERVAÇÃO')),
                ('gr', models.CharField(blank=True, max_length=50, null=True, verbose_name='G.R')),
                ('proc', models.CharField(blank=True, max_length=100, null=True, verbose_name='PROC')),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='OBSERVAÇÃO')),
                ('situacao', models.CharField(choices=[('disponivel', 'Disponível'), ('cautelada', 'Cautelada'), ('extraviado', 'Extraviado'), ('roubado', 'Roubado'), ('quebrado', 'Quebrado'), ('furado', 'Furado'), ('disparado', 'Disparado')], default='disponivel', max_length=20)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias_armamento', to='cautelaarmamento.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='CautelaDeArmamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_servico', models.CharField(choices=[('operacional', 'Operacional'), ('administrativo', 'Administrativo')], max_length=20)),
                ('hora_cautela', models.DateTimeField(default=django.utils.timezone.now)),
                ('armeiro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.categoria')),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policial')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.subcategoria')),
            ],
        ),
        migrations.CreateModel(
            name='SubcategoriaMunicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('total_de_municoes', models.PositiveIntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='cautelaarmamento.categoriamunicao')),
            ],
        ),
        migrations.CreateModel(
            name='CautelaDeMunicoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.categoriamunicao')),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policial')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.subcategoriamunicao')),
            ],
        ),
    ]
