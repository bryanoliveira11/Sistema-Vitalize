# Generated by Django 5.0.4 on 2024-09-04 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0006_products_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.categories', verbose_name='Categoria'),
        ),
    ]
