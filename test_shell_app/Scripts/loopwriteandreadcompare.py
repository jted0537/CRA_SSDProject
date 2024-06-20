from Utils.script import Script
from shell import Shell


class LoopWriteAndReadCompare(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):

        for loop in range(10):
            value = "0x0000000" + str(loop)

            [self.shell.write(i, value) for i in range(5)]

            for i in range(5):
                if self.shell.read(i) != value:
                    print("LoopWriteAndReadCompare Failed")
                    return False

        print("LoopWriteAndReadCompare Success")
        return True
