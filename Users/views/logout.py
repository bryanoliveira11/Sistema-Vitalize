from django.contrib import messages
from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View


class LogoutClassView(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        user = self.request.user.get_username()

        if self.request.POST.get('user') != user:
            messages.error(self.request, 'Usuário de Logout Inválido.')
            return redirect(reverse('users:login'))
        messages.success(self.request, 'Logout Efetuado. Até a Próxima !')

        logout(self.request)
        return redirect(reverse('users:login'))
