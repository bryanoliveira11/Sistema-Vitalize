from django.contrib import admin

from Users.models import VitalizeUser


@admin.register(VitalizeUser)
class AdminVitalizeUser(admin.ModelAdmin):
    list_display = 'id', 'email', 'first_name', 'last_name', \
        'phone_number', 'is_active', 'is_staff', 'is_superuser',
    list_display_links = 'email',
    search_fields = 'email',
    ordering = '-id',
    list_filter = 'is_staff', 'is_superuser'
    readonly_fields = 'email', 'first_name', 'last_name', \
        'phone_number', 'last_login',
    exclude = ('password',)
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return False
