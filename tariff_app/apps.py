from django.apps import AppConfig


class TariffAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tariff_app'

from django.core.signals import request_finished
from django.db import connection

def close_db_connection(sender, **kwargs):
    connection.close()

request_finished.connect(close_db_connection)
