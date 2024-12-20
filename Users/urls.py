from allauth.socialaccount.providers.google import views as all_auth_views
from django.urls import path

from Users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(), name='register'),
    path('login/', views.LoginClassView.as_view(), name='login'),
    path('auto-login/', views.AutoLoginClassView.as_view(), name='auto-login'),
    path('logout/', views.LogoutClassView.as_view(), name='logout'),
    path(
        'admin/options/',
        views.AdminUserOptionsClassView.as_view(),
        name='admin_options'
    ),
    path(
        'accounts/google/login/',
        all_auth_views.oauth2_login,
        name='google_login'
    ),
    path('profile/', views.ProfileClassView.as_view(), name='profile'),
    path(
        'profile/password/',
        views.EditPasswordClassView.as_view(),
        name='profile_password'
    ),
    path(
        'no-permission/',
        views.NoPermissionClassView.as_view(),
        name='no-permission'
    ),
]
