from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def login_cancelled(request):
    if not request.user.is_authenticated:
        messages.success(request, 'Login com Google Cancelado.')
    return redirect(reverse('users:login'))


def account_signup(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, 'Já Existe uma Conta com Esse Endereço de E-mail. '
            'Por Favor, Faça Login na Conta Existente.'
        )
    return redirect(reverse('users:login'))
