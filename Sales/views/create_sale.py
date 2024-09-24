from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Sales.forms import CreateSaleForm
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
            }
        )

    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            raise Http404()

        return self.render_form(form=CreateSaleForm())

    def post(self, *args, **kwargs):
        form = CreateSaleForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            sale = form.save(commit=False)
            schedule = form.cleaned_data.get('schedule')
            products = form.cleaned_data.get('products')
            payment_types = form.cleaned_data.get('payment_types')
            total_price = 0

            if schedule:
                total_price += schedule.total_price

            if products is not None:
                total_price += sum(product.price for product in products)

            sale.total_price = total_price

            sale.save()

            if products is not None:
                sale.products.set(products)

            if payment_types is not None:
                sale.payment_types.set(payment_types)

            messages.success(
                self.request,
                'Venda Registrada com Sucesso.'
            )

            create_log(
                self.request.user,
                f'Venda ID : {sale.pk} Registrada com Sucesso.',
                'Sales'
            )

            return redirect(reverse('users:admin_options'))

        return self.render_form(form=form)
