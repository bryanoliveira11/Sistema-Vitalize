from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from Users.forms import RegisterForm


class RegisterClassView(View):
    def get(self, *args, **kwargs):
        title = 'Cadastro'
        subtitle = 'de Usuário'
        register_data = self.request.session.get('register_data', None)
        form = RegisterForm(register_data)

        return render(
            self.request,
            'users/pages/register.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
                'btn_text': 'Cadastrar',
                'form': form,
                'form_action': reverse('users:register'),
            }
        )
