from subprocess import PIPE, Popen


class Shell:
    def write(self, addr, val):
        pass

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

    def full_write(self):
        pass

    def full_read(self):
        pass
