from django import forms
from django.utils.html import format_html

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_attr(self.fields['password'], 'class', 'login-password-field')

    email = forms.EmailField(
        label=format_html(
            '<i class="fa-solid fa-envelope mr-03"></i> E-mail'
        ),
        error_messages={
            'required': 'Digite seu E-mail.',
        },
    )
    password = forms.CharField(
        label=format_html(
            '<i class="fa-solid fa-lock m-right"></i> Senha'
        ),
        help_text=format_html(
            '''
          <div class="forgot-password-content">
          <a href=""
          id="forgot-password" title="Esqueceu sua Senha">
          Esqueceu sua Senha ?
          </a>
          </div>
            '''
        ),
        widget=forms.PasswordInput()
    )
