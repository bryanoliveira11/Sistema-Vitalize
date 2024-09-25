from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from CashRegister.models import CashRegister
from utils.django_forms import add_placeholder


class CashOutForm(forms.Form):
    def __init__(self, instance: CashRegister | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        add_placeholder(self.fields['cash_out'], 'Digite o Valor da Sangria')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('cash_out'),
        )
        self.instance = instance

    cash_out = forms.DecimalField(
        label='Valor da Sangria',
        help_text=mark_safe(
            '''
          <p class="helptext-p">&#x2022; Somente Números</p>
          <p class="helptext-p">&#x2022; Valores Maiores que Zero</p>
            '''
        ),
        required=True,
    )

    def validate_cash_out(self):
        cash_out = self.cleaned_data['cash_out']
        cashregister = self.instance

        if cash_out <= 0:
            self._my_errors['cash_out'].append(
                'O Valor da Sangria não Pode ser Menor ou Igual a Zero.'
            )

        if cashregister is not None:
            if cash_out > cashregister.cash:
                self._my_errors['cash_out'].append(
                    'O Valor da Sangria não Pode '
                    'ser Maior que o Valor Total do Caixa.'
                )

    def clean(self, *args, **kwargs):
        self.validate_cash_out()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
