from django.contrib import admin

from Users.models import VitalizeUser


@admin.register(VitalizeUser)
class AdminVitalizeUser(admin.ModelAdmin):
    list_display = 'id', 'email', 'first_name', 'last_name', 'phone_number',
    list_display_links = 'email',
    list_editable = 'first_name', 'last_name', 'phone_number',
    search_fields = 'id', 'email',
    ordering = '-id',
    list_filter = 'is_staff', 'is_superuser'
    list_per_page = 20


# @admin.register(Permissions)
# class AdminPermissions(admin.ModelAdmin):
#     list_display = 'id', 'permission',
#     list_display_links = 'permission',
#     search_fields = 'permission',
#     ordering = '-id',
#     list_per_page = 10
