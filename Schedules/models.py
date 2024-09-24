from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError

from utils.resize_image import resize_image

User = get_user_model()


class Services(models.Model):
    service_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )
    description = models.CharField(
        max_length=150, null=False, blank=False, verbose_name='Descrição'
    )
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Preço (R$)'
    )
    cover_path = models.ImageField(
        upload_to='services/%Y/%m/%d/', null=False,
        blank=False, verbose_name='Imagem do Serviço'
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Ativo/Inativo',
        help_text='Marque Essa Caixa para Ativar esse Serviço. '
        'Desmarque para Inativar.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'{self.service_name}'

    def clean(self) -> None:
        cleaned_data = super().clean()
        errors = {}

        if float(self.price) <= 0:
            errors['price'] = 'Digite um Número Positivo.'

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.cover_path:
            try:
                resize_image(self.cover_path, new_width=840)
            except FileNotFoundError:
                ...

        return saved

    class Meta:
        verbose_name = 'Serviço Vitalize'
        verbose_name_plural = 'Serviços Vitalize'


class Schedules(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Usuario', null=True, on_delete=models.PROTECT
    )
    services = models.ManyToManyField(Services, verbose_name="Serviço")
    schedule_date = models.DateTimeField(
        null=False, blank=False, verbose_name='Data e Hora'
    )
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='Preço Total (R$)',
        editable=False,
    )
    status = models.BooleanField(
        default=True, verbose_name='Status',
        help_text='Marcado/Desmarcado',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'Agendamento Nº {self.pk} ({self.user})'

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = 0
        super().save(*args, **kwargs)
        self.update_total_price()

    def update_total_price(self):
        total = self.services.aggregate(total_price=models.Sum('price'))[
            'total_price'] or 0
        Schedules.objects.filter(pk=self.pk).update(total_price=total)

    class Meta:
        verbose_name = 'Agendamento Vitalize'
        verbose_name_plural = 'Agendamentos Vitalize'
