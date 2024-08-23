# Generated by Django 5.0.4 on 2024-08-21 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0004_alter_cashregister_close_date_and_more'),
        ('Sales', '0004_alter_sales_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='sale',
            field=models.ManyToManyField(blank=True, to='Sales.sales', verbose_name='Venda'),
        ),
    ]