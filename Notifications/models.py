from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Notifications(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    subject = models.CharField(max_length=150, verbose_name='Assunto')
    text = models.TextField(max_length=300, verbose_name='Texto')
    is_active = models.BooleanField(
        default=True, verbose_name='Ativo/Inativo',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    def __str__(self) -> str:
        return f'Notificação de {self.user}'

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
