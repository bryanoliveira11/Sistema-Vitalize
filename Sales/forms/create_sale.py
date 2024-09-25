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


class SchedulesCustomWidget(forms.Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-price"] = value.instance.total_price
        return option


class SchedulesChoiceField(forms.ModelChoiceField):
    widget = SchedulesCustomWidget

    def label_from_instance(self, obj: Schedules):
        return f"{obj} - R${obj.total_price:.2f}"


class ProductsCustomWidget(forms.SelectMultiple):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-price"] = value.instance.price
        return option


class ProductsMultipleChoiceField(forms.ModelMultipleChoiceField):
    widget = ProductsCustomWidget

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
            Field('schedule'),
            Field('products'),
            Field('payment_type'),
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
        fields = ['schedule', 'products', 'payment_type']

    schedule = SchedulesChoiceField(
        queryset=Schedules.objects.filter(
            status=True).order_by('-pk').select_related('user'),
        label='Agendamento',
        help_text='Selecionar um Agendamento (Caso Necessário).',
        required=False,
    )

    products = ProductsMultipleChoiceField(
        queryset=Products.objects.filter(
            is_active=True,
        ).order_by('-pk').select_related('product_category'),
        label='Produtos Disponíveis',
        help_text='''Se estiver em um Computador segure a tecla CTRL
          para selecionar mais de um Produto.''',
        required=False,
    )

    payment_type = forms.ModelChoiceField(
        queryset=PaymentTypes.objects.filter(
            is_active=True,
        ).order_by('-pk'),
        label='Tipos de Pagamento',
        required=True,
    )

    def clean(self, *args, **kwargs):
        self.validate_sale()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
