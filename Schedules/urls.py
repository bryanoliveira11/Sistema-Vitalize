from django.urls import path

from Schedules import views

app_name = 'schedules'

urlpatterns = [
    path('create/', views.CreateScheduleClassView.as_view(), name='create')
    # path(
    #     'cancel/<int:id>', views.CancelScheduleClassView.as_view(), name='cancel'
    # ),
]
