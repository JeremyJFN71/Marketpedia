from django.apps import AppConfig


class MarketpediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketpedia'

    def ready(self):
        from . import signals