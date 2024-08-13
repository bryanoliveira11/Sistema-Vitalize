from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages
from Users.forms import RegisterForm
from django.shortcuts import redirect

class RegisterClassView(View):
    def get(self, *args, **kwargs):
        title = 'Cadastro'
        subtitle = 'de Usuário'
        register_data = self.request.session.get('register_data', None)
        form = RegisterForm(register_data)

        return render(
            self.request,
            'users/pages/register.html',
            {
                'site_title': title,
                'page_title': title,
                'page_subtitle': subtitle,
                'btn_text': 'Cadastrar',
                'form': form,
                'form_action': reverse('users:register'),
            }
        )

    def post(self, *args, **kwargs):
        POST = self.request.POST
        self.request.session['register_data'] = POST

        form = RegisterForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)  
            user.save() 

            messages.success(
                self.request,
                'Usuário Cadastrado com Sucesso ! Por Favor Faça seu Login.'
            )

            del (self.request.session['register_data'])

            return redirect(reverse('users:login'))
        
        return redirect(reverse('users:register'))