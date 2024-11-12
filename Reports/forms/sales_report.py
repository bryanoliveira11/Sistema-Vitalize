from collections import defaultdict

from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from utils.django_forms import add_attr, add_placeholder


class SalesReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        add_attr(self.fields['date_initial'], 'class', 'datetime-input')
        add_attr(self.fields['date_final'], 'class', 'datetime-input')
        add_placeholder(self.fields['date_initial'], 'dd-mm-YYYY')
        add_placeholder(self.fields['date_final'], 'dd-mm-YYYY')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            AppendedText('date_initial', mark_safe(
                '<i class="fa-regular fa-calendar-days"></i>'),
            ),
            AppendedText('date_final', mark_safe(
                '<i class="fa-regular fa-calendar-days"></i>'),
            ),
        )

    date_initial = forms.DateField(
        input_formats=['%d-%m-%Y'],
        label='Data Inicial',
        required=True,
        help_text='Selecione a Data Inicial do Período Desejado',
    )

    date_final = forms.DateField(
        input_formats=['%d-%m-%Y'],
        label='Data Final',
        required=True,
        help_text='Selecione a Data Final do Período Desejado',
    )

    def clean(self, *args, **kwargs):
        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
