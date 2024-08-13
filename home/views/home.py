from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages


class HomePage(View):
    def get(self, *args, **kwargs):
        title = 'Vitrine'
        subtitle = 'de Produtos'

        messages.success(self.request, 'mensagem de teste')
        messages.error(self.request, 'mensagem de teste')
        messages.info(self.request, 'mensagem de teste')
        messages.warning(self.request, 'mensagem de teste')

        return render(
            self.request,
            'home/pages/home.html',
            {
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
