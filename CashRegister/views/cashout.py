from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from CashRegister.forms import CashOutForm
from CashRegister.models import CashOut, CashRegister
from utils.cashregister_utils import get_today_cashregister
from utils.create_log import create_log


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
            description = form.cleaned_data.get('description')

            if not cashregister:
                messages.error(self.request, 'Ocorreu um Erro.')
                return redirect(reverse('cashregister:cashregister'))

            cashregister.update_total_price(
                amount=cash_out,
                operation='remove'
            )

            cash_out = CashOut.objects.create(
                value=cash_out,
                description=description,
                cashregister=cashregister
            )

            messages.success(
                self.request,
                'Sangria Registrada com Sucesso.'
            )

            create_log(
                self.request.user,
                'Sangria Registrada com Sucesso.',
                'CashOut',
                cash_out.pk,
            )

            return redirect(
                reverse('cashregister:cashregister') + '?show_cashouts=True'
            )

        return self.render_form(form=form, cashregister=cashregister)
