from test_shell_app.Utils.script import Script
from test_shell_app.shell import Shell

FIRST_VALUE = "0xAAAABBBB"
SECOND_VALUE = "0x12345678"


class TestApp2(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):
        [self.shell.write(j, FIRST_VALUE) for i in range(30) for j in range(5)]

        [self.shell.write(i, SECOND_VALUE) for i in range(5)]

        for i in range(5):
            if self.shell.read(i) != SECOND_VALUE:
                print("TestApp2 Failed")
                return False

        print("TestApp2 Succeed")
        return True
