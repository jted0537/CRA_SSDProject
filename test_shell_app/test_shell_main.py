import io
import sys
from unittest import TestCase

from test_shell_app.shell_main import ShellMain


class TestShellMain(TestCase):
    def test_shell_main_operate_correctly(self):
        output = io.StringIO()
        backup = sys.stdout
        sys.stdout = output
        shell = ShellMain()
        shell.show_init_message()
        try:
            self.assertEqual(shell.init_message, output.getvalue())
        finally:
            sys.stdout = backup
