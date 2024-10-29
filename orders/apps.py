from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        # Импортируем сигнал, чтобы он зарегистрировался
        import orders.signals  # Замените на путь к вашему файлу signals.py
