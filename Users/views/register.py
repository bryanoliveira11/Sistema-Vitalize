from django.shortcuts import render
from django.views.generic import View


class RegisterClassView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'home/pages/home.html', {'title': 'Users'})
