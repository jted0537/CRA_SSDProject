import os
from subprocess import PIPE, Popen


class Shell:
    def write(self, addr, val):
        pass

    def read(self, addr):
        if addr < 0 or addr > 99:
            print("INVALID PARAMETER", flush=True)
            return -1

        try:
            _, stderr = Popen(
                "ssd R 3", shell=True, stdout=PIPE, stderr=PIPE
            ).communicate()
            if stderr != "":
                raise Exception("stderr")
            ret = os.popen(f"ssd R {addr}").read()
            with open("../result.txt") as file_data:
                val = file_data.readline()
                print(val, end="")
            return val
        except Exception:
            print(f"EXCEPTION OCCUR")

    def exit(self):
        pass

    def help(self):
        pass

    def full_write(self):
        pass

    def full_read(self):
        pass
