from django.apps import AppConfig


class EytConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eyt'

    def ready(self):
        # Import signals here to connect them
        import eyt.signals
    
    



