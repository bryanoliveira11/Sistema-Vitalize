from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Sales.models import Sales
from utils.cashregister_utils import get_today_cashregister
from utils.create_log import create_log


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CancelSaleClassView(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        sale_to_cancel = Sales.objects.select_for_update().filter(
            id=self.kwargs.get('id'),
        ).first()

        cashregister = get_today_cashregister()

        if sale_to_cancel is not None and cashregister is not None:
            if sale_to_cancel not in cashregister.sales.all():
                messages.error(self.request, 'Venda Inválida.')
                return redirect(reverse('cashregister:cashregister'))

            if sale_to_cancel.total_price > cashregister.cash:
                messages.error(
                    self.request,
                    'Valor de Estorno Maior que o Valor do Caixa.'
                )
                return redirect(reverse('cashregister:cashregister'))

            sale_to_cancel.canceled = True
            sale_to_cancel.save()
            cashregister.update_total_price(
                amount=sale_to_cancel.total_price,
                operation='remove',
            )
            cashregister.save()
            messages.success(self.request, 'Venda Cancelada com Sucesso.')
            create_log(
                self.request.user,
                'Venda Cancelada com Sucesso.',
                'Sales',
                sale_to_cancel.pk
            )
            return redirect(reverse('cashregister:cashregister'))

        messages.error(
            self.request, 'Erro ao Cancelar Venda. Tente Novamente.'
        )
        return redirect(reverse('cashregister:cashregister'))
