from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import ValidationError

from Products.models import Products
from Sales.models import PaymentTypes, Sales
from Schedules.models import Schedules


class CreateSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('schedule'),
            Field('products'),
            Field('payment_types'),
        )

    def validate_sale(self):
        schedules = self.cleaned_data['schedules']
        products = self.cleaned_data['products']

        print(schedules, products)

    class Meta:
        model = Sales
        fields = ['schedule', 'products', 'payment_types']

    schedule = forms.ModelChoiceField(
        queryset=Schedules.objects.filter(status=True),
        label='Agendamento',
        help_text='Selecionar Agendamento (Caso haja Algum).',
        required=False,
    )

    products = forms.ModelMultipleChoiceField(
        queryset=Products.objects.filter(
            is_active=True,
        ).order_by('-pk'),
        label='Produtos Disponíveis',
        help_text='''Se estiver em um Computador segure a tecla CTRL
          para selecionar mais de um Produto.''',
        required=False,
    )

    payment_types = forms.ModelMultipleChoiceField(
        queryset=PaymentTypes.objects.filter(
            is_active=True,
        ).order_by('-pk'),
        label='Tipos de Pagamento',
        help_text='''Se estiver em um Computador segure a tecla CTRL
          para selecionar mais de um Tipo de Pagamento.''',
        required=True,
    )

    def clean(self, *args, **kwargs):
        self.validate_sale()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
