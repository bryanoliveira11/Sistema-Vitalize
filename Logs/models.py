from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class VitalizeLogs(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    log = models.TextField(max_length=250, verbose_name='Log')
    object_id = models.IntegerField(null=True, blank=True)
    table_affected = models.CharField(
        max_length=150, verbose_name='Tabela Afetada')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    def __str__(self) -> str:
        return f'Log N.{self.pk}'

    class Meta:
        verbose_name = 'Log Vitalize'
        verbose_name_plural = 'Logs Vitalize'
