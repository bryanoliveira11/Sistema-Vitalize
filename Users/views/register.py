from django.shortcuts import render
from django.views.generic import View


class RegisterClassView(View):
    def get(self, *args, **kwargs):
        return render(
            self.request,
            'users/pages/register.html',
            {'title': 'Cadastro'}
        )
