from django.db.models.query import QuerySet
from django.views.generic import ListView

from Products.models import Categories, Products
from utils.pagination import make_pagination


class HomePage(ListView):
    template_name = 'home/pages/home.html'
    model = Products
    context_object_name = 'products'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs) -> QuerySet[Products]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            is_active=True,
        ).select_related('product_category')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        products = context.get('products')
        categories = Categories.objects.all()
        page_obj, pagination_range = make_pagination(
            self.request, products, 15
        )

        context.update({
            'products': page_obj,
            'pagination_range': pagination_range,
            'categories': categories,
            'page_title': 'Vitrine',
            'page_subtitle': 'de Produtos',
        })

        return context
