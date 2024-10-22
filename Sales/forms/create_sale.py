from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django_select2 import forms as s2forms

from Products.models import Products
from Sales.models import PaymentTypes, Sales
from Schedules.models import Schedules

User = get_user_model()


class ScheduleCustomS2ChoiceWidget(s2forms.ModelSelect2Widget):
    def label_from_instance(self, obj: Schedules):
        return f'Agendamento Nº{obj.pk} - {obj.user} - R$ {obj.total_price}'

    def result_from_instance(self, obj: Schedules, request):
        return {
            'id': obj.pk,
            'text': self.label_from_instance(obj),
            'price': obj.total_price,
        }


class ProductsCustomS2MultipleWidget(s2forms.ModelSelect2MultipleWidget):
    def label_from_instance(self, obj: Products):
        return f'{obj.product_name} - R$ {obj.price}'

    def result_from_instance(self, obj: Products, request):
        return {
            'id': obj.pk,
            'text': self.label_from_instance(obj),
            'text_no_price': obj.product_name,
            'price': obj.price,
            'slug': obj.slug,
            'image': obj.cover_path.url,
        }


class CreateSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('schedule'),
            Field('products'),
            HTML('''
                <div class="table-responsive">
                <table class="table table-bordered
                select-products" id="selected-products-table">
                <thead class="thead-light">
                  <tr>
                    <th scope="col">Imagem</th>
                    <th scope="col">Produto</th>
                    <th scope="col">Quantidade</th>
                    <th scope="col">Preço</th>
                  </tr>
                </thead>
                  <tbody id="products-table-body"></tbody>
                </table>
                </div>
            '''),
            Field('payment_type'),
        )

    def validate_sale(self):
        schedule = self.cleaned_data.get('schedule')
        products = self.cleaned_data.get('products')

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

    schedule = forms.ModelChoiceField(
        queryset=Schedules.objects.filter(
            status=True).order_by('-pk').select_related('user'),
        label='Agendamento',
        help_text='Selecionar um Agendamento (Caso Necessário).',
        required=False,
        widget=ScheduleCustomS2ChoiceWidget(
            model=Schedules,
            queryset=Schedules.objects.filter(
              status=True).order_by('-pk').select_related('user'),
            search_fields=[
                'user__email__icontains',
                'pk__icontains',
                'total_price__icontains',
                'schedule_date__icontains',
            ],
            max_results=10,
            attrs={
                'data-placeholder': 'Buscar por E-mail, Data ou Preço',
                'selectionCssClass': 'form-control',
                'data-language': 'pt-BR',
            },
        )
    )

    products = forms.ModelMultipleChoiceField(
        label='Selecionar Produtos',
        queryset=Products.objects.filter(is_active=True).select_related(
            'product_category'
        ).order_by('-pk'),
        required=False,
        widget=ProductsCustomS2MultipleWidget(
            model=Products,
            queryset=Products.objects.filter(is_active=True).select_related(
                'product_category'
            ).order_by('-pk'),
            search_fields=[
                'product_name__icontains',
                'product_category__category_name__icontains',
            ],
            max_results=10,
            attrs={
                'data-placeholder': 'Buscar por Nome ou Categoria',
                'selectionCssClass': 'form-control',
                'data-language': 'pt-BR',
            },
        )
    )

    payment_type = forms.ModelChoiceField(
        queryset=PaymentTypes.objects.filter(
            is_active=True,
        ).order_by('-pk'),
        label='Tipo de Pagamento',
        required=True,
        help_text=mark_safe(
            '''
          <a href="/admin/Sales/paymenttypes/add/" target="_blank"
          class="add-icon" title="Adicionar Forma de Pagamento">
          <i class="fa-solid fa-circle-plus"></i>
          </a>
            '''
        ),
    )

    def clean(self, *args, **kwargs):
        self.validate_sale()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
