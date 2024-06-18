from test_shell_app.shell import Shell


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
        )

        self.invalid_command_message = "Unknown Command"

        self.command_map = {
            "write": Shell().write,
            "fullwrite": Shell().full_write,
            "read": Shell().read,
            "fullread": Shell().full_read,
            "help": Shell().help,
            "exit": Shell().exit,
        }

    def show_init_message(self):
        print(self.init_message, end="")

    def run(self):
        self.show_init_message()
        while True:
            user_input = self.get_user_input()
            if not self.execute_method(user_input):
                break

    def execute_method(self, user_input):
        user_input = user_input.split(" ")
        command = self.command_map.get(user_input[0], None)
        if command:
            args = tuple(user_input[1:])
            command(*args)
        else:
            print(self.invalid_command_message)

        if not user_input[0] == self.EXIT_COMMAND:
            return True

        return False

    def get_user_input(self):
        return input("> ")


if __name__ == "__main__":
    ShellMain().run()
