from django.contrib import messages
from django.core.signing import dumps
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from Users.forms import RegisterForm
from Users.templates.users.emails.email_templates import signin_email_template
from utils.create_log import create_log
from utils.email_service import send_html_mail


class RegisterClassView(View):
    def generate_user_token(self, user):
        token = dumps(user.pk)
        return token

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
                'form': form,
                'form_action': reverse('users:register'),
            }
        )

    def post(self, *args, **kwargs):
        POST = self.request.POST
        self.request.session['register_data'] = POST

        form = RegisterForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            messages.success(
                self.request,
                'Usuário Cadastrado com Sucesso !</br>'
                '<b>Confirme</b> seu Cadastro Utilizando '
                'o <b>Link</b> que Enviamos em seu <b>E-mail</b>.'
            )

            create_log(
                user, 'Usuário foi cadastrado com sucesso.', 'VitalizeUser'
            )

            token = self.generate_user_token(user=user)

            url = f'{reverse('users:auto-login')}?token={token}'

            send_html_mail(
                subject='Confirmação de Cadastro',
                html_content=signin_email_template(
                    user.first_name, url
                ),
                recipient_list=[user.email],
            )

            del (self.request.session['register_data'])

            return redirect(reverse('users:login'))

        return redirect(reverse('users:register'))
