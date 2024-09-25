from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from CashRegister.forms import CashOutForm
from CashRegister.models import CashOut, CashRegister
from utils.cashregister_utils import get_today_cashouts, get_today_cashregister
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

        show_cashout_arg = self.request.GET.get('show_cashouts')
        show_cashouts = True if show_cashout_arg else False

        if cashregister is None:
            messages.info(
                self.request, 'Nenhum Caixa Aberto Encontrado.'
            )
        else:
            page_obj, pagination_range = make_pagination(
                self.request, cashregister.sales.all().order_by('-pk'), 10
            )
            cashouts = get_today_cashouts(cashregister)

        return render(
            self.request,
            'cashregister/pages/cashregister.html',
            context={
                'sales': page_obj,
                'page_obj': page_obj,
                'cashregister': cashregister,
                'cashouts': cashouts,
                'pagination_range': pagination_range,
                'open_cashregister': reverse(
                    'cashregister:cashregister_open'
                ),
                'close_cashregister': reverse(
                    'cashregister:cashregister_close'
                ),
                'show_cashouts': show_cashouts,
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

        messages.success(self.request, 'Caixa Aberto com Sucesso.')
        cashregister = CashRegister.objects.create()
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


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CashOutClassView(View):
    def render_form(
        self, form: CashOutForm, cashregister: CashRegister | None
    ):
        title = 'Sangria'
        subtitle = 'de Caixa'

        if cashregister is None:
            return redirect(reverse('cashregister:cashregister'))

        return render(
            self.request,
            'cashregister/pages/cashout.html',
            context={
                'form': form,
                'cashregister': cashregister,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )

    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        cashregister = get_today_cashregister()

        return self.render_form(
            form=CashOutForm(instance=cashregister),
            cashregister=cashregister,
        )

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        cashregister = get_today_cashregister()

        form = CashOutForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=cashregister,
        )

        if form.is_valid() and cashregister is not None:
            cash_out = form.cleaned_data.get('cash_out')

            if not cashregister:
                messages.error(self.request, 'Ocorreu um Erro.')
                return redirect(reverse('cashregister:cashregister'))

            cashregister.update_total_price(
                amount=cash_out,
                operation='remove'
            )

            cash_out = CashOut.objects.create(
                value=cash_out,
                cashregister=cashregister
            )

            messages.success(
                self.request,
                'Sangria Registrada com Sucesso.'
            )

            create_log(
                self.request.user,
                f'Sangria ID : {cash_out.pk} no Caixa ID : {cashregister.pk} '
                'Registrada com Sucesso.',
                'CashOut, CashRegister'
            )

            return redirect(reverse('cashregister:cashregister'))

        return self.render_form(form=form, cashregister=cashregister)
