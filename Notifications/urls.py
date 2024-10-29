from django.urls import path

from Notifications import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationsClassView.as_view(), name='notifications'),
]
