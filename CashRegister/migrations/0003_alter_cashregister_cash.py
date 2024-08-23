# Generated by Django 5.0.4 on 2024-08-21 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='cash',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço (R$)'),
        ),
    ]