# Generated by Django 5.0.4 on 2024-08-21 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Products', '0001_initial'),
        ('Schedules', '0002_services_alter_schedules_options_schedules_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_name', models.CharField(max_length=50, verbose_name='Nome')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
            ],
            options={
                'verbose_name': 'Pagamento Vitalize',
                'verbose_name_plural': 'Pagamentos Vitalize',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Preço')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('payment', models.ManyToManyField(to='Sales.paymenttypes', verbose_name='Tipo de Pagamento')),
                ('product', models.ManyToManyField(to='Products.products', verbose_name='Produto')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Schedules.schedules', verbose_name='Agendamento')),
            ],
            options={
                'verbose_name': 'Venda Vitalize',
                'verbose_name_plural': 'Vendas Vitalize',
            },
        ),
    ]
