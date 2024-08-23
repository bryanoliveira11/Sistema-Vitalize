# Generated by Django 5.0.4 on 2024-08-21 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_alter_products_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Preço (R$)'),
        ),
    ]