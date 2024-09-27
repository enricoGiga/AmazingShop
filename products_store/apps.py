from django.apps import AppConfig


class ProductsStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_store'

    def ready(self):
        import products_store.signals  # Register the signals

