from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Sales'

    def ready(self) -> None:
        import Sales.signals
        super_ready = super().ready()
        return super_ready
