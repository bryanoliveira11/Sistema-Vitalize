from django.contrib import admin

from Logs.models import VitalizeLogs


@admin.register(VitalizeLogs)
class AdminVitalizeLog(admin.ModelAdmin):
    list_display = 'id', 'log', 'table_affected', 'created_at',
    list_display_links = 'id',
    search_fields = 'table_affected',
    ordering = '-id',
    list_filter = 'table_affected',
    list_per_page = 20