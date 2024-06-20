import os.path
import re
from subprocess import PIPE, Popen

from Utils.message_manager import (
    InvalidArgumentMessageManager,
    ExceptionMessageManager,
    FileMessageManager,
)


class Shell:
    MAX_ADDR = 100
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

    def get_absolute_path(self, relative_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(script_dir, relative_path))
        return file_path

    def is_valid_addr_parameter(self, addr):
        if addr < 0 or addr > 99:
            return False
        return True

    def is_valid_val_parameter(self, val):
        pattern = r"^0x[A-F0-9]{8}$"
        if not re.match(pattern, val):
            return False
        return True

    def write(self, addr, val):
        if not self.is_valid_addr_parameter(addr):
            InvalidArgumentMessageManager(
                classes=self.__class__.__name__, func=f"write({str(addr)}, {val})"
            ).print()
            return None

        if not self.is_valid_val_parameter(val):
            InvalidArgumentMessageManager(
                classes=self.__class__.__name__, func=f"write({str(addr)}, {val})"
            ).print()
            return None

        try:
            _, stderr = Popen(
                f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd W {addr} {val}",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            ).communicate()
            if stderr != b"":
                raise Exception(stderr.decode("cp949"))

            FileMessageManager(
                message=f"WRITE {val} AT ADDRESS {str(addr)}\n",
                classes=self.__class__.__name__,
                func=f"write({str(addr)}, {val})",
            ).print()

        except Exception as e:
            ExceptionMessageManager(
                message=f"EXCEPTION OCCUR : {e}",
                classes=self.__class__.__name__,
                func=f"write({str(addr)}, {val})",
            ).print()
            return None

    def read(self, addr):
        if not self.is_valid_addr_parameter(addr):
            return None

        try:
            _, stderr = Popen(
                f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd R {str(addr)}",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            ).communicate()
            if stderr != b"":
                raise Exception(stderr.decode("cp949"))
            with open(self.get_absolute_path("../result.txt")) as file_data:
                val = file_data.readline()
                FileMessageManager(
                    message=f"READ {val} FROM ADDRESS {str(addr)}\n",
                    classes="Shell",
                    func=f"read({str(addr)})",
                ).print()
            return val
        except Exception as e:
            ExceptionMessageManager(
                message=f"EXCEPTION OCCUR : {e}",
                classes=self.__class__.__name__,
                func=f"read({str(addr)})",
            ).print()
            return None

    def full_write(self, val):
        try:
            for addr in range(Shell.MAX_ADDR):
                self.write(addr, val)
        except Exception as e:
            ExceptionMessageManager(
                message=f"EXCEPTION OCCUR : {e}",
                classes=self.__class__.__name__,
                func=f"full_write({val})",
            ).print()
            return Shell.FAIL
        return Shell.SUCCESS

    def full_read(self):
        try:
            full_read_dict = {}
            for addr in range(Shell.MAX_ADDR):
                full_read_dict[addr] = self.read(addr)
        except Exception as e:
            ExceptionMessageManager(
                message=f"EXCEPTION OCCUR : {e}",
                classes=self.__class__.__name__,
                func=f"full_write()",
            ).print()
            return Shell.FAIL, full_read_dict
        return Shell.SUCCESS, full_read_dict
