from subprocess import PIPE, Popen
import re

LEN_LBAS = 100
INVALID_PARAMETER = "INVALID PARAMETER"


class Shell:
    def __init__(self):
        self._lbas = [0] * 100

    def write(self, addr, val):
        if addr < 0 or addr > 99:
            print(INVALID_PARAMETER, flush=True)
            return ""

        pattern = r"^0x[A-F0-9]+$"
        if not re.match(pattern, val):
            print(INVALID_PARAMETER, flush=True)
            return ""

        try:
            _, stderr = Popen(
                f"ssd W {addr} {val}", shell=True, stdout=PIPE, stderr=PIPE
            ).communicate()
            if stderr != "":
                raise Exception("stderr")

        except Exception as e:
            print(f"EXCEPTION OCCUR {e}")
            return ""

    def read(self, addr):
        if addr < 0 or addr > 99:
            print("INVALID PARAMETER", flush=True)
            return ""

        try:
            _, stderr = Popen(
                f"ssd R {addr}", shell=True, stdout=PIPE, stderr=PIPE
            ).communicate()
            if stderr != "":
                raise Exception("stderr")

            with open("../result.txt") as file_data:
                val = file_data.readline()
                print(val, end="")
            return val
        except Exception as e:
            print(f"EXCEPTION OCCUR {e}")
            return ""

    def exit(self):
        pass

    def help(self):
        pass

    def full_write(self, val):
        for addr in range(LEN_LBAS):
            self.write(addr, val)

    def full_read(self):
        for addr in range(LEN_LBAS):
            self.read(addr)
