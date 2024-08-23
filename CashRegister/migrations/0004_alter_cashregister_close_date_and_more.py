# Generated by Django 5.0.4 on 2024-08-21 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0003_alter_cashregister_cash'),
        ('Sales', '0004_alter_sales_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='close_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de fechamento'),
        ),
        migrations.AlterField(
            model_name='cashregister',
            name='sale',
            field=models.ManyToManyField(blank=True, null=True, to='Sales.sales', verbose_name='Venda'),
        ),
    ]