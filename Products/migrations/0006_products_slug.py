# Generated by Django 5.0.4 on 2024-09-02 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_alter_products_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, default='', unique=True),
        ),
    ]
