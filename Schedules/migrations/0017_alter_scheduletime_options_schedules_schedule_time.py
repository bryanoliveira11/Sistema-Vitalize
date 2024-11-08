# Generated by Django 5.0.4 on 2024-11-07 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedules', '0016_scheduletime_alter_schedules_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheduletime',
            options={'verbose_name': 'Horário Vitalize', 'verbose_name_plural': 'Horários Vitalize'},
        ),
        migrations.AddField(
            model_name='schedules',
            name='schedule_time',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Schedules.scheduletime', verbose_name='Horário Agendado'),
            preserve_default=False,
        ),
    ]