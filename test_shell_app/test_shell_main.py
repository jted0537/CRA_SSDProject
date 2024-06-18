import io
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

from shell_main import ShellMain

INVALID_COMMAND = "NO_COMMAND"
EXIT_COMMAND = "exit"


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
        mock.side_effect = [INVALID_COMMAND, EXIT_COMMAND]
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
    def test_shell_command_argument_check(self, mock):
        test_command_map = {
            "write": ("write 3 0xAAAABBBB", (3, "0xAAAABBBB")),
            "read": ("read 3", (3,)),
            "fullwrite": ("fullwrite 0xAAAABBBB", ("0xAAAABBBB",)),
        }
        for command, (full_command, expected_argument) in test_command_map.items():
            with self.subTest(f"{command} called test"):
                self.shell_main.command_map[command] = MagicMock()
                shell_command = self.shell_main.command_map[command]
                mock.side_effect = [full_command, EXIT_COMMAND]

                self.shell_main.run()

                shell_command.assert_called_with(*expected_argument)

    @patch.object(ShellMain, "get_user_input")
    def test_shell_command_with_no_argument_check(self, mock):
        test_command_list = ["fullread", "help", "exit"]

        for command in test_command_list:
            with self.subTest(f"{command} called test"):
                self.shell_main.command_map[command] = MagicMock()
                shell_command = self.shell_main.command_map[command]
                mock.side_effect = [command, EXIT_COMMAND]

                self.shell_main.run()

                shell_command.assert_called_once()
