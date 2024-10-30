from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from Schedules.models import Services
from Schedules.models import Schedules

from utils.django_forms import add_attr, add_placeholder

User = get_user_model()


class ServicesCustomS2MultipleWidget(s2forms.ModelSelect2MultipleWidget):
    def label_from_instance(self, obj: Services):
        return f'{obj.service_name} - R$ {obj.price}'

    def result_from_instance(self, obj: Services, request):
        return {
            'id': obj.pk,
            'text': self.label_from_instance(obj),
            'text_no_price': obj.service_name,
            'price': obj.price,
            'image': obj.cover_path.url,
        }


class CreateScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['schedule_date'], 'class', 'datetime-input')
        add_placeholder(self.fields['schedule_date'], 'dd-mm-YYYY')
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('services'),
            HTML('''
                <div class="table-responsive">
                <table class="table table-bordered
                select-services" id="selected-services-table">
                <thead class="thead-light">
                  <tr>
                    <th scope="col">Imagem</th>
                    <th scope="col">Produto</th>
                    <th scope="col">Quantidade</th>
                    <th scope="col">Preço</th>
                  </tr>
                </thead>
                  <tbody id="services-table-body"></tbody>
                </table>
                </div>
            '''),
            Field('schedule_date')
        )

    class Meta:
        model = Schedules
        fields = ['services', 'schedule_date']

    services = forms.ModelChoiceField(
        queryset=Services.objects.filter(
            is_active=True).order_by('-pk'),
        label='Agendamento',
        help_text='Selecionar um Agendamento (Caso Necessário).',
        required=False,
        widget=ServicesCustomS2MultipleWidget(
            model=Services,
            queryset=Services.objects.filter(
              is_active=True).order_by('-pk'),
            search_fields=[
                'service_name__icontains'
            ],
            max_results=10,
            attrs={
                'data-placeholder': 'Buscar por Nome do Serviço',
                'selectionCssClass': 'form-control',
                'data-language': 'pt-BR',
                'data-minimum-input-length' : 0
            },
        )
    )

    schedule_date = forms.DateTimeField(
        input_formats=['%d-%m-%Y'],
        label='Data Agendamento',
        required=True,
        help_text='Selecione a Data Agendamento do Agendamento',
    )


    def clean(self, *args, **kwargs):
        self.validate_sale()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
