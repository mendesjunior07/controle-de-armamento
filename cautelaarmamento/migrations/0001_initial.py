# Generated by Django 5.1 on 2024-08-21 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vtr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(choices=[('TOYOTA', 'Toyota'), ('HONDA', 'Honda'), ('FORD', 'Ford'), ('CHEVROLET', 'Chevrolet')], max_length=50)),
                ('modelo', models.CharField(max_length=100)),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('chassi', models.CharField(max_length=50, unique=True)),
                ('ano', models.IntegerField()),
                ('procedencia', models.CharField(max_length=100)),
                ('fornecedor', models.CharField(max_length=100)),
                ('aparencia_visual', models.TextField()),
                ('destino', models.CharField(max_length=100)),
                ('situacao', models.CharField(choices=[('DISPONIVEL', 'Disponível'), ('EM_USO', 'Em uso'), ('MANUTENCAO', 'Manutenção'), ('BAIXADO', 'Baixado')], max_length=50)),
                ('localizacao', models.CharField(max_length=100)),
                ('observacao', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
