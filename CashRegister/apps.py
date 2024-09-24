from django.apps import AppConfig


class CashregisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CashRegister'

    def ready(self) -> None:
        import CashRegister.signals
        super_ready = super().ready()
        return super_ready
