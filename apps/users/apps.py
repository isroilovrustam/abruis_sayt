from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Foydalanuvchilar'

    def ready(self):
        """Signallarni import qilish"""
        try:
            import users.models  # noqa: F401
        except ImportError:
            pass