# Generated by Django 5.0.4 on 2024-09-24 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0011_rename_sale_cashregister_sales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='cash',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor do Caixa (R$)'),
        ),
    ]
