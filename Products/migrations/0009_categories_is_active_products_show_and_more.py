# Generated by Django 5.0.4 on 2024-09-17 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0008_alter_products_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo/Inativo'),
        ),
        migrations.AddField(
            model_name='products',
            name='show',
            field=models.BooleanField(default=True, verbose_name='Mostrar na Vitrine'),
        ),
        migrations.AlterField(
            model_name='products',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo/Inativo'),
        ),
    ]
