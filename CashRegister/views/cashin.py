from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from CashRegister.forms import CashInForm
from CashRegister.models import CashIn, CashRegister
from utils.cashregister_utils import get_today_cashregister
from utils.create_log import create_log


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CashInClassView(View):
    def render_form(
        self, form: CashInForm, cashregister: CashRegister | None
    ):
        title = 'Entrada'
        subtitle = 'de Caixa'

        if cashregister is None:
            return redirect(reverse('cashregister:cashregister'))

        return render(
            self.request,
            'cashregister/pages/cashin.html',
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
            return redirect(reverse('users:no-permission'))

        cashregister = get_today_cashregister()

        return self.render_form(
            form=CashInForm(instance=cashregister),
            cashregister=cashregister,
        )

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            return redirect(reverse('users:no-permission'))

        cashregister = get_today_cashregister()

        form = CashInForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=cashregister,
        )

        if form.is_valid() and cashregister is not None:
            cash_in = form.cleaned_data.get('cash_in')
            description = form.cleaned_data.get('description')

            if not cashregister:
                messages.error(self.request, 'Ocorreu um Erro.')
                return redirect(reverse('cashregister:cashregister'))

            cashregister.update_total_price(
                amount=cash_in,
                operation='add'
            )

            cash_in = CashIn.objects.create(
                value=cash_in,
                description=description,
                cashregister=cashregister
            )

            messages.success(
                self.request,
                'Entrada Registrada com Sucesso.'
            )

            create_log(
                self.request.user,
                'Entrada Registrada com Sucesso.',
                'CashIn',
                cash_in.pk,
            )

            return redirect(
                reverse('cashregister:cashregister') + '?show_cashins=True'
            )

        return self.render_form(form=form, cashregister=cashregister)
