# Generated by Django 5.0.4 on 2024-08-21 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_alter_products_price'),
        ('Sales', '0004_alter_sales_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='product',
            field=models.ManyToManyField(blank=True, to='Products.products', verbose_name='Produto'),
        ),
    ]
