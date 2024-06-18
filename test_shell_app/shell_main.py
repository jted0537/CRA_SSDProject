from shell import Shell


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

        self.help_message = (
            "---Shell Application 사용 방법---\n"
            "· write\n"
            "  - LBA 주소에 데이터를 쓴다.\n"
            "  - 포맷) write [LBA 주소] [4byte 데이터]\n"
            "  - 예시) write 3 0xAAAABBBB\n"
            "· fullwrite\n"
            "  - 모든 LBA에 데이터를 쓴다.\n"
            "  - 포맷) fullwrite [4byte 데이터]\n"
            "  - 예시) fullwrite 0xAAAABBBB\n"
            "· read\n"
            "  - LBA 주소의 데이터를 읽는다.\n"
            "  - 포맷) read [LBA 주소]\n"
            "  - 예시) read 3\n"
            "· fullread\n"
            "  - 모든 LBA의 데이터를 읽는다.\n"
            "  - 포맷) fullread\n"
            "· help\n"
            "  - 도움말 메시지를 출력한다.\n"
            "· exit\n"
            "  - 프로그램을 종료한다.\n"
        )

        self.invalid_command_message = "Unknown Command\n"
        self.exit_message = "Shell Application을 종료합니다.\n"

        self.command_map = {
            "write": Shell().write,
            "fullwrite": Shell().full_write,
            "read": Shell().read,
            "fullread": Shell().full_read,
            "help": self.show_help_message,
            "exit": self.show_exit_message,
        }

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
            print("올바른 input parameter를 입력하세요")

        if not user_input[0] == self.EXIT_COMMAND:
            return True

        return False

    def get_user_input(self):
        return input("> ")


if __name__ == "__main__":
    ShellMain().run()
