# Generated by Django 5.0.4 on 2024-09-23 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedules', '0008_alter_schedules_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedules',
            old_name='service',
            new_name='services',
        ),
        migrations.AddField(
            model_name='schedules',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=7, verbose_name='Preço Total (R$)'),
            preserve_default=False,
        ),
    ]