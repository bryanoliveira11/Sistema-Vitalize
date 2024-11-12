from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Notifications.models import Notifications
from Schedules.forms import (ScheduleSelectDateForm,
                             ScheduleSelectServicesForm,
                             ScheduleSelectTimeForm)
from Schedules.models import ScheduleDateTime, Schedules, ScheduleTime
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
            self.request, user_schedules, 15
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
class ScheduleBaseClassView(View):
    def validate_session_data(self):
        if 'schedule_data' not in self.request.session:
            messages.info(
                self.request,
                'Selecione os Serviços Desejados antes de Prosseguir.'
            )
            return False
        return True

    def render_form(
        self, form: ScheduleSelectServicesForm
        | ScheduleSelectDateForm | ScheduleSelectTimeForm,
        title: str, subtitle: str, pageAttr: str,
        button_html: str, is_services_form: bool = False,
    ):

        notifications, notifications_total = get_notifications(self.request)

        return render(
            self.request,
            'schedules/pages/create_schedule.html',
            context={
                'form': form,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'pageAttr': pageAttr,
                'button_html': button_html,
                'is_services_form': is_services_form,
                'is_creating_schedule': True,
                'notifications': notifications,
                'notifications_total': notifications_total,
            }
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class ScheduleSelectServicesClassView(ScheduleBaseClassView):
    def get(self, *args, **kwargs):
        return self.render_form(
            form=ScheduleSelectServicesForm(), pageAttr='select-services',
            title='Seleção', subtitle='de Serviços', is_services_form=True,
            button_html='Avançar <i class="fa-regular fa-circle-right"></i>'
        )

    def post(self, *args, **kwargs):
        form = ScheduleSelectServicesForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            services = form.cleaned_data.get('services')

            if not services:
                messages.error(
                    self.request,
                    'Erro ao Realizar Agendamento, Tente Novamente.'
                )
                return redirect(reverse('schedules:schedules'))

            if 'schedule_data' not in self.request.session:
                self.request.session['schedule_data'] = {}

            total_price = sum(service.price for service in services)

            self.request.session['schedule_data']['services'] = list(
                services.values_list('id', flat=True)
            )
            self.request.session['schedule_data']['total_price'] = \
                "{:.2f}".format(total_price)

            self.request.session.modified = True

            return redirect(reverse('schedules:create_select-date'))

        return self.render_form(
            form=form, title='Seleção', pageAttr='select-services',
            subtitle='de Serviços', is_services_form=True,
            button_html='Avançar <i class="fa-regular fa-circle-right"></i>'
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class ScheduleSelectDateClassView(ScheduleBaseClassView):
    def get(self, *args, **kwargs):
        if not self.validate_session_data():
            return redirect(reverse('schedules:create'))

        return self.render_form(
            form=ScheduleSelectDateForm(),
            title='Seleção', subtitle='de Data', pageAttr='select-date',
            button_html='Avançar <i class="fa-regular fa-circle-right"></i>'
        )

    def post(self, *args, **kwargs):
        form = ScheduleSelectDateForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if not self.validate_session_data():
            return redirect(reverse('schedules:create'))

        if form.is_valid():
            schedule_date = form.cleaned_data.get('schedule_date')

            if not schedule_date:
                messages.error(
                    self.request,
                    'Erro ao Realizar Agendamento, Tente Novamente.'
                )
                return redirect(reverse('schedules:schedules'))

            date = schedule_date.strftime("%Y-%m-%d")
            self.request.session['schedule_data']['date'] = date

            formatted_date = schedule_date.strftime("%d/%m/%Y")
            self.request.session['schedule_data']['formatted_date'] = \
                formatted_date

            self.request.session.modified = True

            return redirect(reverse('schedules:create_select-time'))

        return self.render_form(
            form=form,
            title='Seleção', subtitle='de Data', pageAttr='select-date',
            button_html='Avançar <i class="fa-regular fa-circle-right"></i>'
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class ScheduleSelectTimeClassView(ScheduleBaseClassView):
    def get(self, *args, **kwargs):
        if not self.validate_session_data():
            return redirect(reverse('schedules:create'))

        selected_date = self.request.session['schedule_data']['date']

        if not selected_date:
            messages.error(
                self.request,
                'Erro ao Realizar Agendamento, Tente Novamente.'
            )
            return redirect(reverse('schedules:create'))

        selected_times = ScheduleDateTime.objects.filter(
            date=selected_date
        )
        selected_time_ids = selected_times.values_list('time', flat=True)
        times_available = ScheduleTime.objects.filter(
            is_active=True
        ).exclude(id__in=selected_time_ids).order_by('time')

        if not times_available:
            messages.info(
                self.request,
                'Nenhum Horário Disponível foi '
                'Encontrado para a Data Selecionada.'
            )
            return redirect(reverse('schedules:create_select-date'))

        return self.render_form(
            form=ScheduleSelectTimeForm(selected_date),
            title='Seleção', subtitle='de Horário', pageAttr='select-time',
            button_html='Agendar <i class="fa-regular fa-calendar-check"></i>'
        )

    def post(self, *args, **kwargs):
        if not self.validate_session_data():
            return redirect(reverse('schedules:create'))

        selected_date = self.request.session['schedule_data']['date']

        if not selected_date:
            messages.error(
                self.request,
                'Erro ao Realizar Agendamento, Tente Novamente.'
            )
            return redirect(reverse('schedules:create'))

        form = ScheduleSelectTimeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            selected_date=selected_date
        )

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule_time = form.cleaned_data.get('schedule_time')
            services = self.request.session['schedule_data']['services']
            total_price = self.request.session['schedule_data']['total_price']
            date = self.request.session['schedule_data']['date']
            schedule.schedule_date = date
            schedule.save()

            if not schedule_time:
                messages.error(
                    self.request,
                    'Erro ao Realizar Agendamento, Tente Novamente.'
                )
                return redirect(reverse('schedules:schedules'))

            schedule.services.set(services)
            schedule.total_price = total_price
            schedule.user = self.request.user
            schedule.save()

            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")

            messages.success(
                self.request,
                'Agendamento Realizado com Sucesso.'
            )

            ScheduleDateTime.objects.create(
                time=schedule_time,
                date=date,
            )

            Notifications.objects.create(
                user=self.request.user,
                subject='Confirmação de Agendamento',
                text=f'''Olá, {self.request.user} ! </br>
                Seu Agendamento está <b>Marcado</b> para o dia
                <b>{formatted_date if formatted_date else date}</b>
                às <b>{schedule_time.time if schedule_time else '-'}</b>'''
            )

            send_html_mail(
                subject='Confirmação de Agendamento Vitalize',
                html_content=schedule_confirmation(
                    self.request.user.first_name,  # type:ignore
                    reverse('schedules:schedules'),
                    formatted_date if formatted_date else date,
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

            del (self.request.session['schedule_data'])

            return redirect(reverse('schedules:schedules'))

        return self.render_form(
            form=form,
            title='Seleção', subtitle='de Data', pageAttr='select-time',
            button_html='Agendar <i class="fa-regular fa-calendar-check"></i>'
        )
