import os
import pickle


class CommandBuffer:
    DEFAULT_BUFFER_FILE_PATH = os.path.join(os.path.dirname(__file__), "buffer.txt")

    def __init__(self, buffer_file_path: str = None):
        self.__buffer_file_path = (
            CommandBuffer.DEFAULT_BUFFER_FILE_PATH
            if buffer_file_path is None
            else buffer_file_path
        )
        self.__init_buffer()

    def insert_cmd(self, *args, **kwargs):
        cmd = (args[0], args[1], args[2])

        buffer_contents = self.__get_buffer_contents()
        buffer_contents.append(cmd)

        self.__update_buffer_contents(buffer_contents)

    def get_value(self, addr: int) -> str:
        pass

    def flush(self):
        pass

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
