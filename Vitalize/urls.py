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
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('users/', include('Users.urls')),
    path(
        'accounts/google/login/callback/',
        all_auth_views.oauth2_callback,
        name='google_callback'
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
