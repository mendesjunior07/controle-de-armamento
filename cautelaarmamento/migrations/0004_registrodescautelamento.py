# Generated by Django 5.1 on 2024-09-23 12:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cautelaarmamento', '0003_registrocautelacompleta'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('data_descautelamento', models.DateField(auto_now_add=True)),
                ('hora_descautelamento', models.TimeField(auto_now_add=True)),
                ('armeiro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrodescautelamento_armeiro', to=settings.AUTH_USER_MODEL)),
                ('armeiro_descautela', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrodescautelamento_armeiro_descautela', to=settings.AUTH_USER_MODEL)),
                ('policial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cautelaarmamento.policial')),
            ],
        ),
    ]
