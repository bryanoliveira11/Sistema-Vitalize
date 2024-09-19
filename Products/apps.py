from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Products'

    def ready(self) -> None:
        import Products.signals
        super_ready = super().ready()
        return super_ready
