from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from utils.user_utils import validate_user_acess


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class AdminUserOptionsClassView(View):
    def get(self, *args, **kwargs):
        if not validate_user_acess(self.request):  # type: ignore
            return redirect(reverse('users:no-permission'))

        title = 'Opções'
        subtitle = 'de Administrador'

        return render(
            self.request,
            'users/pages/admin_options.html',
            context={
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
