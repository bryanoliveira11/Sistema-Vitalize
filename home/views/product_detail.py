from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView

from Products.models import Products


class ProductDetailClassView(DetailView):
    template_name = 'Home/pages/product_detail.html'
    model = Products
    context_object_name = 'product'
    slug_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            is_active=True
        ).select_related('product_category')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        product = context.get('product')
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('home:products')
        )
        context.update({
            'product': product,
            'site_title': product.product_name if product else None,
            'go_back_url': http_referer,
        })

        return context
