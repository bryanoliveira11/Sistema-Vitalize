# Generated by Django 5.0.4 on 2024-09-23 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0008_alter_sales_schedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='payment',
            new_name='payment_types',
        ),
    ]