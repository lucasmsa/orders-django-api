import time
from psycopg2 import OperationalError as Psycopg2OperationalError
from django.db.utils import OperationalError as DjangoOperationalError
from django.core.management.base import BaseCommand 

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("🔄 Waiting for database...")
        database_up = False
        while database_up is False:
            try:
                self.check(databases=['default'])
                database_up = True
            except (Psycopg2OperationalError, DjangoOperationalError):
                self.stdout.write("❌ Database unavailable, waiting 1 second...")
                time.sleep(1)
                
        self.stdout.write(self.style.SUCCESS('Database available!'))