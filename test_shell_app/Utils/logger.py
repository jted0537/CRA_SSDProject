import os
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, log_file="latest.log", max_log_size=10 * 1024):
        self.log_file = log_file
        self.log_file_path = ""
        self.ROTATE_SIZE = 2
        self.MAX_LOG_SIZE = max_log_size

        self.make_log_file()

    def make_log_file(self):
        parent_dir = Path.cwd().parent / "logs"
        parent_dir.mkdir(parents=True, exist_ok=True)
        self.log_file_path = parent_dir / self.log_file

        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w"):
                pass

    def logging(self, class_name, function_name, contents):
        pass

    def write(self, class_name, function_name, contents):
        pass

    def rotate(self):
        file_size = os.path.getsize(self.log_file_path)
        if file_size > self.MAX_LOG_SIZE:
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"until_{current_datetime}.log"
            new_file_path = Path.cwd().parent / "logs" / new_file_name

            os.rename(self.log_file_path, new_file_path)
            print(f"[rotate] {new_file_path} is created.")

        self.make_log_file()

    def compress(self):
        logs_path = Path.cwd().parent / "logs"
        file_list = list(map(lambda x: str(x), sorted(logs_path.glob("until_*.log"))))

        if len(file_list) >= self.ROTATE_SIZE:
            before_compress = file_list[0]
            after_compress = before_compress.replace(".log", ".zip")

            os.rename(before_compress, after_compress)
            print(f"[compress] {after_compress} is compressed.")


