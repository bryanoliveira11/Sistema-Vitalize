from django.urls import path

from Schedules import views

app_name = 'schedules'

urlpatterns = [
    path('', views.ShowSchedulesClassView.as_view(), name='schedules'),
    path(
        'create/select-services/',
        views.ScheduleSelectServicesClassView.as_view(), name='create'
    ),
    path(
        'create/select-date/',
        views.ScheduleSelectDateClassView.as_view(),
        name='create_select-date'
    ),
    path(
        'create/select-time/',
        views.ScheduleSelectTimeClassView.as_view(),
        name='create_select-time'
    ),
]
