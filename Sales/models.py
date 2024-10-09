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
        Products, verbose_name='Produto(s)', blank=True
    )
    payment_type = models.ForeignKey(
        PaymentTypes,
        verbose_name='Tipo de Pagamento',
        on_delete=models.PROTECT,
    )
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Preço Total (R$)', editable=False,
    )
    canceled = models.BooleanField(
        default=False, verbose_name='Cancelada',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Venda Nº {self.pk} - {self.total_price} R$'

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = 0
        super().save(*args, **kwargs)

    def update_total_price(self):
        product_total = self.products.aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0
        schedule_total = self.schedule.total_price if self.schedule and \
            self.schedule.total_price is not None else 0
        total = product_total + schedule_total
        Sales.objects.filter(pk=self.pk).update(total_price=total)

    class Meta:
        verbose_name = 'Venda Vitalize'
        verbose_name_plural = 'Vendas Vitalize'


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sales, verbose_name='Venda',
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Products, verbose_name='Produto da Venda',
        on_delete=models.PROTECT,
    )
    quantity = models.IntegerField(
        verbose_name='Quantidade'
    )
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Preço Total (R$)',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Item {self.pk} da Venda {self.sale}'

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Items da Venda'
