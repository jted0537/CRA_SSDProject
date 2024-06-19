import io
import sys
from script import Script
from shell import Shell


class TestApp1(Script):
    def __init__(self):
        self.shell = Shell()

    def run(self):
        val = "0xFFFFFFFF"
        full_write_result = self.shell.full_write(val)
        if full_write_result == Shell.FAIL:
            print("TestApp1 Full Write Failed")
            return

        captured_output = io.StringIO()
        sys.stdout = captured_output

        full_read_result, full_read_dict = self.shell.full_read()

        sys.stdout = sys.__stdout__

        if full_read_result == Shell.FAIL:
            print("TestApp1 Full Read Failed")
            return

        for addr in range(Shell.MAX_ADDR):
            if full_read_dict[addr] != val:
                print(f"Address: {addr}, expected {val}, got {self.shell.read(addr)}")
                return

        print("TestApp1 Succeed")
