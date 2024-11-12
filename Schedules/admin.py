from django.contrib import admin
from django.contrib.auth import get_user_model

from Schedules.models import Schedules, ScheduleTime, Services

User = get_user_model()


@admin.register(Schedules)
class AdminVitalizeSchedules(admin.ModelAdmin):
    list_display = 'id_text', 'user', 'get_services', \
        'price_in_BRL', 'schedule_date', 'status', 'canceled',
    list_display_links = 'id_text',
    ordering = '-id',
    list_filter = 'user', 'status', 'services', 'schedule_date',
    readonly_fields = 'id_text', 'user', 'services', 'total_price', \
        'schedule_date', 'schedule_time', 'status',
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

    def price_in_BRL(self, obj):
        return f'R$ {obj.total_price}' if obj.total_price \
            is not None else f'R$ {0}'
    price_in_BRL.short_description = 'Preço Total'

    def id_text(self, obj):
        return f'Agendamento Nº {obj.pk}'
    id_text.short_description = 'Agendamento'

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return False

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
    list_display = 'id', 'service_name', 'description', \
        'price_in_BRL', 'is_active',
    list_display_links = 'id', 'service_name',
    list_editable = 'description', 'is_active',
    search_fields = 'service_name',
    ordering = '-id',
    list_filter = 'service_name', 'is_active',
    list_per_page = 20

    def price_in_BRL(self, obj):
        return f'R$ {obj.price}' if obj.price \
            is not None else f'R$ {0}'
    price_in_BRL.short_description = 'Preço'

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(ScheduleTime)
class AdminVitalizeScheduleTimes(admin.ModelAdmin):
    list_display = 'id', 'time', 'is_active',
    list_display_links = 'id', 'time',
    list_editable = 'is_active',
    ordering = '-id',
    list_filter = 'is_active',
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_delete_permission(request, obj)
