import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Очікування бази даних...')
        while True:
            try:
                conn = connections['default']
                conn.cursor()
                break
            except OperationalError:
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('База даних готова.'))
