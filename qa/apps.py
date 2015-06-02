from django.apps import AppConfig
from django.conf import settings

from elasticsearch_dsl.connections import connections

class QAConfig(AppConfig):
    name = 'qa'
    verbose_name = "Q & A"

    def ready(self):
        connections.configure(**settings.ES_CONNECTIONS)
