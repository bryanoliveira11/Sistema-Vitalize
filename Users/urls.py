from django.urls import path

from Users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(), name='register'),
]
