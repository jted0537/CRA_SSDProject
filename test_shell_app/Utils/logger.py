import os
from pathlib import Path
from datetime import datetime


class MyLogger:
    def __init__(self, log_file="latest.log"):
        self.log_file = log_file
        self.make_log_file()

    def make_log_file(self):
        parent_dir = Path(__file__).resolve().parent.parent / "logs"
        parent_dir.mkdir(parents=True, exist_ok=True)
        log_file_path = parent_dir / self.log_file

        if not os.path.exists(log_file_path):
            with open(log_file_path, "w"):
                pass
            print(f"Log file path: {log_file_path}")
            
    def logging(self, class_name, function_name, contents):
        self.write(class_name, function_name, contents)

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
        pass
