from django.urls import path

from Reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.SelectReportClassView.as_view(), name='reports'),
    path(
        'cashregister/',
        views.CashRegisterReport.as_view(),
        name='cashregister',
    ),
    path(
        'sales/',
        views.SalesReport.as_view(),
        name='sales',
    ),
    path(
        'prooducts/',
        views.ProductsReport.as_view(),
        name='products',
    )
]
