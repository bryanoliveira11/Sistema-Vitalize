from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VitalizeLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Usuário')
    log = models.TextField(max_length=250, verbose_name='Log')
    table_affected = models.CharField(max_length=150, verbose_name='Tabela Afetada')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    def __str__(self) -> str:
        return f'Log N.{self.pk}'


    class Meta:
        verbose_name = 'Log Vitalize'
        verbose_name_plural = 'Logs Vitalize'