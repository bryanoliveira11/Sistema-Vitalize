from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Schedules.forms import CreateScheduleForm
from Schedules.models import Schedules
from utils.create_log import create_log
from utils.pagination import make_pagination
from utils.user_utils import get_notifications


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class ShowSchedulesClassView(View):
    def get(self, *args, **kwargs):
        title = 'Meus'
        subtitle = 'Agendamentos'
        user_schedules = Schedules.objects.filter(
            user=self.request.user,
        ).prefetch_related('services').order_by('-pk')

        page_obj, pagination_range = make_pagination(
            self.request, user_schedules, 10
        )

        notifications, notifications_total = get_notifications(self.request)

        return render(
            self.request,
            'schedules/pages/show_schedules.html',
            context={
                'schedules': page_obj,
                'page_obj': page_obj,
                'pagination_range': pagination_range,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'notifications': notifications,
                'notifications_total': notifications_total,
            }
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CreateScheduleClassView(View):
    def render_form(self, form: CreateScheduleForm):
        title = 'Agendamento'
        subtitle = 'de Serviços'
        notifications, notifications_total = get_notifications(self.request)

        return render(
            self.request,
            'schedules/pages/create_schedule.html',
            context={
                'form': form,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'is_creating_schedule': True,
                'notifications': notifications,
                'notifications_total': notifications_total,
            }
        )

    def get(self, *args, **kwargs):
        return self.render_form(form=CreateScheduleForm())
