from django.db import models
from django.forms import ValidationError

from Sales.models import Sales


class CashOut(models.Model):
    value = models.DecimalField(
        max_digits=5, decimal_places=2, null=False,
        blank=False, verbose_name='Valor (R$)'
    )
    description = models.CharField(
        max_length=100, null=False, blank=False, verbose_name='Descrição'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Sangria nº {self.pk} - {self.description}'

    def clean(self) -> None:
        cleaned_data = super().clean()
        errors = {}

        if float(self.value) <= 0:
            errors['value'] = 'Digite um Número Positivo.'

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    class Meta:
        verbose_name = 'Sangria Vitalize'
        verbose_name_plural = 'Sangrias Vitalize'


class CashRegister(models.Model):
    sales = models.ManyToManyField(Sales, verbose_name='Venda', blank=True)
    cash_out = models.ManyToManyField(
        CashOut, verbose_name='Sangria',
        blank=True, help_text='Faça uma Sangria no Caixa '
        'Escolhendo uma Opção e Salvando.'
    )
    cash = models.DecimalField(
        max_digits=10, decimal_places=2, null=False,
        blank=False, verbose_name='Valor do Caixa (R$)', editable=False,
    )
    is_open = models.BooleanField(
        default=True, verbose_name='Aberto/Fechado', editable=False
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
        return f'Caixa nº {self.pk} - {self.open_date}'

    def save(self, *args, **kwargs):
        if not self.cash:
            self.cash = 0

        saved = super().save(*args, **kwargs)
        return saved

    class Meta:
        verbose_name = 'Caixa Vitalize'
        verbose_name_plural = 'Caixas Vitalize'
