from django.apps import AppConfig


class AppDjangogrammConfig(AppConfig):
    name = 'app_DjangoGramm'

    def ready(self):
        from app_DjangoGramm import signals
