from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from Schedules.forms import CreateScheduleForm
from utils.create_log import create_log


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class CreateScheduleClassView(View):
    def render_form(self, form: CreateScheduleForm):
        title = 'Agendamento'
        subtitle = 'de Serviços'

        return render(
            self.request,
            'schedules/pages/create_schedule.html',
            context={
                'form': form,
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
                'is_creating_schedule': True,
            }
        )

    def get(self, *args, **kwargs):
        return self.render_form(form=CreateScheduleForm())
