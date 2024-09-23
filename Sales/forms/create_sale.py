from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from Products.models import Products
from Sales.models import PaymentTypes, Sales
from Schedules.models import Schedules

User = get_user_model()


class SchedulesChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: Schedules):
        return f"{obj} - R${obj.total_price:.2f}"


class ProductsMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj: Products):
        return f"{obj.product_name} - \
          {obj.product_category} - R${obj.price:.2f}"


class CreateSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('users'),
            Field('schedule'),
            Field('products'),
            Field('payment_types'),
        )

    def validate_sale(self):
        schedule = self.cleaned_data['schedule']
        products = self.cleaned_data['products']

        if schedule is None and not products:
            self._my_errors['schedule'].append(
                'A Venda deve ter ao menos um Agendamento ou Produto.'
            )
            self._my_errors['products'].append(
                'A Venda deve ter ao menos um Agendamento ou Produto.'
            )

    class Meta:
        model = Sales
        fields = ['schedule', 'products', 'payment_types']

    schedule = SchedulesChoiceField(
        queryset=Schedules.objects.filter(status=True).select_related('user'),
        label='Agendamento',
        help_text='Selecionar um Agendamento (Caso Necessário).',
        required=False,
    )

    products = ProductsMultipleChoiceField(
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
