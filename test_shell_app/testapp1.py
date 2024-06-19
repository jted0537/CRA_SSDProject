import io
import sys
from script import Script
from shell import Shell


class TestApp1(Script):
    def __init__(self, val):
        self.shell = Shell()
        self.val = val

    def run(self):
        full_write_result = self.shell.full_write(self.val)
        if full_write_result == Shell.FAIL:
            print("TestApp1 Full Write Failed")
            return False

        captured_output = io.StringIO()
        sys.stdout = captured_output

        full_read_result, full_read_dict = self.shell.full_read()

        sys.stdout = sys.__stdout__

        if full_read_result == Shell.FAIL:
            print("TestApp1 Full Read Failed")
            return False

        for addr in range(Shell.MAX_ADDR):
            if full_read_dict[addr] != self.val:
                print(
                    f"Address: {addr}, expected {self.val}, got {self.shell.read(addr)}"
                )
                return False

        print("TestApp1 Succeed")
        return True
