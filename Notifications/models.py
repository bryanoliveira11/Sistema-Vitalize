from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notifications(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    subject = models.CharField(max_length=150, verbose_name='Assunto')
    text = models.TextField(max_length=300, verbose_name='Texto')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    def __str__(self) -> str:
        return f'Notificação de {self.user}'

    class Meta:
        verbose_name = f'Notificação'
        verbose_name_plural = 'Notificações'
