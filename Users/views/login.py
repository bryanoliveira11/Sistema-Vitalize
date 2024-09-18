from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.core.signing import BadSignature, SignatureExpired, loads
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
                    f'Logado como "{self.request.user}".'
                )
                return redirect(reverse('products:products'))
            else:
                messages.error(self.request, 'Credenciais Inválidas.')
        else:
            messages.error(self.request, 'E-mail ou Senha Inválidos.')

        return redirect(reverse('users:login'))


class AutoLoginClassView(View):
    def get(self, *args, **kwargs):
        token = self.request.GET.get('token')

        if token:
            try:
                user_id = loads(token, max_age=86400)
                user = get_user_model().objects.get(pk=user_id)
                login(
                    self.request, user,
                    'django.contrib.auth.backends.ModelBackend'
                )
                messages.success(
                    self.request,
                    f'Logado como "{self.request.user}".'
                )
                return redirect(reverse('products:products'))

            except (BadSignature, SignatureExpired):
                messages.error(
                    self.request,
                    'Token de Login Expirado ou Inválido. '
                    'Por Favor, Utilize o Formulário Abaixo.'
                )
                return redirect(reverse('users:login'))
        else:
            messages.error(
                self.request,
                'Erro ao Logar Automaticamente. '
                'Por Favor, Utilize o Formulário Abaixo.'
            )
            return redirect(reverse('users:login'))
