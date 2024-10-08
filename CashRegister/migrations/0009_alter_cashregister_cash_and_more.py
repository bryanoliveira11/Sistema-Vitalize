# Generated by Django 5.0.4 on 2024-09-23 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0008_alter_cashregister_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='cash',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Valor do Caixa (R$)'),
        ),
        migrations.AlterField(
            model_name='cashregister',
            name='close_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Data de fechamento'),
        ),
    ]
