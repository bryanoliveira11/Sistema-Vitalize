from crispy_forms.bootstrap import AppendedText, PrependedAppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.utils.safestring import mark_safe

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_attr(self.fields['password'], 'class', 'login-password-field')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            PrependedAppendedText('email', mark_safe(
                '<i class="fa-solid fa-envelope"></i>')
            ),
            AppendedText('password', mark_safe(
                '<i class="fa-solid fa-eye"></i>'), css_class='show-password'
            ),
        )

    email = forms.EmailField(
        label='E-mail',
        error_messages={
            'required': 'Digite seu E-mail.',
        },
    )
    password = forms.CharField(
        label='Senha',
        # help_text=mark_safe(
        #     '''
        #   <div class="forgot-password-content">
        #   <a href=""
        #   id="forgot-password" title="Esqueceu sua Senha">
        #   Esqueceu sua Senha ?
        #   </a>
        #   </div>
        #     '''
        # ),
        widget=forms.PasswordInput()
    )
