from Scripts.testapp1 import TestApp1
from Scripts.testapp2 import TestApp2
from Utils.message_manager import *
from shell import Shell


class ShellMainCommand:
    def __init__(self, command_text, action):
        self.command_text = command_text
        self.action = action

    def act(self, *args):
        self.action(*args)


class WriteCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("write", Shell().write)


class FullWriteCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("fullwrite", Shell().full_write)


class ReadCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("read", Shell().read)


class FullReadCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("fullread", Shell().full_read)


class EraseCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("erase", Shell().erase)


class EraseRangeCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("erase_range", Shell().erase_range)


class FlushCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("flush", Shell().flush)


class HelpCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("help", HelpMessageManager().print)


class ExitCommand(ShellMainCommand):
    def __init__(self):
        super().__init__("exit", ExitMessageManager().print)


class TestApp1Command(ShellMainCommand):
    def __init__(self):
        super().__init__("testapp1", TestApp1().run)


class TestApp2Command(ShellMainCommand):
    def __init__(self):
        super().__init__("testapp2", TestApp2().run)


class InvalidCommand(ShellMainCommand):
    def __init__(self, command):
        super().__init__(
            "arbitrary",
            InvalidCommandMessageManager(
                message=command,
                classes="ShellMain",
                func=f"execute_method('{command}')",
            ).print,
        )


def get_shell_main_command(command):
    return {
        "write": WriteCommand(),
        "fullwrite": FullWriteCommand(),
        "read": ReadCommand(),
        "fullread": FullReadCommand(),
        "erase": EraseCommand(),
        "erase_range": EraseRangeCommand(),
        "flush": FlushCommand(),
        "help": HelpCommand(),
        "exit": ExitCommand(),
        "testapp1": TestApp1Command(),
        "testapp2": TestApp2Command(),
    }.get(command, InvalidCommand(command))
