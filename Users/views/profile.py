from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Users.forms import EditPasswordForm, ProfileForm


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class ProfileClassView(View):
    def get_user_full_name(self) -> str:
        user = self.request.user.get_full_name()  # type:ignore
        return user

    def render_form(
        self, form: ProfileForm | EditPasswordForm, title: str, subtitle: str,
        is_data_form: bool = False, is_password_form: bool = False
    ):
        title = title
        subtitle = subtitle

        if is_data_form:
            form_action = reverse('users:profile')
        else:
            form_action = reverse('users:profile_password')

        return render(
            self.request,
            'users/pages/profile.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
                'form': form,
                'form_action': form_action,
                'is_data_form': is_data_form,
                'is_password_form': is_password_form,
            }
        )

    def get(self, *args, **kwargs):
        form = ProfileForm(instance=self.request.user)
        return self.render_form(
            form=form, title='Perfil',
            subtitle=f'de Usuário ({self.get_user_full_name()})',
            is_data_form=True
        )

    def post(self, *args, **kwargs):
        form = ProfileForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.request.user
        )

        if form.is_valid():
            user = form.save(commit=False)
            email_changed = getattr(form, '_email_changed', False)
            user.save()

            if email_changed:
                messages.warning(
                    self.request,
                    'Detectamos uma Alteração em seu E-mail, '
                    'Por Favor, Faça o Login.'
                )
                logout(self.request)

            messages.success(
                self.request,
                'Dados Editados com Sucesso.'
            )

            return redirect(reverse('users:profile'))

        return self.render_form(
            form=form, title='Perfil',
            subtitle=f'de Usuário ({self.get_user_full_name()})',
            is_data_form=True
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class EditPasswordClassView(ProfileClassView):
    def get(self, *args, **kwargs):
        form = EditPasswordForm(instance=self.request.user)
        return self.render_form(
            form=form, title='Alteração',
            subtitle=f'de Senha ({self.get_user_full_name()})',
            is_password_form=True,
        )

    def post(self, *args, **kwargs):
        form = EditPasswordForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.request.user
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(
                self.request,
                'Senha Alterada com Sucesso ! Por Favor, Faça seu Login.'
            )

            return redirect(reverse('users:login'))

        return self.render_form(
            form=form, title='Alteração',
            subtitle=f'de Senha ({self.get_user_full_name()})',
            is_password_form=True,
        )
