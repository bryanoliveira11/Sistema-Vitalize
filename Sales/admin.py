from django.contrib import admin

from Sales.models import PaymentTypes, Sales


@admin.register(PaymentTypes)
class AdminVitalizePaymentTypes(admin.ModelAdmin):
    list_display = 'id', 'payment_name',
    list_display_links = 'id',
    list_editable = 'payment_name',
    search_fields = 'payment_name',
    ordering = '-id',
    list_per_page = 20


@admin.register(Sales)
class AdminVitalizeSales(admin.ModelAdmin):
    list_display = 'id', 'schedule', 'get_products', \
        'get_payment_types', 'total_price',
    list_display_links = 'id', 'schedule',
    search_fields = 'schedule',
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
