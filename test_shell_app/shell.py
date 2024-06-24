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

    def ssd_cmd_call(self, ssd_cmd):
        _, stderr = Popen(
            ssd_cmd,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        ).communicate()
        if stderr != b"":
            raise Exception(stderr.decode("cp949"))

    def print_file_message(self, message, func):
        FileMessageManager(
            message=message,
            classes=self.__class__.__name__,
            func=func,
        ).print()

    def print_exception_message(self, e, func):
        ExceptionMessageManager(
            message=f"EXCEPTION OCCUR : {e}",
            classes=self.__class__.__name__,
            func=func,
        ).print()

    def print_invalid_argument_message(self, func):
        InvalidArgumentMessageManager(
            classes=self.__class__.__name__,
            func=func,
        ).print()

    def write(self, addr, val):
        if not (
            self.is_valid_addr_parameter(addr) and self.is_valid_val_parameter(val)
        ):
            self.print_invalid_argument_message(f"write({str(addr)}, {val})")
            return None

        try:
            self.ssd_cmd_call(
                f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd W {addr} {val}"
            )

            self.print_file_message(
                f"WRITE {val} AT ADDRESS {str(addr)}\n", f"write({str(addr)}, {val})"
            )

        except Exception as e:
            self.print_exception_message(e, f"write({str(addr)}, {val})")
            return None

    def read(self, addr):
        if not self.is_valid_addr_parameter(addr):
            self.print_invalid_argument_message(f"read({str(addr)})")
            return None

        try:
            self.ssd_cmd_call(
                f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd R {str(addr)}"
            )

            with open(self.get_absolute_path("../result.txt")) as file_data:
                val = file_data.readline()
                self.print_file_message(
                    f"READ {val} FROM ADDRESS {str(addr)}\n", f"read({str(addr)})"
                )
            return val
        except Exception as e:
            self.print_exception_message(e, f"read({str(addr)})")
            return None

    def full_write(self, val):
        try:
            for addr in range(Shell.MAX_ADDR):
                self.write(addr, val)
        except Exception as e:
            self.print_exception_message(e, f"full_write({val})")
            return Shell.FAIL
        return Shell.SUCCESS

    def full_read(self):
        try:
            full_read_dict = {}
            for addr in range(Shell.MAX_ADDR):
                full_read_dict[addr] = self.read(addr)
        except Exception as e:
            self.print_exception_message(e, f"full_write()")
            return Shell.FAIL, full_read_dict
        return Shell.SUCCESS, full_read_dict

    def erase(self, addr, size):
        if not (
            self.is_valid_addr_parameter(addr)
            and self.is_valid_size_parameter(addr, size)
        ):
            self.print_invalid_argument_message(f"erase({str(addr)}, {str(size)})")
            return None

        while size > 0:
            if size > self.MAX_SSD_ERASE_SIZE:
                ssd_erase_size = self.MAX_SSD_ERASE_SIZE
            else:
                ssd_erase_size = size

            try:
                self.ssd_cmd_call(
                    f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd E {addr} {ssd_erase_size}"
                )

            except Exception as e:
                self.print_exception_message(e, f"erase({str(addr)}, {str(size)})")
                return None

            self.print_file_message(
                f"ERASE FROM ADDRESS {str(addr)} TO {str(addr + ssd_erase_size - 1)} (SIZE : {str(ssd_erase_size)})\n",
                f"erase({str(addr)}, {str(size)})",
            )

            size -= ssd_erase_size
            addr += ssd_erase_size

        return Shell.SUCCESS

    def erase_range(self, start_addr, end_addr):
        if not (
            self.is_valid_addr_parameter(start_addr)
            and self.is_valid_addr_parameter(end_addr - 1)
            and self.is_valid_start_end_addr_parameter(start_addr, end_addr)
        ):
            self.print_invalid_argument_message(
                f"erase_range({str(start_addr)}, {str(end_addr)})"
            )
            return None

        self.erase(start_addr, end_addr - start_addr)
        return Shell.SUCCESS

    def flush(self):
        try:
            self.ssd_cmd_call(
                f"python {self.get_absolute_path('../virtual_ssd/ssd.py')} ssd F"
            )
            self.print_file_message(f"FLUSH!\n", f"flush()")

        except Exception as e:
            self.print_exception_message(e, "flush()")
            return None

        return Shell.SUCCESS
