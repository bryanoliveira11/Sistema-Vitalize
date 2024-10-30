from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from utils.user_utils import get_notifications


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class NotificationsClassView(View):
    def get(self, *args, **kwargs):
        title = 'Notificações'
        subtitle = 'de Usuário'
        notifications, notifications_total = get_notifications(self.request)

        return render(
            self.request,
            'notifications/pages/notifications.html',
            context={
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'notifications': notifications,
                'notifications_total': notifications_total,
            }
        )
