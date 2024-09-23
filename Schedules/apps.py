from django.apps import AppConfig


class SchedulesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Schedules'

    def ready(self) -> None:
        import Schedules.signals
        super_ready = super().ready()
        return super_ready
