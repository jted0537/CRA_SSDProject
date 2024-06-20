import os
from datetime import datetime


class MyLogger:
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
