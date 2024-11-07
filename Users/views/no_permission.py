from django.shortcuts import render
from django.views.generic import View


class NoPermissionClassView(View):
    def get(self, *args, **kwargs):
        title = 'Permissões'
        subtitle = 'Insuficientes'

        return render(
            self.request,
            'users/pages/no_permission.html',
            {
                'site_title': f'{title} {subtitle}',
                'page_title': title,
                'page_subtitle': subtitle,
            }
        )
