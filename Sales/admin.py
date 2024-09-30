from django.contrib import admin

from Products.models import Products
from Sales.models import PaymentTypes, SaleItem, Sales


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
        'payment_type', 'total_price',
    list_display_links = 'id',
    list_filter = 'payment_type', 'products',
    search_fields = 'schedule',
    readonly_fields = 'created_at', 'price_in_BRL',
    ordering = '-id',
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('schedule', 'products', 'payment_type')

    def get_products(self, obj):
        products = obj.products.all()
        return ", ".join(
            [product.product_name for product in products]
        ) or 'Nenhum Produto Escolhido.'
    get_products.short_description = 'Produto(s)'

    def price_in_BRL(self, obj):
        return f'R$ {obj.total_price}' if obj.total_price \
            is not None else f'R$ {0}'

    price_in_BRL.short_description = 'Preço Total'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "payment_type":
            kwargs["queryset"] = PaymentTypes.objects.filter(
                is_active=True
            ).order_by('-pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "products":
            kwargs["queryset"] = Products.objects.filter(
                is_active=True
            ).order_by('-pk')

        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(SaleItem)
class AdminVitalizeSaleItem(admin.ModelAdmin):
    list_display = 'id', 'sale', 'product', 'quantity', \
        'price_in_BRL', 'created_at',
    list_display_links = 'id',
    search_fields = 'sale', 'product',
    list_filter = 'sale', 'product',
    ordering = '-id',
    list_per_page = 20

    def price_in_BRL(self, obj):
        return f'R$ {obj.total_price}' if obj.total_price \
            is not None else f'R$ {0}'

    price_in_BRL.short_description = 'Preço Total'
