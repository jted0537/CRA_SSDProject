from Scripts.testapp1 import TestApp1
from Scripts.testapp2 import TestApp2
from Utils.message_manager import *
from shell import Shell


class CommandManager:
    def __init__(self, command_text, action):
        self.command_text = command_text
        self.action = action

    def act(self, *args):
        self.action(*args)


class WriteCommand(CommandManager):
    def __init__(self):
        super().__init__("write", Shell().write)


class FullWriteCommand(CommandManager):
    def __init__(self):
        super().__init__("fullwrite", Shell().full_write)


class ReadCommand(CommandManager):
    def __init__(self):
        super().__init__("read", Shell().read)


class FullReadCommand(CommandManager):
    def __init__(self):
        super().__init__("fullread", Shell().full_read)


class EraseCommand(CommandManager):
    def __init__(self):
        super().__init__("erase", Shell().erase)


class EraseRangeCommand(CommandManager):
    def __init__(self):
        super().__init__("erase_range", Shell().erase_range)


class FlushCommand(CommandManager):
    def __init__(self):
        super().__init__("flush", Shell().flush)


class HelpCommand(CommandManager):
    def __init__(self):
        super().__init__("help", HelpMessageManager().print)


class ExitCommand(CommandManager):
    def __init__(self):
        super().__init__("exit", ExitMessageManager().print)


class TestApp1Command(CommandManager):
    def __init__(self):
        super().__init__("testapp1", TestApp1().run)


class TestApp2Command(CommandManager):
    def __init__(self):
        super().__init__("testapp2", TestApp2().run)


class InvalidCommand(CommandManager):
    def __init__(self, command):
        super().__init__(
            "arbitrary",
            InvalidCommandMessageManager(
                message=command,
                classes="ShellMain",
                func=f"execute_method('{command}')",
            ).print,
        )


def command_factory(command):
    if command == "write":
        return WriteCommand()
    elif command == "fullwrite":
        return FullWriteCommand()
    elif command == "read":
        return ReadCommand()
    elif command == "fullread":
        return FullReadCommand()
    elif command == "erase":
        return EraseCommand()
    elif command == "erase_range":
        return EraseRangeCommand()
    elif command == "flush":
        return FlushCommand()
    elif command == "help":
        return HelpCommand()
    elif command == "exit":
        return ExitCommand()
    elif command == "testapp1":
        return TestApp1Command()
    elif command == "testapp2":
        return TestApp2Command()
    else:
        return InvalidCommand(command)
