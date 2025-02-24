"""
Test custom django management commands

"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error


from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
#  we're mocking this command, check method
class CommandTests(SimpleTestCase):
    """
    Test commands.
    """

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database of database ready.
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=["default"])
        # we want to ensure that the command has been called with theese params

    @patch('time.sleep')  # decorators apply arguments inside-out
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when getting OperationalError
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # side effect allows to handle different type
        # the first 2 times we raise Psycopg2Error,next 3 times Op. error
        # sixth time, we're gonna get true value

        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
