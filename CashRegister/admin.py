from django.contrib import admin

from CashRegister.models import CashOut, CashRegister


@admin.register(CashRegister)
class AdminVitalizeCashRegister(admin.ModelAdmin):
    list_display = 'id', 'get_sales', 'cash', 'is_open', \
        'open_date', 'close_date',
    list_display_links = 'id',
    ordering = '-id',
    list_filter = 'open_date', 'close_date',
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('sales', 'cash_out')

    def get_sales(self, obj):
        sales = obj.sales.all()
        return ", ".join(
            [str(sale) for sale in sales]
        ) or 'Nenhuma Venda Feita até o Momento.'
    get_sales.short_description = 'Vendas'


@admin.register(CashOut)
class AdminVitalizeCashOut(admin.ModelAdmin):
    list_display = 'id', 'value', 'description',
    list_display_links = 'id',
    list_editable = 'value', 'description',
    search_fields = 'value',
    ordering = '-id',
    list_per_page = 20
