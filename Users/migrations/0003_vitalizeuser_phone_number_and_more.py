# Generated by Django 5.0.4 on 2024-05-23 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_vitalizeuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitalizeuser',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=11),
        ),
        migrations.AlterField(
            model_name='vitalizeuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='vitalizeuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='vitalizeuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='vitalizeuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Sobrenome'),
        ),
    ]
