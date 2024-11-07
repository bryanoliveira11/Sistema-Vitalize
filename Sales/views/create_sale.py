from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Sales.forms import CreateSaleForm
from Sales.models import SaleItem, Schedules
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
            return redirect(reverse('users:no-permission'))

        if get_today_cashregister() is None:
            return redirect(reverse('cashregister:cashregister'))

        return self.render_form(form=CreateSaleForm())

    def post(self, *args, **kwargs):
        if not self.request.user.is_superuser:  # type: ignore
            return redirect(reverse('users:no-permission'))

        form = CreateSaleForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            sale = form.save(commit=False)
            user = form.cleaned_data.get('user')
            schedule = form.cleaned_data.get('schedule')
            products = form.cleaned_data.get('products')
            services = form.cleaned_data.get('services')

            total_price = 0
            schedule_price = 0

            sale.total_price = total_price
            sale.save()

            if products is not None:
                sale_items = []
                total_price = 0
                sale.products.set(products)

                for product in products:
                    quantity = self.request.POST.get(
                        f'quantities[{product.pk}]'
                    )
                    quantity = quantity or 1
                    qty_price = product.price * int(quantity)

                    sale_item = SaleItem(
                        sale=sale,
                        product=product,
                        quantity=int(quantity),
                        total_price=qty_price
                    )
                    sale_items.append(sale_item)
                    total_price += qty_price

                SaleItem.objects.bulk_create(sale_items)

            if schedule:
                schedule.services.set(services)

                if not schedule.schedule_date:
                    schedule.schedule_date = datetime.now()

                schedule.save()

                if services:
                    service_total = sum(service.price for service in services)
                    schedule_price = service_total

                schedule.total_price = schedule_price
                schedule.save()
            else:
                if services:
                    service_total = sum(service.price for service in services)
                    schedule = Schedules.objects.create(
                        user=user,
                        schedule_date=datetime.now(),
                        total_price=service_total,
                    )
                    schedule.services.set(services)
                    schedule.save()
                    sale.schedule = schedule
                    schedule_price = service_total
                    sale.save()

            sale.total_price = total_price + schedule_price
            sale.user = user
            sale.save()

            cashregister = get_today_cashregister()

            if cashregister:
                cashregister.sales.add(sale)

            messages.success(
                self.request,
                'Venda Registrada com Sucesso.'
            )
            create_log(
                self.request.user,
                'Venda Registrada com Sucesso.',
                'Sales',
                sale.pk
            )

            return redirect(reverse('cashregister:cashregister'))

        return self.render_form(form=form)
