# Generated by Django 5.1 on 2024-08-27 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cautelaarmamento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policialmilitar',
            name='user',
        ),
    ]
