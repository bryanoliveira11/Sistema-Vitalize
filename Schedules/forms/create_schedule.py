from collections import defaultdict

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from Schedules.models import (ScheduleDateTime, Schedules, ScheduleTime,
                              Services)
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
            'description': obj.description,
            'price': obj.price,
            'image': obj.cover_path.url,
        }


class ScheduleTimeCustomS2ChoiceWidget(s2forms.ModelSelect2Widget):
    def label_from_instance(self, obj: ScheduleTime):
        return obj.time


class ScheduleSelectServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                    <th scope="col">Serviço</th>
                    <th scope="col">Descrição</th>
                    <th scope="col">Preço</th>
                  </tr>
                </thead>
                  <tbody id="services-table-body"></tbody>
                </table>
                </div>
            '''),
        )

    class Meta:
        model = Schedules
        fields = ['services']

    services = forms.ModelMultipleChoiceField(
        queryset=Services.objects.filter(
            is_active=True,
        ).order_by('-pk'),
        label='Serviços',
        help_text='Escolha os Serviços Desejados.',
        required=True,
        widget=ServicesCustomS2MultipleWidget(
            model=Services,
            search_fields=[
                'service_name__icontains',
            ],
            max_results=10,
            attrs={
                'data-placeholder': 'Buscar por Nome do Serviço',
                'selectionCssClass': 'form-control',
                'data-language': 'pt-BR',
                'data-minimum-input-length': 0,
            },
        )
    )

    def clean(self, *args, **kwargs):

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)


class ScheduleSelectDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['schedule_date'], 'class', 'datetime-input')
        add_placeholder(self.fields['schedule_date'], 'dd-mm-YYYY')
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Field('schedule_date'))

    class Meta:
        model = Schedules
        fields = ['schedule_date']

    schedule_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        label='Data do Agendamento',
        required=True,
        help_text='Selecione a Data do Agendamento',
    )

    def clean(self, *args, **kwargs):

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)


class ScheduleSelectTimeForm(forms.ModelForm):
    def __init__(self, selected_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Field('schedule_time'))
        selected_times = ScheduleDateTime.objects.filter(
            date=selected_date
        )
        selected_time_ids = selected_times.values_list('time', flat=True)
        self.fields['schedule_time'].queryset = ScheduleTime.objects.filter(
            is_active=True
        ).exclude(id__in=selected_time_ids).order_by('time')

    class Meta:
        model = Schedules
        fields = ['schedule_time']

    schedule_time = forms.ModelChoiceField(
        queryset=ScheduleTime.objects.none(),
        label='Horário do Agendamento',
        help_text='Selecione o Horário do Agendamento',
        required=True,
        widget=ScheduleTimeCustomS2ChoiceWidget(
            model=ScheduleTime,
            search_fields=[
                'time__icontains',
            ],
            max_results=10,
            attrs={
                'data-placeholder': 'Buscar por Horário',
                'selectionCssClass': 'form-control',
                'data-language': 'pt-BR',
                'data-minimum-input-length': 0,
            },
        )
    )

    def clean(self, *args, **kwargs):

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
