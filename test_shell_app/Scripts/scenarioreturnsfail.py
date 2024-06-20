from test_shell_app.Utils.script import Script
from test_shell_app.shell import Shell


class ScenarioReturnsFail(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):
        return False
