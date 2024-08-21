from django.db import models
from Schedules.models import Schedules
from Products.models import Products

class PaymentTypes(models.Model):

    payment_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'{self.payment_name}'

    class Meta:
        verbose_name = 'Pagamento Vitalize'
        verbose_name_plural = 'Pagamentos Vitalize'


class Sales(models.Model):

    schedule = models.ForeignKey(Schedules, verbose_name='Agendamento', on_delete=models.DO_NOTHING)

    product = models.ManyToManyField(Products, verbose_name="Produto")

    payment = models.ManyToManyField(PaymentTypes, verbose_name="Tipo de Pagamento")

    total_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False, verbose_name='Preço'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Venda nº {self.pk}'

    class Meta:
        verbose_name = 'Venda Vitalize'
        verbose_name_plural = 'Vendas Vitalize'