from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Users.forms import ProfileForm


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class ProfileClassView(View):
    def render_form(self, form):
        title = 'Perfil'
        subtitle = 'de Usuário'

        return render(
            self.request,
            'users/pages/profile.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
                'form': form,
                'form_action': reverse('users:profile'),
            }
        )

    def get(self, *args, **kwargs):
        form = ProfileForm(instance=self.request.user)
        return self.render_form(form=form)

    def post(self, *args, **kwargs):
        form = ProfileForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.request.user
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(
                self.request,
                'Dados Editados com Sucesso.'
            )

            return redirect(reverse('users:profile'))

        return self.render_form(form=form)
