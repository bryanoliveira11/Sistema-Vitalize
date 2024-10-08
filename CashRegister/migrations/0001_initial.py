# Generated by Django 5.0.4 on 2024-08-21 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Valor')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
            ],
            options={
                'verbose_name': 'Sangria Vitalize',
                'verbose_name_plural': 'Sangrias Vitalize',
            },
        ),
        migrations.CreateModel(
            name='CashRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
                ('is_open', models.BooleanField(default=True)),
                ('open_date', models.DateTimeField(auto_now_add=True, verbose_name='Data de Abertura')),
                ('close_date', models.DateTimeField(verbose_name='Data de fechamento')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('cash_out', models.ManyToManyField(to='CashRegister.cashout', verbose_name='Sangria')),
            ],
            options={
                'verbose_name': 'Caixa Vitalize',
                'verbose_name_plural': 'Caixas Vitalize',
            },
        ),
    ]
