from test_shell_app.shell import Shell


class ShellMain:
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
            "Exit": Shell().exit,
        }

    def show_init_message(self):
        print(self.init_message, end="")

    def run(self):
        self.show_init_message()
        while True:
            user_input = self.get_user_input()
            if user_input == "Exit":
                break
            command = self.command_map.get(user_input, None)
            args = ()

            if command is None:
                print(self.invalid_command_message)
            else:
                command(*args)

    def get_user_input(self):
        return input("> ")


if __name__ == "__main__":
    ShellMain().run()
