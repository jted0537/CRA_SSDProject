from test_shell_app.shell import Shell


class ShellMain:
    EXIT_COMMAND = "Exit"

    def __init__(self):
        self.init_message = (
            "SSD Shell Application\n"
            "---Command List---\n"
            "- Write\n"
            "- FullWrite\n"
            "- Read\n"
            "- FullRead\n"
            "- Help\n"
            "- Exit\n"
        )

        self.invalid_command_message = "Unknown Command"

        self.command_map = {
            "Write": Shell().write,
            "FullWrite": Shell().full_write,
            "Read": Shell().read,
            "FullRead": Shell().full_read,
            "Help": Shell().help,
            "Exit": self.exit,
        }

    def show_init_message(self):
        print(self.init_message, end="")

    def exit(self):
        print("Exit Shell Application")

    def run(self):
        self.show_init_message()
        while True:
            user_input = self.get_user_input()
            if not self.execute_method(user_input):
                break

    def execute_method(self, user_input):
        command = self.command_map.get(user_input, None)
        if command:
            args = ()
            command(*args)
        else:
            print(self.invalid_command_message)

        if not user_input == self.EXIT_COMMAND:
            return True

        return False

    def get_user_input(self):
        return input("> ")


if __name__ == "__main__":
    ShellMain().run()
