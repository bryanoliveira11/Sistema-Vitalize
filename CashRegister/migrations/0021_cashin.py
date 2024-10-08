# Generated by Django 5.0.4 on 2024-10-03 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0020_cashout_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Valor (R$)')),
                ('description', models.CharField(max_length=150, verbose_name='Descrição de Adição')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('cashregister', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CashRegister.cashregister', verbose_name='Caixa')),
            ],
            options={
                'verbose_name': 'Adição de Valor Vitalize',
                'verbose_name_plural': 'Adição de Valores Vitalize',
            },
        ),
    ]
