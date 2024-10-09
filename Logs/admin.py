from django.contrib import admin

from Logs.models import VitalizeLogs


@admin.register(VitalizeLogs)
class AdminVitalizeLog(admin.ModelAdmin):
    list_display = 'id', 'user', 'log', 'table_affected', 'created_at',
    list_display_links = 'id', 'user',
    search_fields = 'table_affected',
    ordering = '-id',
    list_filter = 'table_affected',
    list_per_page = 20

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return False
