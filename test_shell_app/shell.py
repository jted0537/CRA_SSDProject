import os.path
import re
from subprocess import PIPE, Popen

from Utils.message_manager import InvalidArgumentMessageManager


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
            InvalidArgumentMessageManager().print()
            return False
        return True

    def is_valid_val_parameter(self, val):
        pattern = r"^0x[A-F0-9]{8}$"
        if not re.match(pattern, val):
            InvalidArgumentMessageManager().print()
            return False
        return True

    def write(self, addr, val):
        if not self.is_valid_addr_parameter(addr):
            return None

        if not self.is_valid_val_parameter(val):
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

        except Exception as e:
            print(f"EXCEPTION OCCUR : {e}")
            return None

    def read(self, addr):
        if not self.is_valid_addr_parameter(addr):
            return None

        try:
            _, stderr = Popen(
                f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd R {addr}",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            ).communicate()
            if stderr != b"":
                raise Exception(stderr.decode("cp949"))
            with open(self.get_absolute_path("../result.txt")) as file_data:
                val = file_data.readline()
                print(val)
            return val
        except Exception as e:
            print(f"EXCEPTION OCCUR : {e}")
            return None

    def full_write(self, val):
        try:
            for addr in range(Shell.MAX_ADDR):
                self.write(addr, val)
        except:
            return Shell.FAIL
        return Shell.SUCCESS

    def full_read(self):
        try:
            full_read_dict = {}
            for addr in range(Shell.MAX_ADDR):
                full_read_dict[addr] = self.read(addr)
        except:
            return Shell.FAIL, full_read_dict
        return Shell.SUCCESS, full_read_dict

    def erase(self, addr, size):
        pass

    def erase_range(self, start_addr, end_addr):
        pass

    def flush(self):
        pass
