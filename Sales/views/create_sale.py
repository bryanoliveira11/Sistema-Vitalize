from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Sales.forms import CreateSaleForm
from utils.cashregister_utils import get_today_cashregister
from utils.create_log import create_log


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CreateSaleClassView(View):
    def render_form(self, form: CreateSaleForm):
        title = 'Registrar'
        subtitle = 'Venda'

        return render(
            self.request,
            'sales/pages/create_sale.html',
            context={
                'form': form,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'is_creating_sale': True,
            }
        )

    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        if get_today_cashregister() is None:
            return redirect(reverse('cashregister:cashregister'))

        return self.render_form(form=CreateSaleForm())

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        form = CreateSaleForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            sale = form.save(commit=False)
            schedule = form.cleaned_data.get('schedule')
            products = form.cleaned_data.get('products')
            total_price = 0

            if schedule:
                total_price += schedule.total_price

            if products is not None:
                total_price += sum(product.price for product in products)

            sale.total_price = total_price

            sale.save()

            if products is not None:
                sale.products.set(products)

            cashregister = get_today_cashregister()

            if cashregister:
                cashregister.sales.add(sale)

            messages.success(
                self.request,
                'Venda Registrada com Sucesso.'
            )

            create_log(
                self.request.user,
                f'Venda ID : {sale.pk} Registrada com Sucesso.',
                'Sales'
            )

            return redirect(reverse('cashregister:cashregister'))

        return self.render_form(form=form)
