from django.db import models

from Products.models import Products
from Schedules.models import Schedules


class PaymentTypes(models.Model):
    payment_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Ativo/Inativo',
        help_text='Marque Essa Caixa para Ativar esse Tipo de Pagamento. '
        'Desmarque para Inativar.',
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
        verbose_name = 'Tipo de Pagamento Vitalize'
        verbose_name_plural = 'Tipos de Pagamento Vitalize'


class Sales(models.Model):
    schedule = models.ForeignKey(
        Schedules, verbose_name='Agendamento',
        on_delete=models.PROTECT, null=True, blank=True
    )
    products = models.ManyToManyField(
        Products, verbose_name="Produto(s)", blank=True
    )
    payment_types = models.ManyToManyField(
        PaymentTypes, verbose_name="Tipo de Pagamento"
    )
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Preço Total (R$)'
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
