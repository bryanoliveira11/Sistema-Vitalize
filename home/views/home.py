from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View


class HomePage(View):
    def get(self, *args, **kwargs):
        title = 'Vitrine'
        subtitle = 'de Produtos'

        return render(
            self.request,
            'home/pages/home.html',
            {
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
