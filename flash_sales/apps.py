from django.apps import AppConfig


class FlashSalesConfig(AppConfig):
    name = 'flash_sales'

    def ready(self):
        import flash_sales.signals
