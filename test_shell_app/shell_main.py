from shell import Shell
from testapp1 import TestApp1
from testapp2 import TestApp2
import os.path


class ShellMain:
    EXIT_COMMAND = "exit"

    def __init__(self):
        self.init_message = (
            "SSD Shell Application\n"
            "---Command List---\n"
            "- write\n"
            "- fullwrite\n"
            "- read\n"
            "- fullread\n"
            "- help\n"
            "- exit\n"
            "---Test Command List---\n"
            "- testapp1\n"
            "- testapp2\n"
        )

        self.set_help_message()
        self.invalid_command_message = "INVALID COMMAND\n"
        self.invalid_argument_message = "INVALID PARAMETER\n"
        self.exit_message = "Shell Application을 종료합니다.\n"

        self.command_map = {
            "write": Shell().write,
            "fullwrite": Shell().full_write,
            "read": Shell().read,
            "fullread": Shell().full_read,
            "help": self.show_help_message,
            "exit": self.show_exit_message,
            "testapp1": TestApp1().run,
            "testapp2": TestApp2().run,
        }

    def set_help_message(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        help_file_path = os.path.abspath(os.path.join(script_dir, "./help.txt"))

        with open(help_file_path, "r", encoding="utf-8") as f:
            self.help_message = f.read()

    def show_init_message(self):
        print(self.init_message, end="")

    def show_invalid_command_message(self):
        print(self.invalid_command_message, end="")

    def show_help_message(self):
        print(self.help_message, end="")

    def show_exit_message(self):
        print(self.exit_message, end="")

    def run(self):
        self.show_init_message()
        while True:
            user_input = self.get_user_input()
            if not self.execute_method(user_input):
                break

    def execute_method(self, user_input):
        user_input = user_input.split(" ")
        command = self.command_map.get(user_input[0], self.show_invalid_command_message)

        for i, one_input in enumerate(user_input):
            try:
                user_input[i] = int(one_input)
            except:
                pass

        args = tuple(user_input[1:])
        try:
            command(*args)
        except TypeError:
            print(self.invalid_argument_message)

        if not user_input[0] == self.EXIT_COMMAND:
            return True

        return False

    def get_user_input(self):
        return input("> ")


if __name__ == "__main__":
    ShellMain().run()
