from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from CashRegister.models import CashRegister
from utils.cashregister_utils import (close_last_cashregisters,
                                      get_last_cashregister, get_today_cashins,
                                      get_today_cashouts,
                                      get_today_cashregister)
from utils.create_log import create_log
from utils.pagination import make_pagination


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CashRegisterClassView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        cashregister = get_today_cashregister()
        title = 'Caixa'
        subtitle = 'de Hoje'
        page_obj = None
        pagination_range = None
        cashouts = None
        cashins = None

        show_cashout_arg = self.request.GET.get('show_cashouts')
        show_cashouts = True if show_cashout_arg else False
        show_cashint_arg = self.request.GET.get('show_cashins')
        show_cashins = True if show_cashint_arg else False

        if cashregister is None:
            messages.info(
                self.request, 'Nenhum Caixa Aberto Encontrado.'
            )
        else:
            page_obj, pagination_range = make_pagination(
                self.request, cashregister.sales.all().order_by('-pk'), 10
            )
            if show_cashouts:
                cashouts = get_today_cashouts(cashregister)
            if show_cashins:
                cashins = get_today_cashins(cashregister)

        return render(
            self.request,
            'cashregister/pages/cashregister.html',
            context={
                'sales': page_obj,
                'page_obj': page_obj,
                'cashregister': cashregister,
                'last_cashregister': get_last_cashregister() if cashregister
                is None else None,
                'cashouts': cashouts,
                'cashins': cashins,
                'pagination_range': pagination_range,
                'open_cashregister': reverse(
                    'cashregister:cashregister_open'
                ),
                'close_cashregister': reverse(
                    'cashregister:cashregister_close'
                ),
                'show_cashouts': show_cashouts,
                'show_cashins': show_cashins,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CashRegisterOpenClassView(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        close_last_cashregisters()
        last_cashregister = get_last_cashregister()
        messages.success(self.request, 'Caixa Aberto com Sucesso.')
        cashregister = CashRegister.objects.create(
            cash=last_cashregister.cash if last_cashregister else 0,
        )
        create_log(
            self.request.user, f'Caixa ID : {cashregister.pk} foi Aberto.',
            table_affected='CashRegister',
        )
        return redirect(reverse('cashregister:cashregister'))


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CashRegisterCloseClassView(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        messages.success(self.request, 'Caixa Fechado com Sucesso.')
        cashregister = get_today_cashregister()

        if not cashregister:
            return redirect(reverse('cashregister:cashregister'))

        cashregister.is_open = False
        cashregister.save()

        create_log(
            self.request.user, f'Caixa ID : {cashregister.pk} foi Fechado.',
            table_affected='CashRegister',
        )

        return redirect(reverse('cashregister:cashregister'))
