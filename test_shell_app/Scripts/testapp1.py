from Utils.script import Script
from shell import Shell


class TestApp1(Script):
    def __init__(self, val="0xFFFFFFFF"):
        self.shell = Shell()
        self.val = val

    def run(self):

        self.full_write_test()

        full_read_result, full_read_dict = self.full_read_test()
        if full_read_result == Shell.FAIL:
            return False

        self.compare_write_read(full_read_dict)

        print("TestApp1 Succeed")
        return True

    def full_write_test(self):
        full_write_result = self.shell.full_write(self.val)
        if full_write_result == Shell.FAIL:
            print("TestApp1 Full Write Failed")
            return False

    def full_read_test(self):
        full_read_result, full_read_dict = self.shell.full_read()
        if full_read_result == Shell.FAIL:
            print("TestApp1 Full Read Failed")
            return full_read_result, full_read_dict
        return full_read_result, full_read_dict

    def compare_write_read(self, full_read_dict):
        for addr in range(Shell.MAX_ADDR):
            if full_read_dict[addr] != self.val:
                print(
                    f"Address: {addr}, expected {self.val}, got {full_read_dict[addr]}"
                )
                return False
