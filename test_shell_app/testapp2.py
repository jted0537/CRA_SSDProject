from script import Script
from shell import Shell

FIRST_VALUE = "0xAAAABBBB"
SECOND_VALUE = "0x12345678"


class TestApp2(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):
        [self.shell.write(j, FIRST_VALUE) for i in range(30) for j in range(5)]

        [self.shell.write(i, SECOND_VALUE) for i in range(5)]

        return [self.shell.read(i) for i in range(5)]
