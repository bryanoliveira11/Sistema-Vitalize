from django.contrib import admin

from CashRegister.models import CashIn, CashOut, CashRegister
from utils.cashregister_utils import get_today_cashregister


@admin.register(CashRegister)
class AdminVitalizeCashRegister(admin.ModelAdmin):
    list_display = 'id', 'get_sales', 'cash', 'is_open', \
        'open_date', 'close_date',
    list_display_links = 'id',
    ordering = '-id',
    list_filter = 'open_date', 'close_date', 'is_open',
    readonly_fields = 'open_date', 'close_date', 'cash_in_BRL',
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('sales')

    def get_sales(self, obj):
        sales = obj.sales.all()
        return f'{len(sales)} Venda(s)'
    get_sales.short_description = 'Vendas'

    def cash_in_BRL(self, obj):
        return f'R$ {obj.cash}' if obj.cash is not None else f'R$ {0}'

    cash_in_BRL.short_description = 'Valor do Caixa'

    def has_change_permission(self, request, obj=None):
        if obj is not None and not obj.is_open:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not obj.is_open:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        today_cashregister = get_today_cashregister()

        if today_cashregister is not None:
            return False

        return super().has_add_permission(request)


@admin.register(CashOut)
class AdminVitalizeCashOut(admin.ModelAdmin):
    list_display = 'id', 'description', 'value', 'cashregister', 'created_at',
    list_display_links = 'id', 'description',
    readonly_fields = 'created_at', 'value_in_BRL',
    ordering = '-id',
    list_per_page = 20

    def value_in_BRL(self, obj):
        return f'R$ {obj.value}' if obj.value \
            is not None else f'R$ {0}'

    value_in_BRL.short_description = 'Valor da Sangria'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cashregister":
            kwargs["queryset"] = CashRegister.objects.filter(
                is_open=True,
            ).order_by('-pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CashIn)
class AdminVitalizeCashIn(admin.ModelAdmin):
    list_display = 'id', 'description', 'value', 'cashregister', 'created_at',
    list_display_links = 'id', 'description',
    readonly_fields = 'created_at', 'value_in_BRL',
    ordering = '-id',
    list_per_page = 20

    def value_in_BRL(self, obj):
        return f'R$ {obj.value}' if obj.value \
            is not None else f'R$ {0}'

    value_in_BRL.short_description = 'Valor da Entrada'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cashregister":
            kwargs["queryset"] = CashRegister.objects.filter(
                is_open=True,
            ).order_by('-pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
