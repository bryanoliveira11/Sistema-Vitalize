# Generated by Django 5.0.4 on 2024-11-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedules', '0018_alter_scheduletime_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduletime',
            name='is_picked',
            field=models.BooleanField(default=True, verbose_name='Em Uso'),
        ),
        migrations.AlterField(
            model_name='scheduletime',
            name='time',
            field=models.TimeField(help_text='Utilize o Formato HH:MM, EX.: 12:30', unique=True, verbose_name='Horário de Agendamento'),
        ),
    ]
