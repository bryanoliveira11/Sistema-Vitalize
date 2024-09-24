# Generated by Django 5.0.4 on 2024-09-24 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0014_alter_cashregister_cash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='is_open',
            field=models.BooleanField(default=True, help_text='Marque para Abrir o Caixa.         Desmarque para Fechar. Um Caixa Fechado não Poderá ser Editado.', verbose_name='Aberto/Fechado'),
        ),
    ]