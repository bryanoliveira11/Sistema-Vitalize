from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import ListView

from Products.models import Categories, Products
from utils.pagination import make_pagination


class ProductsClassView(ListView):
    template_name = 'Products/pages/products.html'
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


class CategoriesFilterClassView(ProductsClassView):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            product_category__id=self.kwargs.get('id'),
            is_active=True,
        ).select_related('product_category')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        try:
            category_name = context.get('object_list', None)[
                0].product_category
            category_name = f'({str(category_name)})'
        except IndexError:
            category_name = None

        context.update({
            'page_title': 'Filtro',
            'page_subtitle': f'por Categoria {str(category_name)}',
            'is_filtered': True,
        })

        return context


class SearchClassView(ProductsClassView):
    def __init__(self, *args, **kwargs) -> None:
        self.search_term = None
        super().__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Products]:
        queryset = super().get_queryset(*args, **kwargs)
        self.search_term = self.request.GET.get('q', '').strip()

        queryset = queryset.filter(
            Q(
                Q(product_name__icontains=self.search_term) |
                Q(product_category__category_name__icontains=self.search_term)
            )
        ).select_related('product_category')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'page_title': 'Busca',
            'page_subtitle': f'por "{self.search_term}"',
            'additional_url_query': f'&q={self.search_term}',
            'is_filtered': True,
        })
        return context
