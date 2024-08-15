from allauth.socialaccount.providers.google import views as all_auth_views
from django.urls import path

from Users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(), name='register'),
    path('login/', views.LoginClassView.as_view(), name='login'),
    path('logout/', views.LogoutClassView.as_view(), name='logout'),
    path(
        'accounts/google/login/',
        all_auth_views.oauth2_login,
        name='google_login'
    ),
]
