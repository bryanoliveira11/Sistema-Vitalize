from django.contrib import admin

from Products.models import Products
from Sales.models import PaymentTypes, Sales


@admin.register(PaymentTypes)
class AdminVitalizePaymentTypes(admin.ModelAdmin):
    list_display = 'id', 'payment_name', 'is_active',
    list_display_links = 'id',
    list_editable = 'payment_name', 'is_active',
    search_fields = 'payment_name',
    ordering = '-id',
    list_per_page = 20


@admin.register(Sales)
class AdminVitalizeSales(admin.ModelAdmin):
    list_display = 'id', 'schedule', 'get_products', \
        'get_payment_types', 'total_price',
    list_display_links = 'id',
    list_filter = 'payment_types', 'products',
    search_fields = 'schedule',
    readonly_fields = 'created_at', 'price_in_BRL',
    ordering = '-id',
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('schedule', 'products', 'payment_types')

    def get_products(self, obj):
        products = obj.products.all()
        return ", ".join(
            [product.product_name for product in products]
        ) or 'Nenhum Produto Escolhido.'
    get_products.short_description = 'Produto(s)'

    def get_payment_types(self, obj):
        payment_types = obj.payment_types.all()
        return ", ".join(
            [payment_type.payment_name for payment_type in payment_types]
        )
    get_payment_types.short_description = 'Tipo(s) de Pagamento'

    def price_in_BRL(self, obj):
        return f'{obj.total_price} R$'

    price_in_BRL.short_description = 'Preço Total'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "products":
            kwargs["queryset"] = Products.objects.filter(
                is_active=True
            ).order_by('-pk')

        if db_field.name == "payment_types":
            kwargs["queryset"] = PaymentTypes.objects.filter(
                is_active=True
            ).order_by('-pk')

        return super().formfield_for_manytomany(db_field, request, **kwargs)
