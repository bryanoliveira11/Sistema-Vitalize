from collections import defaultdict

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from utils.django_forms import add_attr, add_placeholder, strong_password

User = get_user_model()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_placeholder(self.fields['first_name'], 'Digite seu Nome')
        add_placeholder(self.fields['last_name'], 'Digite seu Sobrenome')
        add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
        add_attr(self.fields['email'], 'class', 'span-2')
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_placeholder(self.fields['password2'], 'Confirme sua Senha')
        add_attr(self.fields['password'], 'class', 'password-help-text-m0')

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
        label=format_html(
            '<i class="fa-solid fa-envelope mr-03"></i> E-mail'
        ),
        help_text=('E-mail Precisa ser Válido.'),
        error_messages={
            'required': 'Digite seu E-mail.',
        },
    )

    password = forms.CharField(
        label=format_html(
            '<i class="fa-solid fa-lock mr-03"></i> Senha'
        ),
        error_messages={
            'required': 'Digite sua Senha.'
        },
        help_text=format_html(
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
        help_text=(
            'Confirme sua Senha.'
        ),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    # def clean_username(self):
    #     return self.validate_username(is_register=True)

    # def clean_email(self):
    #     return self.validate_email(is_register=True)

    def clean(self, *args, **kwargs):
        # self.validate_password()

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)
