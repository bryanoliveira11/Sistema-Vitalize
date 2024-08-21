from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def login_cancelled(request):
    messages.success(request, 'Login com Google Cancelado.')
    return redirect(reverse('users:login'))
