from django.http import Http404
from django.views.generic import DetailView

from Products.models import Products
from utils.user_utils import get_notifications


class ProductDetailClassView(DetailView):
    template_name = 'Products/pages/product_detail.html'
    model = Products
    context_object_name = 'product'
    slug_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            show=True,
        ).select_related('product_category')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        product = context.get('product')
        related_products = None

        if product:
            category = product.product_category
            if category:
                related_products = Products.objects.filter(
                    product_category=category, show=True,
                ).all().select_related('product_category').exclude(
                    pk=product.pk,
                )

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'product': product,
            'related_products': related_products,
            'site_title': product.product_name if product else None,
            'page_title': 'Veja',
            'page_subtitle': 'Também',
            'is_product_detail': True,
            'notifications': notifications,
            'notifications_total': notifications_total,
        })

        return context
