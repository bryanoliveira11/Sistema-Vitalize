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


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors: defaultdict[str, list[str]] = defaultdict(list)

        add_placeholder(self.fields['first_name'], 'Digite seu Nome')
        add_placeholder(self.fields['last_name'], 'Digite seu Sobrenome')
        add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
        add_placeholder(self.fields['email2'], 'Confirme seu E-mail')
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_placeholder(self.fields['password2'], 'Confirme sua Senha')
        add_placeholder(self.fields['phone_number'], 'Digite seu Telefone')
        add_attr(self.fields['password'], 'class', 'password-help-text-m0')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            PrependedAppendedText('email', mark_safe(
                '<i class="fa-solid fa-envelope"></i>')
            ),
            Field('email2', css_class='prevent-paste'),
            PrependedAppendedText('phone_number', mark_safe(
                '<i class="fa-solid fa-phone"></i>')
            ),
            AppendedText('password', mark_safe(
                '<i class="fa-solid fa-eye"></i>'), css_class='show-password'
            ),
            Field('password2'),
        )

    def validate_email(self):
        email = self.cleaned_data.get('email')
        email_database = User.objects.filter(email__iexact=email).first()

        if email_database:
            self._my_errors['email'].append(
                'Este E-mail Está em Uso.'
            )

        return email

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

    def handle_css_classes(self):
        for field_name, field in self.fields.items():
            if field_name in ['password', 'password2']:
                continue

            if field_name in self.errors:
                add_attr(field, 'class', 'is-invalid')
                return

            add_attr(field, 'class', 'is-valid')

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password', 'phone_number'
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

    email2 = forms.EmailField(
        label='Confirmação de E-mail',
        error_messages={
            'required': 'Confirme seu E-mail.'
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

    def clean_email(self):
        return self.validate_email()

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            self._my_errors['email'].append(
                'E-mails Precisam ser Iguais.'
            )
            self._my_errors['email2'].append(
                'E-mails Precisam ser Iguais.'
            )

    def clean(self, *args, **kwargs):
        self.validate_password()
        self.handle_css_classes()

        if self._my_errors:
            raise ValidationError(dict(self._my_errors))

        return super().clean(*args, **kwargs)
