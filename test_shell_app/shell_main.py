from Utils.message_manager import *
from Utils.shell_main_command import get_shell_main_command
from runner import main as runner_main
import sys


class ShellMain:
    EXIT_COMMAND = "exit"

    def run(self):
        InitMessageManager().print()
        while True:
            user_input = self.get_user_input()
            if not self.execute_method(user_input):
                break

    def get_command(self, command):
        return get_shell_main_command(command)

    def execute_method(self, user_input):
        parsed_user_input = self.parse_user_input(user_input)
        command = self.get_command(parsed_user_input[0])

        args = tuple(parsed_user_input[1:])
        try:
            command.act(*args)
        except TypeError:
            InvalidArgumentMessageManager(
                classes=command.__class__.__name__,
                func=f"{parsed_user_input[0]}{args}",
            ).print()

        if not user_input == self.EXIT_COMMAND:
            return True

        return False

    def parse_user_input(self, user_input):
        user_input = user_input.split(" ")
        for i, one_input in enumerate(user_input):
            try:
                user_input[i] = int(one_input)
            except:
                pass
        return user_input

    def get_user_input(self):
        return input("> ")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        runner_main(sys.argv)
    else:
        ShellMain().run()
