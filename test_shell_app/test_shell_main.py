import io
import sys
from unittest import TestCase
from unittest.mock import patch

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

    @patch.object(ShellMain, "get_user_input")
    def test_shell_main_invalid_command(self, mock):
        mock.side_effect = ["NO_COMMAND", "Exit"]
        output = io.StringIO()
        backup = sys.stdout
        sys.stdout = output
        shell = ShellMain()
        shell.run()
        try:
            self.assertTrue(shell.invalid_command_message in output.getvalue())
        finally:
            sys.stdout = backup
