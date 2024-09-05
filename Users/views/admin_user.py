from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class AdminUserOptionsClassView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        title = 'Opções'
        subtitle = 'de Administrador'

        return render(
            self.request,
            'users/pages/admin_options.html',
            {
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
