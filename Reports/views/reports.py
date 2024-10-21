from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class SelectReportClassView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type:ignore
            raise Http404()

        title = 'Selecionar'
        subtitle = 'Relatório'

        return render(
            self.request,
            'reports/pages/select_report.html',
            context={
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
