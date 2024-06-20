import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(current_dir)
sys.path.append(parent_dir)

from shell import Shell
from Scripts.testapp1 import TestApp1
from Scripts.testapp2 import TestApp2
from Utils.message_manager import *


class ShellMain:
    EXIT_COMMAND = "exit"

    def __init__(self):
        self.command_map = {
            "write": Shell().write,
            "fullwrite": Shell().full_write,
            "read": Shell().read,
            "fullread": Shell().full_read,
            "help": HelpMessageManager().print,
            "exit": ExitMessageManager().print,
            "testapp1": TestApp1().run,
            "testapp2": TestApp2().run,
        }

    def run(self):
        InitMessageManager().print()
        while True:
            user_input = self.get_user_input()
            if not self.execute_method(user_input):
                break

    def execute_method(self, user_input):
        parsed_user_input = self.parse_user_input(user_input)

        command = self.command_map.get(
            parsed_user_input[0],
            InvalidCommandMessageManager(
                message=parsed_user_input[0],
                classes="ShellMain",
                func=f"execute_method('{user_input}')",
            ).print,
        )

        args = tuple(parsed_user_input[1:])
        try:
            command(*args)
        except TypeError:
            InvalidArgumentMessageManager(
                classes="Shell", func=f"{parsed_user_input[0]}{args}"
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
    ShellMain().run()
