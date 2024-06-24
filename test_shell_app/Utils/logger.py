import os
from datetime import datetime
from glob import glob


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance._init(*args, **kwargs)
        return cls._instance

    def _init(self, log_file="latest.log", max_log_size=10 * 1024):
        self.log_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../logs"
        )
        self.log_file = os.path.join(self.log_file_path, log_file)

        self.ROTATE_SIZE = 2
        self.MAX_LOG_SIZE = max_log_size
        self.make_log_file()

    def make_log_file(self):
        if not os.path.exists(self.log_file_path):
            os.mkdir(self.log_file_path)

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w"):
                pass

    def logging(self, class_name, function_name, contents):
        self.write(class_name, function_name, contents)
        self.rotate()
        self.compress()

    def write(self, class_name, function_name, contents):
        timestamp = datetime.now().strftime("%y.%m.%d %H:%M")

        log_line = (
            f"[{timestamp}] {f'{class_name}.{function_name}'.ljust(30)} : {contents}\n"
        )
        with open(self.log_file, "a") as f:
            f.write(log_line)

    def rotate(self):
        file_size = os.path.getsize(self.log_file)
        if file_size > self.MAX_LOG_SIZE:
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"until_{current_datetime}.log"
            new_file_path = os.path.join(self.log_file_path, new_file_name)

            os.rename(self.log_file, new_file_path)
            print(f"[rotate] {new_file_path} is created.")

            self.make_log_file()

    def compress(self):
        file_list = sorted(glob(os.path.join(self.log_file_path, "until_*.log")))
        if len(file_list) >= self.ROTATE_SIZE:
            before_compress = file_list[0]
            after_compress = before_compress.replace(".log", ".zip")

            os.rename(before_compress, after_compress)
            print(f"[compress] {after_compress} is compressed.")
