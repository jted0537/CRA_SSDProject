import os.path


class MessageManager:
    def __init__(self):
        self._message = ""

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    def print(self, *args):
        print(self.message, end="")


class InitMessageManager(MessageManager):
    def __init__(self):
        super().__init__()
        self.message = (
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


class InvalidCommandMessageManager(MessageManager):
    def __init__(self):
        super().__init__()
        self.message = "INVALID COMMAND\n"


class InvalidArgumentMessageManager(MessageManager):
    def __init__(self):
        super().__init__()
        self.message = "INVALID PARAMETER\n"


class HelpMessageManager(MessageManager):
    def __init__(self):
        super().__init__()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        help_file_path = os.path.abspath(os.path.join(script_dir, "./help.txt"))
        with open(help_file_path, "r", encoding="utf-8") as f:
            self.message = f.read()


class ExitMessageManager(MessageManager):
    def __init__(self):
        super().__init__()
        self.message = "Shell Application을 종료합니다.\n"