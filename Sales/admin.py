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
    list_display = 'id', 'schedule', 'total_price',
    list_display_links = 'id', 'schedule',
    list_editable = 'total_price',
    search_fields = 'schedule',
    ordering = '-id',
    list_per_page = 20