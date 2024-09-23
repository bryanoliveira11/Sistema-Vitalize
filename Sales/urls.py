from django.urls import path

from Sales import views

app_name = 'sales'

urlpatterns = [
    path('create/', views.CreateSaleClassView.as_view(), name='create'),
]
