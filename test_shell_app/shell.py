import os.path
import re
from subprocess import PIPE, Popen

INVALID_PARAMETER = "INVALID PARAMETER"


class Shell:
    def __init__(self):
        self._lbas = [0] * 100

    def get_absolute_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ssd_file_dir = os.path.join(script_dir, "../virtual_ssd/ssd.py")
        return ssd_file_dir

    def write(self, addr, val):
        if addr < 0 or addr > 99:
            print(INVALID_PARAMETER, flush=True)
            return None

        pattern = r"^0x[A-F0-9]{8}$"
        if not re.match(pattern, val):
            print(INVALID_PARAMETER, flush=True)
            return None

        try:
            _, stderr = Popen(
                f"python {self.get_absolute_path()} ssd W {addr} {val}",
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
        if addr < 0 or addr > 99:
            print("INVALID PARAMETER", flush=True)
            return None

        try:
            _, stderr = Popen(
                f"python {self.get_absolute_path()} ssd R {addr}",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            ).communicate()
            if stderr != b"":
                raise Exception(stderr.decode("cp949"))
            with open("../result.txt") as file_data:
                val = file_data.readline()
                print(val)
            return val
        except Exception as e:
            print(f"EXCEPTION OCCUR : {e}")
            return None

    def full_write(self, val):
        for addr in range(100):
            self.write(addr, val)

    def full_read(self):
        for addr in range(100):
            self.read(addr)
