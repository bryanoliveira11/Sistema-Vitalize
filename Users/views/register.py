from django.shortcuts import render
from django.views.generic import View


class RegisterClassView(View):
    def get(self, *args, **kwargs):
        title = 'Cadastro'
        subtitle = 'de Usuário'

        return render(
            self.request,
            'users/pages/register.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
