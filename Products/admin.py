from django.contrib import admin

from Products.models import Categories, Products


@admin.register(Products)
class AdminVitalizeProducts(admin.ModelAdmin):
    list_display = 'id', 'product_name', 'product_category', \
        'price_in_BRL', 'show', 'is_active',
    list_display_links = 'id', 'product_name',
    list_editable = 'show', 'is_active',
    search_fields = 'product_name', 'product_category',
    prepopulated_fields = {
        'slug': ('product_name',)
    }
    ordering = '-id',
    list_filter = 'product_category', 'is_active', 'show',
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product_category')

    def price_in_BRL(self, obj):
        return f'R$ {obj.price}' if obj.price \
            is not None else f'R$ {0}'
    price_in_BRL.short_description = 'Preço'

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product_category":
            kwargs["queryset"] = Categories.objects.filter(
                is_active=True
            ).order_by('-pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Categories)
class AdminVitalizeCategories(admin.ModelAdmin):
    list_display = 'id', 'category_name', 'is_active',
    list_display_links = 'id', 'category_name',
    list_editable = 'is_active',
    search_fields = 'category_name',
    ordering = '-id',
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)
