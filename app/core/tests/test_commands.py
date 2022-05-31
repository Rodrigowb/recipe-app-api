"""
Test custom Django management commands
"""
# Mock behavior of the db
from unittest.mock import patch
# Operartional error that we might ge
from psycopg2 import OperationalError as Psycopg2Error
# Helper function that allow us to call the command that we are testing
from django.core.management import call_command
# Operartional error that we might ge
from django.db.utils import OperationalError
# Base test class
from django.test import SimpleTestCase

# Mock check method to check availability of the db


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        # When we call check, we want it to return true value
        patched_check.return_value = True
        # Execute the code inside the wait_for_db.py
        call_command('wait_for_db')
        # Ensure that the mocked value is called with \
        # the database=['default] parameter
        patched_check.assert_called_once_with(databases=['default'])

    # Mock the db sleep for the connection wait the db to load
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # Call method, the first two times raise the Psycopg2 error \
        # and the next three, OperationalError
        patched_check.side_effect = [
            Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        # Execute the code inside the wait_for_db.py
        call_command('wait_for_db')
        # Call the method equal to the checked above
        self.assertEqual(patched_check.call_count, 6)
        # Ensure that the mocked value is called with \
        # the database=['default] parameter
        patched_check.assert_called_with(databases=['default'])
