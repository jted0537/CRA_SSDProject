from Utils.script import Script
from shell import Shell


class FullRead3AndCompare(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):
        previous_result = None
        for i in range(3):
            full_read_result, full_read_dict = self.shell.full_read()
            if full_read_result == Shell.FAIL:
                print("FullRead3AndCompare Full Read Failed")
                return False
            if i == 0:
                previous_result = full_read_dict
            else:
                if previous_result != full_read_dict:
                    print("FullRead3AndCompare Value Compare Test Failed")
                    return False

        print("FullRead3AndCompare Succeed")
        return True
