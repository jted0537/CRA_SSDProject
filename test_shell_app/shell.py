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
    MAX_SSD_ERASE_SIZE = 10
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

    def get_absolute_path(self, relative_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(script_dir, relative_path))
        return file_path

    def is_valid_addr_parameter(self, addr):
        if (type(addr) is not int) or addr < 0 or addr > self.MAX_ADDR - 1:
            return False
        return True

    def is_valid_size_parameter(self, addr, size):
        if (type(size) is not int) or (size <= 0) or (addr + size > self.MAX_ADDR):
            return False
        return True

    def is_valid_start_end_addr_parameter(self, start_addr, end_addr):
        if start_addr >= end_addr:
            return False
        return True

    def is_valid_val_parameter(self, val):
        pattern = r"^0x[A-F0-9]{8}$"
        if not re.match(pattern, val):
            return False
        return True

    def write(self, addr, val):
        if not (
            self.is_valid_addr_parameter(addr) and self.is_valid_val_parameter(val)
        ):
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
            InvalidArgumentMessageManager(
                classes=self.__class__.__name__,
                func=f"read({str(addr)})",
            ).print()
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
                    classes=self.__class__.__name__,
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

    def erase(self, addr, size):
        if not (
            self.is_valid_addr_parameter(addr)
            and self.is_valid_size_parameter(addr, size)
        ):
            InvalidArgumentMessageManager(
                classes=self.__class__.__name__,
                func=f"erase({str(addr)}, {str(size)})",
            ).print()
            return None

        while size > 0:
            if size > self.MAX_SSD_ERASE_SIZE:
                ssd_erase_size = self.MAX_SSD_ERASE_SIZE
            else:
                ssd_erase_size = size

            try:
                _, stderr = Popen(
                    f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd E {addr} {ssd_erase_size}",
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE,
                ).communicate()
                if stderr != b"":
                    raise Exception(stderr.decode("cp949"))
            except Exception as e:
                ExceptionMessageManager(
                    message=f"EXCEPTION OCCUR : {e}",
                    classes=self.__class__.__name__,
                    func=f"erase({str(addr)}, {str(size)})",
                ).print()
                return None

            FileMessageManager(
                message=f"ERASE FROM ADDRESS {str(addr)} TO {str(addr + ssd_erase_size - 1)} (SIZE : {str(ssd_erase_size)})\n",
                classes=self.__class__.__name__,
                func=f"erase({str(addr)}, {str(size)})",
            ).print()
            size -= ssd_erase_size
            addr += ssd_erase_size

        return Shell.SUCCESS

    def erase_range(self, start_addr, end_addr):
        if not (
            self.is_valid_addr_parameter(start_addr)
            and self.is_valid_addr_parameter(end_addr - 1)
            and self.is_valid_start_end_addr_parameter(start_addr, end_addr)
        ):
            InvalidArgumentMessageManager(
                classes=self.__class__.__name__,
                func=f"erase_range({str(start_addr)}, {str(end_addr)})",
            ).print()
            return None

        self.erase(start_addr, end_addr - start_addr)
        return Shell.SUCCESS

    def flush(self):
        pass
