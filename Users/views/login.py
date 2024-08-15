from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
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

    def post(self, *args, **kwargs):
        POST = self.request.POST
        form = LoginForm(POST)

        if form.is_valid():
            authenticated_user = authenticate(
                request=self.request,
                email=form.cleaned_data.get('email', ''),
                password=form.cleaned_data.get('password', '')
            )

            if authenticated_user is not None:
                login(self.request, user=authenticated_user)
                messages.success(
                    self.request,
                    f'Logado como "{self.request.user.get_username()}".'
                )
                return redirect(reverse('home:home'))
            else:
                messages.error(self.request, 'Credenciais Inválidas.')
        else:
            messages.error(self.request, 'E-mail ou Senha Inválidos.')

        return redirect(reverse('users:login'))
