# Generated by Django 5.1 on 2024-10-13 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='perfil.clientprofile'),
        ),
    ]
