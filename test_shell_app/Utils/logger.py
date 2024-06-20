import os
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, log_file="latest.log"):
        self.log_file = log_file
        self.log_file_path = ""
        self.make_log_file()

    def make_log_file(self):
        parent_dir = Path(__file__).resolve().parent.parent / "logs"
        parent_dir.mkdir(parents=True, exist_ok=True)
        self.log_file_path = parent_dir / self.log_file

        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w"):
                pass
            print(f"Log file path: {self.log_file_path}")

    def logging(self, class_name, function_name, contents):
        pass

    def write(self, class_name, function_name, contents):
        pass

    def rotate(self):
        file_size = os.path.getsize(self.log_file_path)
        print(f"file size : {file_size}")
        if file_size > 10 * 1024:
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"until_{current_datetime}.log"

            os.rename(
                self.log_file_path,
                os.path.join(os.path.dirname(self.log_file_path), new_file_name),
            )

        self.make_log_file()

    def compress(self):
        pass


