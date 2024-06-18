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
            user_input = input("> ")
            command = self.command_map.get(user_input, None)
            args = ()

            if command is None:
                break
            else:
                command(*args)


if __name__ == "__main__":
    ShellMain().run()
