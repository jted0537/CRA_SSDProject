import os
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, log_file="latest.log", max_log_size=10 * 1024):
        self.log_file_path = Path.cwd().parent / "logs" / log_file
        self.ROTATE_SIZE = 2
        self.MAX_LOG_SIZE = max_log_size
        self.make_log_file()

    def make_log_file(self):
        parent_dir = Path.cwd().parent / "logs"
        parent_dir.mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w"):
                pass
            print(f"Log file path: {self.log_file_path}")

    def logging(self, class_name, function_name, contents):
        self.write(class_name, function_name, contents)
        self.rotate()
        self.compress()

    def write(self, class_name, function_name, contents):
        timestamp = datetime.now().strftime("%y.%m.%d %H:%M")

        log_line = (
            f"[{timestamp}] {f'{class_name}.{function_name}'.ljust(30)} : {contents}\n"
        )
        log_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../logs/latest.log"
        )
        with open(log_file, "a") as f:
            f.write(log_line)

    def rotate(self):
        file_size = os.path.getsize(self.log_file_path)
        if file_size > self.MAX_LOG_SIZE:
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"until_{current_datetime}.log"
            new_file_path = self.log_file_path.parent / new_file_name

            os.rename(self.log_file_path, new_file_path)
            print(f"[rotate] {new_file_path} is created.")

        self.make_log_file()

    def compress(self):
        file_list = list(
            map(lambda x: str(x), sorted(self.log_file_path.parent.glob("until_*.log")))
        )

        if len(file_list) >= self.ROTATE_SIZE:
            before_compress = file_list[0]
            after_compress = before_compress.replace(".log", ".zip")

            os.rename(before_compress, after_compress)
            print(f"[compress] {after_compress} is compressed.")
