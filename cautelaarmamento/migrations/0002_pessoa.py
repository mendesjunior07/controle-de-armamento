# Generated by Django 5.1 on 2024-09-03 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cautelaarmamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
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
    ]
