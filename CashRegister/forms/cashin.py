from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from CashRegister.models import CashRegister
from utils.django_forms import add_placeholder


class CashInForm(forms.Form):
    def __init__(self, instance: CashRegister | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        add_placeholder(self.fields['cash_in'], 'Digite o Valor da Entrada')
        add_placeholder(
            self.fields['description'], 'Digite a Descrição da Entrada'
        )
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('cash_in'),
            Field('description'),
        )
        self.instance = instance

    cash_in = forms.DecimalField(
        label='Valor da Entrada',
        help_text=mark_safe(
            '''
          <p class="helptext-p">&#x2022; Somente Números</p>
          <p class="helptext-p">&#x2022; Valores Maiores que Zero</p>
            '''
        ),
        required=True,
    )

    description = forms.CharField(
        label='Descrição de Entrada',
        required=True,
    )

    def validate_cash_in(self):
        cash_in = self.cleaned_data['cash_in']

        if cash_in <= 0:
            self._my_errors['cash_in'].append(
                'O Valor da Entrada não Pode ser Menor ou Igual a Zero.'
            )

    def clean(self, *args, **kwargs):
        self.validate_cash_in()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
