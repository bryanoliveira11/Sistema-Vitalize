# Generated by Django 5.0.4 on 2024-08-14 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0012_vitalizeuser_groups_vitalizeuser_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vitalizeuser',
            name='is_client',
        ),
    ]