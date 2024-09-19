# Generated by Django 5.1 on 2024-09-18 18:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cautelaarmamento', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cauteladearmamento',
            name='armeiro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cauteladearmamento',
            name='hora_cautela',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
