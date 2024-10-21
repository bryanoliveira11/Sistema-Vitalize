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
        additional_url_query = ''
        sales_label = None
        is_filtered = False
        show_cashouts = 'show_cashouts' in self.request.GET
        show_cashins = 'show_cashins' in self.request.GET
        sales_canceled = 'sales_canceled' in self.request.GET
        sales_finished = 'sales_finished' in self.request.GET

        if cashregister is None:
            messages.info(
                self.request, 'Nenhum Caixa Aberto Encontrado.'
            )
        else:
            if show_cashouts:
                cashouts = get_today_cashouts(cashregister)
                page_obj, pagination_range = make_pagination(
                    self.request, cashouts, 10
                )
                additional_url_query = '&show_cashouts=True'
            elif show_cashins:
                cashins = get_today_cashins(cashregister)
                page_obj, pagination_range = make_pagination(
                    self.request, cashins, 10
                )
                additional_url_query = '&show_cashins=True'
            else:
                qs = cashregister.sales.all().order_by('-pk')

                if sales_canceled:
                    qs = qs.filter(canceled=True)
                    additional_url_query = '&sales_canceled=True'
                    sales_label = 'Canceladas'
                    is_filtered = True

                if sales_finished:
                    qs = qs.filter(canceled=False)
                    additional_url_query = '&sales_finished=True'
                    sales_label = 'Finalizadas'
                    is_filtered = True

                page_obj, pagination_range = make_pagination(
                    self.request, qs, 10
                )

        return render(
            self.request,
            'cashregister/pages/cashregister.html',
            context={
                'cashregister': cashregister,
                'sales': page_obj,
                'page_obj': page_obj,
                'cashouts': page_obj,
                'cashins': page_obj,
                'last_cashregister': get_last_cashregister() if cashregister
                is None else None,
                'pagination_range': pagination_range,
                'additional_url_query': additional_url_query,
                'open_cashregister': reverse('cashregister:cashregister_open'),
                'close_cashregister': reverse(
                    'cashregister:cashregister_close'
                ),
                'show_cashouts': show_cashouts,
                'show_cashins': show_cashins,
                'sales_label': sales_label,
                'is_filtered': is_filtered,
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
            self.request.user,
            'Caixa foi Aberto.',
            'CashRegister',
            cashregister.pk,
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
            self.request.user,
            'Caixa foi Fechado.',
            'CashRegister',
            cashregister.pk,
        )

        return redirect(reverse('cashregister:cashregister'))
