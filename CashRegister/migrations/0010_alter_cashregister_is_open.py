# Generated by Django 5.0.4 on 2024-09-23 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0009_alter_cashregister_cash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='is_open',
            field=models.BooleanField(default=True, editable=False, verbose_name='Aberto/Fechado'),
        ),
    ]
