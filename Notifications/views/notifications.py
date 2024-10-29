from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from Notifications.models import Notifications


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class NotificationsClassView(View):
    def get(self, *args, **kwargs):
        title = 'Notificações'
        subtitle = 'de Usuário'
        user = self.request.user
        notifications = Notifications.objects.filter(
            user=user
        ).select_related('user')

        return render(
            self.request,
            'notifications/pages/notifications.html',
            context={
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'notifications': notifications,
            }
        )