from collections import defaultdict

from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from utils.django_forms import add_attr, add_placeholder


class ProductsReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)
        
        add_attr(self.fields['is_active'], 'class', 'select-input')
        add_attr(self.fields['show_in_showcase'], 'class', 'select-input')
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            AppendedText('is_active', mark_safe(
                '<i class="fa-regular fa-check-circle"></i>'),
            ),
            AppendedText('show_in_showcase', mark_safe(
                '<i class="fa-regular fa-eye"></i>'),
            ),
        )

    is_active = forms.ChoiceField(
        choices=[('Todos', 'Todos'), (True, 'Ativo'), (False, 'Inativo')],
        label='Status do Produto',
        required=True,
        help_text='Selecione a listagem por status do produto'
    )

    show_in_showcase = forms.ChoiceField(
        choices=[('Todos', 'Todos'), (True, 'Vitrine'), (False, 'Oculto')],
        label='Exibição',
        required=True,
        help_text='Selecione a listagem por exibição do produto'
    )

    def clean(self, *args, **kwargs):
        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
