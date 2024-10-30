from django.urls import path

from Notifications import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationsClassView.as_view(), name='notifications'),
    path(
        'remove/', views.NotificationsRemoveClassView.as_view(),
        name='notifications_remove',
    ),
    path(
        'remove/<int:id>/',
        views.NotificationsRemoveSingleClassView.as_view(),
        name='notifications_remove_single',
    )
]
