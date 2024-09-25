# Generated by Django 5.0.4 on 2024-09-25 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashRegister', '0017_remove_cashregister_cash_out'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashout',
            name='description',
        ),
        migrations.AddField(
            model_name='cashout',
            name='cashregister',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.PROTECT, to='CashRegister.cashregister', verbose_name='Caixa'),
            preserve_default=False,
        ),
    ]