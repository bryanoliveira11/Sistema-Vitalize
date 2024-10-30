from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Notifications.models import Notifications
from utils.pagination import make_pagination
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

        notifications, pagination_range = make_pagination(
            self.request, notifications, 5,
        )

        return render(
            self.request,
            'notifications/pages/notifications.html',
            context={
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'page_obj': notifications,
                'pagination_range': pagination_range,
                'notifications': notifications,
                'notifications_total': notifications_total,
            }
        )


class NotificationsRemoveClassView(View):
    def get(self, *args, **kwargs):
        return redirect(reverse('notifications:notifications'))

    def post(self, *args, **kwargs):
        Notifications.objects.filter(
            user=self.request.user, is_active=True,
        ).update(is_active=False)
        return redirect(reverse('notifications:notifications'))


class NotificationsRemoveSingleClassView(View):
    def get(self, *args, **kwargs):
        return redirect(reverse('notifications:notifications'))

    def post(self, *args, **kwargs):
        notification_id = self.kwargs.get('id')
        Notifications.objects.filter(
            id=notification_id, user=self.request.user, is_active=True,
        ).update(is_active=False)
        return redirect(reverse('notifications:notifications'))
