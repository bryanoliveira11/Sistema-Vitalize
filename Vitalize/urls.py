"""
URL configuration for Vitalize project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.providers.google import views as all_auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Users.views.all_auth import account_signup, login_cancelled

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Products.urls')),
    path('users/', include('Users.urls')),
    path('sales/', include('Sales.urls')),
    path('cashregister/', include('CashRegister.urls')),
    path(
        'accounts/google/login/callback/',
        all_auth_views.oauth2_callback,
        name='google_callback'
    ),
    path(
        'accounts/social/login/cancelled/',
        login_cancelled,
        name='socialaccount_login_cancelled'
    ),
    path('accounts/signup/', account_signup, name='account_signup'),
    path(
        'accounts/social/signup/', account_signup, name='socialaccount_signup'
    ),
    path("select2/", include("django_select2.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
