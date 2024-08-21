from django.contrib import admin

from CashRegister.models import CashRegister, CashOut


@admin.register(CashRegister)
class AdminVitalizeCashRegister(admin.ModelAdmin):
    list_display = 'id', 'cash', 'is_open', 'open_date', 'close_date',
    list_display_links = 'id',
    list_editable = 'is_open', 'close_date', 'value',
    # search_fields = 'product_name',
    ordering = '-id',
    list_filter = 'product_category',
    list_per_page = 20