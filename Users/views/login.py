from django.shortcuts import render
from django.views.generic import View


class LoginClassView(View):
    def get(self, *args, **kwargs):
        title = 'Login'
        subtitle = 'de Usuário'

        return render(
            self.request,
            'users/pages/login.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
