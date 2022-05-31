"""
Django command to wait for the database to be available
"""
# Sleep execution
import time
# Error when db is not ready
from psycopg2 import OperationalError as Psycopg20pError
# Error when db is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to wait for db """

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for db')
        db_up = False
        while db_up is False:
            try:
                # If the db is ready, the db_up will be true
                self.check(databases=['default'])
                db_up = True
            except (Psycopg20pError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second ...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
