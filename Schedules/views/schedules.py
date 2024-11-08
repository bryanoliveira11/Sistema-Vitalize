from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Notifications.models import Notifications
from Schedules.forms import CreateScheduleForm
from Schedules.models import Schedules
from Schedules.templates.schedules.emails.email_templates import \
    schedule_confirmation
from utils.create_log import create_log
from utils.email_service import send_html_mail
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
        ).prefetch_related('services').select_related(
            'schedule_time'
        ).order_by('-pk')

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

    def post(self, *args, **kwargs):
        form = CreateScheduleForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            schedule = form.save(commit=False)
            services = form.cleaned_data.get('services')
            schedule_date = form.cleaned_data.get('schedule_date')
            schedule_time = form.cleaned_data.get('schedule_time')
            schedule.save()

            if not services:
                messages.error(
                    self.request,
                    'Erro ao Realizar Agendamento, Tente Novamente.'
                )
                return redirect(reverse('schedules:schedules'))

            schedule.services.set(services)
            total_price = sum(service.price for service in services)
            schedule.total_price = total_price
            schedule.user = self.request.user
            schedule.save()

            if schedule_time:
                schedule_time.is_picked = True
                schedule_time.save()

            if schedule_date:
                formatted_date = datetime.strptime(
                    str(schedule_date), "%Y-%m-%d"
                ).strftime("%d/%m/%Y")

            messages.success(
                self.request,
                'Agendamento Realizado com Sucesso.'
            )

            Notifications.objects.create(
                user=self.request.user,
                subject='Confirmação de Agendamento',
                text=f'''Olá, {self.request.user} ! </br>
                Seu Agendamento está <b>Marcado</b> para o dia
                <b>{formatted_date if formatted_date else schedule_date}</b>
                às <b>{schedule_time.time if schedule_time else '-'}</b>'''
            )

            send_html_mail(
                subject='Confirmação de Agendamento Vitalize',
                html_content=schedule_confirmation(
                    self.request.user.first_name,  # type:ignore
                    reverse('schedules:schedules'),
                    formatted_date if formatted_date else schedule_date,
                    schedule_time.time if schedule_time else '-'
                ),
                recipient_list=[self.request.user],  # type:ignore
            )

            create_log(
                self.request.user,
                'Agendamento Realizado com Sucesso.',
                'Schedules',
                schedule.pk
            )

            return redirect(reverse('schedules:schedules'))

        return self.render_form(form=form)
