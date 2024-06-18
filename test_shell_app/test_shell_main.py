import io
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

from test_shell_app.shell_main import ShellMain


class TestShellMain(TestCase):
    def setUp(self):
        super().setUp()
        self.shell_main = ShellMain()

    def test_shell_main_operate_correctly(self):
        output = io.StringIO()
        backup = sys.stdout
        sys.stdout = output
        self.shell_main.show_init_message()
        try:
            self.assertEqual(self.shell_main.init_message, output.getvalue())
        finally:
            sys.stdout = backup

    @patch.object(ShellMain, "get_user_input")
    def test_shell_main_invalid_command(self, mock):
        mock.side_effect = ["NO_COMMAND", "exit"]
        output = io.StringIO()
        backup = sys.stdout
        sys.stdout = output
        self.shell_main.run()
        try:
            self.assertTrue(
                self.shell_main.invalid_command_message in output.getvalue()
            )
        finally:
            sys.stdout = backup

    @patch.object(ShellMain, "get_user_input")
    def test_shell_write_command_argument_check(self, mock):
        self.shell_main.command_map["write"] = MagicMock()
        mock.side_effect = ["write 3 0xAAAABBBB", "exit"]
        self.shell_main.run()
        self.shell_main.command_map["write"].assert_called_with("3", "0xAAAABBBB")
