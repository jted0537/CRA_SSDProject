import os.path

from test_shell_app.Utils.logger import MyLogger


class MessageManager:
    def __init__(self):
        self._classes = ""
        self._func = ""
        self._message = ""
        self._logger = MyLogger()

    @property
    def message(self):
        return self._message

    @property
    def classes(self):
        return self._classes

    @property
    def func(self):
        return self._func

    @message.setter
    def message(self, message):
        self._message = message

    @classes.setter
    def classes(self, classes):
        self._classes = classes

    @func.setter
    def func(self, func):
        self._func = func

    def print(self, *args):
        print(self.message, end="")
        self._logger.logging(self.classes, self.func, self.message.rstrip())


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

    def print(self, *args):
        print(self.message, end="")


class InvalidCommandMessageManager(MessageManager):
    def __init__(self, classes="", func=""):
        super().__init__()
        self.message = "INVALID COMMAND\n"
        self.classes = classes
        self.func = func


class InvalidArgumentMessageManager(MessageManager):
    def __init__(self, classes="", func=""):
        super().__init__()
        self.message = "INVALID PARAMETER\n"
        self.classes = classes
        self.func = func


class ExceptionMessageManager(MessageManager):
    def __init__(self, message="", classes="", func=""):
        super().__init__()
        self.message = message
        self.classes = classes
        self.func = func


class HelpMessageManager(MessageManager):
    def __init__(self):
        super().__init__()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        help_file_path = os.path.abspath(os.path.join(script_dir, "./help.txt"))
        with open(help_file_path, "r", encoding="utf-8") as f:
            self.message = f.read()

    def print(self, *args):
        print(self.message, end="")


class ExitMessageManager(MessageManager):
    def __init__(self, classes="", func=""):
        super().__init__()
        self.message = "Shell Application을 종료합니다.\n"
        self.classes = classes
        self.func = func

    def print(self, *args):
        print(self.message, end="")
