# Generated by Django 5.0.4 on 2024-08-14 15:04

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_vitalizeuser_is_client_alter_vitalizeuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitalizeuser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]