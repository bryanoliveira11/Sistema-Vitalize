from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Services(models.Model):
    service_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )
    description = models.CharField(
        max_length=150, null=False, blank=False, verbose_name='Descrição'
    )
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Preço (R$)'
    )
    cover_path = models.ImageField(
        upload_to='services/%Y/%m/%d/', null=False,
        blank=False, verbose_name='Imagem'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'{self.service_name}'

    class Meta:
        verbose_name = 'Serviço Vitalize'
        verbose_name_plural = 'Serviços Vitalize'


class Schedules(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Usuario', null=True, on_delete=models.SET_NULL
    )
    service = models.ManyToManyField(Services, verbose_name="Serviço")
    schedule_date = models.DateTimeField(
        null=False, blank=False, verbose_name='Data e Hora'
    )
    status = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Agendamento nº {self.pk}'

    class Meta:
        verbose_name = 'Agendamento Vitalize'
        verbose_name_plural = 'Agendamentos Vitalize'
