from django.contrib import admin

from CashRegister.models import CashOut, CashRegister


@admin.register(CashRegister)
class AdminVitalizeCashRegister(admin.ModelAdmin):
    list_display = 'id', 'cash', 'is_open', 'open_date', 'close_date',
    list_display_links = 'id',
    list_editable = 'is_open',
    ordering = '-id',
    list_filter = 'open_date', 'close_date',
    list_per_page = 20


@admin.register(CashOut)
class AdminVitalizeCashOut(admin.ModelAdmin):
    list_display = 'id', 'value', 'description',
    list_display_links = 'id',
    list_editable = 'value', 'description',
    search_fields = 'value',
    ordering = '-id',
    list_per_page = 20
