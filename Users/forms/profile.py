from collections import defaultdict

from crispy_forms.bootstrap import AppendedText, Field, PrependedAppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField

from utils.django_forms import add_attr, add_placeholder, strong_password

User = get_user_model()


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        self._email_changed = False
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
        self._email_changed = True
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


class EditPasswordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_placeholder(self.fields['password2'], 'Confirme sua Senha')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            AppendedText('password', mark_safe(
                '<i class="fa-solid fa-eye"></i>'), css_class='show-password'
            ),
            Field('password2'),
        )

    def validate_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            self._my_errors['password'].append(
                'Senhas Precisam ser Iguais.'
            )
            self._my_errors['password2'].append(
                'Senhas Precisam ser Iguais.'
            )

    class Meta:
        model = User
        fields = ['password']

    password = forms.CharField(
        label='Senha',
        error_messages={
            'required': 'Digite sua Senha.'
        },
        help_text=mark_safe(
            '''
          <p class="helptext-p password">&#x2022; Mínimo de 8 Dígitos</p>
          <p class="helptext-p password">&#x2022; 1x Letra Maiúscula</p>
          <p class="helptext-p password">&#x2022; 1x Letra Mínuscula</p>
          <p class="helptext-p password">&#x2022; 1x Número</p>
            '''
        ),
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        label='Confirmação de Senha',
        error_messages={
            'required': 'Confirme sua Senha.'
        },
        widget=forms.PasswordInput()
    )

    def clean(self, *args, **kwargs):
        self.validate_password()

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)
