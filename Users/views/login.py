from django.shortcuts import render
from django.views.generic import View


class LoginClassView(View):
    def get(self, *args, **kwargs):
        return render(
            self.request,
            'users/pages/login.html',
            {'title': 'Login'}
        )
