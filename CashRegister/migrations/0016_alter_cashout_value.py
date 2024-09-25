# Generated by Django 5.0.4 on 2024-09-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0015_alter_cashregister_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashout',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Valor (R$)'),
        ),
    ]
