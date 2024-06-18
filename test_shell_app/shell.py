import re
from subprocess import PIPE, Popen

INVALID_PARAMETER = "INVALID PARAMETER"


class Shell:
    MAX_ADDR = 100

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
                f"python ../virtual_ssd/ssd.py ssd W {addr} {val}",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            ).communicate()
            if stderr != "":
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
                f"python ../virtual_ssd/ssd.py ssd R {addr}",
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            ).communicate()
            if stderr != "":
                raise Exception(stderr.decode("cp949"))
            with open("../result.txt") as file_data:
                val = file_data.readline()
                print(val)
            return val
        except Exception as e:
            print(f"EXCEPTION OCCUR : {e}")
            return None

    def full_write(self, val):
        for addr in range(self.MAX_ADDR):
            self.write(addr, val)

    def full_read(self):
        for addr in range(self.MAX_ADDR):
            self.read(addr)
