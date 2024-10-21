from django.urls import path

from Reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.SelectReportClassView.as_view(), name='reports'),
]
