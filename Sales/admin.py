from django.contrib import admin

from Sales.models import PaymentTypes


@admin.register(PaymentTypes)
class AdminVitalizePaymentTypes(admin.ModelAdmin):
    list_display = 'id', 'payment_name',
    list_display_links = 'id',
    list_editable = 'payment_name',
    search_fields = 'payment_name',
    ordering = '-id',
    list_per_page = 20