from django.contrib import admin

from Products.models import Categories, Products


@admin.register(Products)
class AdminVitalizeProducts(admin.ModelAdmin):
    list_display = 'id', 'product_name', 'product_category', \
        'price', 'is_active',
    list_display_links = 'id',
    list_editable = 'product_name', 'product_category', 'price', 'is_active',
    search_fields = 'product_name',
    prepopulated_fields = {
        'slug': ('product_name',)
    }
    ordering = '-id',
    list_filter = 'product_category',
    list_per_page = 20


@admin.register(Categories)
class AdminVitalizeCategories(admin.ModelAdmin):
    list_display = 'id', 'category_name',
    list_display_links = 'id',
    list_editable = 'category_name',
    search_fields = 'category_name',
    ordering = '-id',
    list_per_page = 20
