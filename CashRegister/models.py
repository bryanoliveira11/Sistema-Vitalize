from datetime import datetime

from django.db import models
from django.forms import ValidationError

from Sales.models import Sales


class CashRegister(models.Model):
    sales = models.ManyToManyField(Sales, verbose_name='Venda', blank=True)
    cash = models.DecimalField(
        max_digits=10, decimal_places=2, null=False,
        blank=False, verbose_name='Valor do Caixa (R$)', editable=False,
    )
    is_open = models.BooleanField(
        default=True, verbose_name='Aberto/Fechado',
        help_text='Marque para Abrir o Caixa. \
        Desmarque para Fechar. Um Caixa Fechado não Poderá ser Editado.'
    )
    open_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Abertura'
    )
    close_date = models.DateTimeField(
        verbose_name='Data de fechamento',
        null=True, blank=True, editable=False,
    )
    updated_date = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em'
    )

    def __str__(self):
        return f'Caixa Nº {self.pk} - {self.open_date}'

    def save(self, *args, **kwargs):
        if not self.cash:
            self.cash = 0

        if not self.is_open:
            self.close_date = datetime.now()

        super().save(*args, **kwargs)

    def update_total_price(self, amount, operation:str='add'):
        if operation == 'add':
            self.cash += amount
        elif operation == 'remove':
            self.cash -= amount
        self.save(update_fields=['cash'])

    class Meta:
        verbose_name = 'Caixa Vitalize'
        verbose_name_plural = 'Caixas Vitalize'


class CashOut(models.Model):
    value = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Valor (R$)'
    )
    cashregister = models.ForeignKey(
      CashRegister, on_delete=models.PROTECT,
      verbose_name='Caixa',
      )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Sangria nº {self.pk} - {self.cashregister}'

    def clean(self) -> None:
        cleaned_data = super().clean()
        errors = {}

        if self.value is None or float(self.value) <= 0:
            errors['value'] = 'Digite um Número Positivo.'

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    class Meta:
        verbose_name = 'Sangria Vitalize'
        verbose_name_plural = 'Sangrias Vitalize'
