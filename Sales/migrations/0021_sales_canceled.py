# Generated by Django 5.0.4 on 2024-10-09 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0020_alter_saleitem_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='canceled',
            field=models.BooleanField(default=False, verbose_name='Venda Cancelada'),
        ),
    ]