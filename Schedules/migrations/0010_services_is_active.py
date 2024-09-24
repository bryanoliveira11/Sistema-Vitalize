# Generated by Django 5.0.4 on 2024-09-23 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedules', '0009_rename_service_schedules_services_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Marque Essa Caixa para Ativar esse Serviço. Desmarque para Inativar.', verbose_name='Ativo/Inativo'),
        ),
    ]