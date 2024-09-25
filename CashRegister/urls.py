from django.urls import path

from CashRegister import views

app_name = 'cashregister'

urlpatterns = [
    path('', views.CashRegisterClassView.as_view(), name='cashregister'),
    path(
        'open/',
        views.CashRegisterOpenClassView.as_view(),
        name='cashregister_open'
    ),
    path(
        'close/',
        views.CashRegisterCloseClassView.as_view(),
        name='cashregister_close'
    ),
    path(
        'cashout/',
        views.CashOutClassView.as_view(),
        name='cashout'
    ),
]
