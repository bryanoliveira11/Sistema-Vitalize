# Generated by Django 5.0.4 on 2024-10-09 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logs', '0002_alter_vitalizelogs_options_alter_vitalizelogs_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitalizelogs',
            name='object_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
