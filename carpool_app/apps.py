from django.apps import AppConfig


class CarpoolAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carpool_app'

    def ready(self):
        import carpool_app.signals
