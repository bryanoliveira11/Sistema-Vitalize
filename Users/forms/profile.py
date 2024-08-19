from collections import defaultdict

from crispy_forms.bootstrap import Field, PrependedAppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField

from utils.django_forms import add_attr, add_placeholder

User = get_user_model()


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_placeholder(self.fields['first_name'], 'Digite seu Nome')
        add_placeholder(self.fields['last_name'], 'Digite seu Sobrenome')
        add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
        add_attr(self.fields['email'], 'class', 'span-2')
        add_placeholder(self.fields['phone_number'], 'Digite seu Telefone')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            PrependedAppendedText('email', mark_safe(
                '<i class="fa-solid fa-envelope"></i>')
            ),
            PrependedAppendedText('phone_number', mark_safe(
                '<i class="fa-solid fa-phone"></i>')
            ),
        )

    def validate_email(self, instance=None):
        email = self.cleaned_data.get('email')
        email_database = User.objects.filter(email__iexact=email).first()

        if instance and instance.email == email:
            return email

        if email_database and instance:
            if email_database.pk != instance.pk:
                self._my_errors['email'].append(
                    'Este E-mail Está em Uso.'
                )
                return email
        return email

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number'
        ]

    first_name = forms.CharField(
        label='Nome', max_length=150,
        error_messages={
            'required': 'Digite seu Nome.',
            'max_length': 'O Nome deve ter no Máximo 150 Dígitos.',
        }
    )

    last_name = forms.CharField(
        label='Sobrenome', max_length=150,
        error_messages={
            'required': 'Digite seu Sobrenome.',
            'max_length': 'O Sobrenome deve ter no Máximo 150 Dígitos.',
        }
    )

    email = forms.EmailField(
        label='E-mail',
        help_text=('E-mail Precisa ser Válido.'),
        error_messages={
            'required': 'Digite seu E-mail.',
        },
    )

    phone_number = PhoneNumberField(
        label='Telefone ou Celular', max_length=15,
        help_text=mark_safe(
            '''
          <p class="helptext-p">&#x2022; Somente Números</p>
          <p class="helptext-p">&#x2022; Informe o DDD</p>
            '''
        ),
        error_messages={
            'required': 'Digite seu Telefone.',
            'invalid': 'Digite um Telefone Válido (exemplo : 1123456789).',
        },
        region='BR',
    )

    def clean_email(self):
        return self.validate_email(instance=self.instance)

    def clean(self, *args, **kwargs):
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)
