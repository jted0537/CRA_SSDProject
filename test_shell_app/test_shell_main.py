import io
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

from shell_main import ShellMain

INVALID_COMMAND = "NO_COMMAND"
EXIT_COMMAND = "exit"
HELP_COMMAND = "help"


class TestShellMain(TestCase):
    def setUp(self):
        super().setUp()
        self.shell_main = ShellMain()

        self.output = io.StringIO()
        self.stdout_backup = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = self.stdout_backup

    def test_shell_main_operate_correctly(self):
        self.shell_main.show_init_message()

        try:
            self.assertEqual(self.shell_main.init_message, self.output.getvalue())
        finally:
            pass

    @patch.object(ShellMain, "get_user_input")
    def test_shell_exit_operate_correctly(self, mock):
        mock.side_effect = [EXIT_COMMAND]

        self.shell_main.run()

        try:
            self.assertTrue(self.shell_main.exit_message in self.output.getvalue())
        finally:
            pass

    @patch.object(ShellMain, "get_user_input")
    def test_shell_help_operate_correctly(self, mock):
        mock.side_effect = [HELP_COMMAND, EXIT_COMMAND]

        self.shell_main.run()

        try:
            self.assertTrue(self.shell_main.help_message in self.output.getvalue())
        finally:
            pass

    @patch.object(ShellMain, "get_user_input")
    def test_shell_main_invalid_command(self, mock):
        mock.side_effect = [INVALID_COMMAND, EXIT_COMMAND]

        self.shell_main.run()

        try:
            self.assertTrue(
                self.shell_main.invalid_command_message in self.output.getvalue()
            )
        finally:
            pass

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

    @patch.object(ShellMain, "get_user_input")
    def test_shell_main_invalid_input_command(self, mock):
        test_commands = [
            ["write 3", EXIT_COMMAND],
            ["read", EXIT_COMMAND],
            ["read 3 0xAAAABBBB", EXIT_COMMAND],
            ["help 3", EXIT_COMMAND],
            ["write abc 0xAAAABBBB", EXIT_COMMAND],
            ["write  ", EXIT_COMMAND],
        ]

        for test_command in test_commands:
            with self.subTest(f"'{test_command[0]}' test"):
                mock.side_effect = test_command

                self.shell_main.run()
                self.assertTrue(
                    self.shell_main.invalid_argument_message in self.output.getvalue()
                )
