from django.contrib import admin
from django.contrib.auth import get_user_model

from Schedules.models import Schedules, Services

User = get_user_model()


@admin.register(Schedules)
class AdminVitalizeSchedules(admin.ModelAdmin):
    list_display = 'id', 'user', 'get_services', \
        'total_price', 'schedule_date', 'status',
    list_display_links = 'id',
    search_fields = 'user',
    ordering = '-id',
    list_filter = 'user', 'status', 'services',
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('services').select_related('user')

    def get_services(self, obj):
        services = obj.services.all()
        return ", ".join(
            [service.service_name for service in services]
        ) or 'Nenhum Serviço Escolhido.'
    get_services.short_description = 'Serviço(s)'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "services":
            kwargs["queryset"] = Services.objects.filter(
                is_active=True
            ).order_by('-pk')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(
                is_active=True
            ).order_by('-pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Services)
class AdminVitalizeServices(admin.ModelAdmin):
    list_display = 'id', 'service_name', 'description', 'price', 'is_active',
    list_display_links = 'id', 'service_name',
    list_editable = 'description', 'price', 'is_active',
    search_fields = 'service_name',
    ordering = '-id',
    list_filter = 'service_name',
    list_per_page = 20
