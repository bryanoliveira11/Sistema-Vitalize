from django.contrib import admin

from Schedules.models import Schedules, Services


@admin.register(Schedules)
class AdminVitalizeSchedules(admin.ModelAdmin):
    list_display = 'id', 'user', 'schedule_date', 'status',
    list_display_links = 'id', 'user',
    search_fields = 'user',
    ordering = '-id',
    list_filter = 'user', 'status',
    list_per_page = 20


@admin.register(Services)
class AdminVitalizeServices(admin.ModelAdmin):
    list_display = 'id', 'service_name', 'price', 
    list_display_links = 'id', 'service_name',
    search_fields = 'service_name',
    ordering = '-id',
    list_filter = 'service_name',
    list_per_page = 20