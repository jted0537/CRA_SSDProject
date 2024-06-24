import os
import pickle
import copy
from command_buffer.contents.optimizer import ReduceWriteDuplication


class CommandBuffer:
    DEFAULT_BUFFER_FILE_PATH = os.path.join(os.path.dirname(__file__), "buffer.txt")
    DEFAULT_BUFFER_LENGTH = 10

    def __init__(self, buffer_file_path: str = None):
        self.__buffer_length = CommandBuffer.DEFAULT_BUFFER_LENGTH
        self.__buffer_file_path = (
            CommandBuffer.DEFAULT_BUFFER_FILE_PATH
            if buffer_file_path is None
            else buffer_file_path
        )
        self.__init_buffer()
        self.__optimizer = [
            ReduceWriteDuplication(),
        ]

    def insert_cmd(self, *args, **kwargs) -> list:
        return_buffer_contents = (
            None
            if len(self.__get_buffer_contents()) < self.__buffer_length
            else self.flush()
        )

        buffer_contents = self.__get_buffer_contents()
        cmd = (args[0], args[1], args[2])
        buffer_contents.append(cmd)

        for optimizer in self.__optimizer:
            buffer_contents = optimizer.optimize(buffer_contents)

        self.__update_buffer_contents(buffer_contents)

        return return_buffer_contents

    def get_value(self, addr: int) -> str:
        buffer_contents = self.__get_buffer_contents()
        for cmd, arg1, arg2 in reversed(buffer_contents):
            if cmd == "W" and arg1 == addr:
                return arg2
            elif cmd == "E" and arg1 <= addr < arg1 + arg2:
                return "0x00000000"

        return None

    def flush(self) -> list:
        buffer_contents = self.__get_buffer_contents()
        self.__update_buffer_contents([])

        return buffer_contents

    def __get_buffer_contents(self):
        result = []
        with open(self.__buffer_file_path, "rb") as f:
            result = pickle.load(f)

        return result

    def __update_buffer_contents(self, buffer_contents: list):
        with open(self.__buffer_file_path, "wb") as f:
            pickle.dump(buffer_contents, f)

    def __init_buffer(self):
        if not os.path.exists(self.__buffer_file_path):
            with open(self.__buffer_file_path, "wb") as f:
                pickle.dump([], f)

    # get_buffer_contents is for testing purposes
    def get_buffer_contents(self):
        return self.__get_buffer_contents()
