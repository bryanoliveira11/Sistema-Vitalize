# Generated by Django 5.0.4 on 2024-10-30 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='is_active',
            field=models.BooleanField(default=True, editable=False, verbose_name='Ativo/Inativo'),
        ),
    ]
