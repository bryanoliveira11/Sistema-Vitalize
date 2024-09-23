from django.contrib import admin

from Users.models import VitalizeUser


@admin.register(VitalizeUser)
class AdminVitalizeUser(admin.ModelAdmin):
    list_display = 'id', 'email', 'first_name', 'last_name', \
        'phone_number', 'is_active', 'is_staff', 'is_superuser',
    list_display_links = 'email',
    list_editable = 'first_name', 'last_name', 'phone_number',
    search_fields = 'id', 'email',
    ordering = '-id',
    list_filter = 'is_staff', 'is_superuser'
    list_per_page = 20
