from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from Users.forms import LoginForm


class LoginClassView(View):
    def get(self, *args, **kwargs):
        title = 'Login'
        subtitle = 'de Usuário'
        form = LoginForm()

        return render(
            self.request,
            'users/pages/login.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
                'btn_text': title,
                'form': form,
                'form_action': reverse('users:login'),
            }
        )
