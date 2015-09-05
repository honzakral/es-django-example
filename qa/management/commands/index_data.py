from __future__ import print_function

import sys
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from elasticsearch_dsl.connections import connections

from elasticsearch.helpers import streaming_bulk

from qa.models import Question, Answer

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.es = connections.get_connection()
        self.es.indices.delete(index=settings.ES_INDEX, ignore=404)
        self.verbose_run(Question)
        self.verbose_run(Answer)

    def verbose_run(self, model, report_every=100):
        name = model._meta.verbose_name
        print('Indexing %s: ' % name, end='')
        start = time.time()
        cnt = 0
        for _  in streaming_bulk(
                self.es,
                (m.to_search() for m in model.objects.all().iterator()),
                index=settings.ES_INDEX,
                doc_type=name.lower(),
            ):
            cnt += 1
            if cnt % report_every:
                print('.', end='')
                sys.stdout.flush()
        print('DONE\nIndexing %d %s in %.2f seconds'% (
            cnt, name, time.time() - start
        ))

