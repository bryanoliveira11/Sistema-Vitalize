from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.generic import View

from CashRegister.models import CashRegister
from Reports.forms import CashRegisterReportForm
from Sales.models import Sales
from utils.user_utils import validate_user_acess


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class SelectReportClassView(View):
    def get(self, *args, **kwargs):
        if not validate_user_acess(self.request):
            return redirect(reverse('users:no-permission'))

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


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CashRegisterReport(View):
    def render_page(self, form: CashRegisterReportForm):
        title = 'Relatório'
        subtitle = 'de Caixa'

        return render(
            self.request,
            'reports/pages/cashregister_report.html',
            context={
                'form': form,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'is_report_page': True,
            }
        )

    def get(self, *args, **kwargs):
        if not validate_user_acess(self.request):
            return redirect(reverse('users:no-permission'))

        return self.render_page(CashRegisterReportForm())

    def post(self, *args, **kwargs):
        if not validate_user_acess(self.request):
            return redirect(reverse('users:no-permission'))

        form = CashRegisterReportForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            date_initial = form.cleaned_data.get('date_initial')
            date_final = form.cleaned_data.get('date_final')

            if date_initial:
                date_initial = datetime.combine(
                    date_initial, datetime.min.time()
                )
                date_initial = make_aware(date_initial)

            if date_final:
                date_final = datetime.combine(date_final, datetime.max.time())
                date_final = make_aware(date_final)

            cashregisters = CashRegister.objects.filter(
                is_open=False,
                open_date__range=(date_initial, date_final)
            ).prefetch_related(Prefetch(
                'sales', queryset=Sales.objects.select_related('payment_type')
            ),)

            print(cashregisters)

        return self.render_page(form)
